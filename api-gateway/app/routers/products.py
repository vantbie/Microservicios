from fastapi import APIRouter, Depends
from app.auth.auth import verify_token
from app.models.products import ProductCreate, ProductUpdate
import requests
import json
import logging

logger = logging.getLogger("api-gateway")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [API GATEWAY] - %(message)s')

router = APIRouter(prefix="/products", tags=["products"])

PRODUCTS_SERVICE_URL = "http://localhost:8002/products"

@router.get("/")
def proxy_list_products(token: str = Depends(verify_token)):
    
    logger.info("GET /products recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Products Service: {PRODUCTS_SERVICE_URL}")
    
    response = requests.get(PRODUCTS_SERVICE_URL, headers=headers)
    try:
        data = response.json()
        logger.info(f"Respuesta exitosa - {len(data)} productos recuperados")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()


@router.get("/{product_id}")
def proxy_product_id(product_id: int, token: str = Depends(verify_token)):
    
    logger.info(f"GET /products/{product_id} recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Products Service: {PRODUCTS_SERVICE_URL}/{product_id}")
    
    response = requests.get(f"{PRODUCTS_SERVICE_URL}/{product_id}", headers=headers)
    try:
        data = response.json()
        logger.info(f"Producto {product_id} recuperado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()


@router.post("/")
def proxy_create_product(product: ProductCreate, token: str = Depends(verify_token)):
    
    logger.info(f"POST /products - Nombre: {product.name}, Precio: {product.price}")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Products Service: {PRODUCTS_SERVICE_URL}")
    
    response = requests.post(PRODUCTS_SERVICE_URL, json=product.dict(), headers=headers)
    try:
        data = response.json()
        logger.info("Producto creado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()


@router.delete("/{product_id}")
def proxy_delete_product(product_id: int, token: str = Depends(verify_token)):
    
    logger.info(f"DELETE /products/{product_id} recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Products Service: {PRODUCTS_SERVICE_URL}/{product_id}")
    
    response = requests.delete(f"{PRODUCTS_SERVICE_URL}/{product_id}", headers=headers)
    try:
        data = response.json()
        logger.info(f"Producto {product_id} eliminado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()

@router.put("/{product_id}")
def proxy_update_product(product_id: int, product: ProductUpdate, token: str = Depends(verify_token)):
    logger.info(f"PUT /products/{product_id} recibido - Nombre: {product.name}, Precio: {product.price}")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Products Service: {PRODUCTS_SERVICE_URL}/{product_id}")
    
    response = requests.put(f"{PRODUCTS_SERVICE_URL}/{product_id}", json=product.dict(exclude_none=True), headers=headers)
    try:
        data = response.json()
        logger.info(f"Producto {product_id} actualizado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()