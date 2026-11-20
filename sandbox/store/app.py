"""Instrumented mock e-commerce store for sandbox validation experiments."""

from __future__ import annotations

import os
import uuid
from typing import Any

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

TELEMETRY_URL = os.environ.get("TELEMETRY_URL", "http://localhost:8090").rstrip("/")
STORE_PUBLIC_URL = os.environ.get("STORE_PUBLIC_URL", "http://localhost:8080").rstrip("/")

PRODUCTS: list[dict[str, Any]] = [
    {
        "id": "sku-tees-01",
        "name": "Canvas Tee",
        "price_cents": 2400,
        "category": "apparel",
        "description": "Soft cotton tee for everyday wear.",
    },
    {
        "id": "sku-mug-02",
        "name": "Studio Mug",
        "price_cents": 1800,
        "category": "home",
        "description": "Matte ceramic mug, 350 ml.",
    },
    {
        "id": "sku-bag-03",
        "name": "Field Tote",
        "price_cents": 4200,
        "category": "bags",
        "description": "Heavy canvas tote with interior pocket.",
    },
]

# In-memory carts keyed by sandbox session id.
CARTS: dict[str, dict[str, int]] = {}

app = FastAPI(title="Agent Hunt Sandbox Store", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class CartAdd(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=20)


def _session_id(request: Request) -> str:
    sid = request.cookies.get("sandbox_session_id")
    if not sid:
        sid = str(uuid.uuid4())
    return sid


def _cart_items(session_id: str) -> list[dict[str, Any]]:
    cart = CARTS.get(session_id, {})
    items: list[dict[str, Any]] = []
    for product_id, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if product:
            items.append({**product, "quantity": qty, "line_total_cents": product["price_cents"] * qty})
    return items


def _render(request: Request, name: str, **context: Any) -> HTMLResponse:
    session_id = _session_id(request)
    response = templates.TemplateResponse(
        request,
        name,
        {
            "request": request,
            "products": PRODUCTS,
            "cart_items": _cart_items(session_id),
            "session_id": session_id,
            "telemetry_url": TELEMETRY_URL,
            "store_public_url": STORE_PUBLIC_URL,
            **context,
        },
    )
    if "sandbox_session_id" not in request.cookies:
        response.set_cookie("sandbox_session_id", session_id, httponly=False, samesite="lax")
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "store"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return _render(request, "home.html", page="home")


@app.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: str) -> HTMLResponse:
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product is None:
        return HTMLResponse("Product not found", status_code=404)
    return _render(request, "product.html", page="product", product=product)


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request) -> HTMLResponse:
    items = _cart_items(_session_id(request))
    total = sum(i["line_total_cents"] for i in items)
    return _render(request, "cart.html", page="cart", total_cents=total)


@app.post("/api/cart/add")
async def add_to_cart(request: Request, body: CartAdd) -> dict[str, Any]:
    session_id = _session_id(request)
    if not any(p["id"] == body.product_id for p in PRODUCTS):
        return {"ok": False, "error": "unknown_product"}
    cart = CARTS.setdefault(session_id, {})
    cart[body.product_id] = cart.get(body.product_id, 0) + body.quantity
    return {"ok": True, "cart": cart, "session_id": session_id}


@app.post("/cart/add")
async def add_to_cart_form(
    request: Request,
    product_id: str = Form(...),
    quantity: int = Form(1),
) -> RedirectResponse:
    session_id = _session_id(request)
    if any(p["id"] == product_id for p in PRODUCTS):
        cart = CARTS.setdefault(session_id, {})
        cart[product_id] = cart.get(product_id, 0) + max(1, min(quantity, 20))
    response = RedirectResponse(url="/cart", status_code=303)
    if "sandbox_session_id" not in request.cookies:
        response.set_cookie("sandbox_session_id", session_id, httponly=False, samesite="lax")
    return response


@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request) -> HTMLResponse:
    items = _cart_items(_session_id(request))
    total = sum(i["line_total_cents"] for i in items)
    return _render(request, "checkout.html", page="checkout", total_cents=total)


@app.post("/checkout")
async def checkout_submit(
    request: Request,
    email: str = Form("shopper@example.com"),
    name: str = Form("Sandbox Shopper"),
) -> HTMLResponse:
    session_id = _session_id(request)
    items = _cart_items(session_id)
    total = sum(i["line_total_cents"] for i in items)
    order_id = str(uuid.uuid4())[:8]
    CARTS[session_id] = {}
    return _render(
        request,
        "receipt.html",
        page="receipt",
        order_id=order_id,
        email=email,
        customer_name=name,
        items=items,
        total_cents=total,
    )


@app.get("/api/products")
def list_products() -> list[dict[str, Any]]:
    return PRODUCTS
