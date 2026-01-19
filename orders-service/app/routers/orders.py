from fastapi import APIRouter, HTTPException
import requests
from app.database.database import SessionLocal
from app.models.orders import Order
import json
import logging

logger = logging.getLogger("orders-service")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ORDERS SERVICE] - %(message)s')

router = APIRouter(prefix="/orders", tags=["orders"])

PRODUCT_SERVICE_URL = "http://localhost:8002/products"

# listamos todas las ordenes
@router.get("/")
def list_all_orders():
    logger.info("GET /orders recibido")
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    
    logger.info(f"BD: Recuperadas {len(orders)} ordenes")
    return orders


# mostramos la orden por su id
@router.get("/{order_id}")
def list_orders_from_id(order_id: int):
    logger.info(f"GET /orders/{order_id} recibido")
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    db.close()
    
    if not order:
        logger.error(f"Orden {order_id} no encontrada")
        raise HTTPException(status_code=404, detail="Order not found")
    
    logger.info(f"BD: Orden {order_id} encontrada")
    return order


# creamos una orden
@router.post("/")
def create_order(order: dict):
    logger.info(f"POST /orders - Producto ID: {order.get('product_id')}, Cantidad: {order.get('quantity')}")
    if not isinstance(order, dict) or "product_id" not in order or "quantity" not in order:
        raise HTTPException(status_code=422, detail="Invalid order data")
    
    # verificamos que exista el producto
    logger.info(f"Verificando existencia de producto {order['product_id']} en Products Service")
    headers = {"Authorization": "Bearer pindeacceso3344"}
    response = requests.get(f"{PRODUCT_SERVICE_URL}/{order['product_id']}", headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Product does not exist")
    
    logger.info(f"Producto {order['product_id']} validado correctamente")
    
    db = SessionLocal()
    new_order = Order(product_id=order["product_id"], quantity=order["quantity"])
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()
    
    logger.info(f"BD: Orden creada con ID {new_order.id}")
    return new_order


# eliminamos una orden por su id
@router.delete("/{order_id}")
def delete_order(order_id: int):
    logger.info(f"DELETE /orders/{order_id} recibido")
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        db.close()
        logger.error(f"Orden {order_id} no encontrada")
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    db.close()
    
    logger.info(f"BD: Orden {order_id} eliminada")
    return {"message": f"Order with id {order_id} deleted"}