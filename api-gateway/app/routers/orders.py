from fastapi import APIRouter, Depends, HTTPException
from app.auth.auth import verify_token
from app.models.orders import OrderCreate
from app.core.circuit_breaker import orders_cb, products_cb
import requests
import json
import logging

logger = logging.getLogger("api-gateway")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [API GATEWAY] - %(message)s')

router = APIRouter(prefix="/orders", tags=["orders"])

PRODUCTS_SERVICE_URL = "http://localhost:8002/products"
ORDERS_SERVICE_URL = "http://localhost:8003/orders"



@router.get("/")
def proxy_list_orders(token: str = Depends(verify_token)):
    logger.info("GET /orders recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Orders Service: {ORDERS_SERVICE_URL}")
    
    response = requests.get(ORDERS_SERVICE_URL, headers=headers)
    try:
        data = response.json()
        logger.info(f"Respuesta exitosa - {len(data)} ordenes recuperadas")
    except:
        logger.error(f"Error en respuesta: {response.text}")
        
    return response.json()


@router.get("/{order_id}")
def proxy_order_id(order_id: int, token: str = Depends(verify_token)):
    logger.info(f"GET /orders/{order_id} recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Orders Service: {ORDERS_SERVICE_URL}/{order_id}")
    
    response = requests.get(f"{ORDERS_SERVICE_URL}/{order_id}", headers=headers)
    try:
        data = response.json()
        logger.info(f"Orden {order_id} recuperada exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()


@router.post("/")
def proxy_create_order(order: OrderCreate, token: str = Depends(verify_token)):
    headers = {"Authorization": f"Bearer {token}"}
    
    # Circuit Breaker para Products
    if not products_cb.allow_request():
        raise HTTPException(503, f"Products Service no disponible (circuit abierto)")

    # Circuit Breaker para Orders
    if not orders_cb.allow_request():
        raise HTTPException(503, f"Orders Service no disponible (circuit abierto)")


    # Llamada a Products
    try:
        logger.info(f"Llamando a Products Service para product_id: {order.product_id}")
        prod_resp = requests.get(f"{PRODUCTS_SERVICE_URL}/{order.product_id}", headers=headers)
        prod_resp.raise_for_status()
        products_cb.record_success()
    except requests.RequestException as e:
        logger.error(f"Error en Products Service: {e}")
        products_cb.record_failure()
        raise HTTPException(503, "Products Service no disponible")

    # Llamada a Orders
    try:
        logger.info(f"Llamando a Orders Service para crear orden: {order.dict()}")
        order_resp = requests.post(ORDERS_SERVICE_URL, json=order.dict(), headers=headers)
        order_resp.raise_for_status()
        orders_cb.record_success()
        return order_resp.json()
    except requests.RequestException as e:
        logger.error(f"Error en Orders Service: {e}")
        orders_cb.record_failure()
        raise HTTPException(503, "Orders Service no disponible")
    
    
@router.delete("/{order_id}")
def proxy_delete_order(order_id: int, token: str = Depends(verify_token)):
    logger.info(f"DELETE /orders/{order_id} recibido")

    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Orders Service: {ORDERS_SERVICE_URL}/{order_id}")
    
    response = requests.delete(f"{ORDERS_SERVICE_URL}/{order_id}", headers=headers)
    try:
        data = response.json()
        logger.info(f"Orden {order_id} eliminada exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()