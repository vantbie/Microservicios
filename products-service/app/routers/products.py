from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.products import Product, ProductUpdate
import json
import logging

logger = logging.getLogger("products-service")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [PRODUCTS SERVICE] - %(message)s')

router = APIRouter(prefix="/products", tags=["products"])

# listar los productos
@router.get("/")
def list_products():
    logger.info("GET /products recibido")
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    
    logger.info(f"BD: Recuperados {len(products)} productos")
    return products


@router.get("/{product_id}")
def list_product_id(product_id: int):
    
    logger.info(f"GET /products/{product_id} recibido")
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    
    if not product:
        logger.error(f"Producto {product_id} no encontrado")
        raise HTTPException(status_code=404, detail="Product not found")
    
    logger.info(f"BD: Producto {product_id} encontrado")
    return product


@router.post("/")
def create_product(product: dict):
    logger.info(f"POST /products - Nombre: {product.get('name')}, Precio: {product.get('price')}")
    
    if not isinstance(product, dict) or "name" not in product or "price" not in product:
        logger.error("Estructura de datos inválida")
        raise HTTPException(status_code=422, detail="Invalid product data")
    
    db = SessionLocal()
    new_product = Product(name=product["name"], price=product["price"])
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    db.close()
    
    logger.info(f"BD: Producto creado con ID {new_product.id}")
    return new_product


@router.delete("/{product_id}")
def delete_product(product_id: int):
    logger.info(f"DELETE /products/{product_id} recibido")
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        db.close()
        logger.error(f"Producto {product_id} no encontrado")
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    db.close()
    
    logger.info(f"BD: Producto {product_id} eliminado")
    return {"message": f"Product with id {product_id} deleted"}


@router.put("/{product_id}")
def update_product(product_id: int, update: ProductUpdate):
    logger.info(f"PUT /products/{product_id} recibido")
    
    update_data = update.dict(exclude_none=True)
    
    if not update_data:
        logger.error("Estructura de datos inválida")
        raise HTTPException(status_code=422, detail="Invalid update data")
    
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        db.close()
        logger.error(f"Producto {product_id} no encontrado")
        raise HTTPException(status_code=404, detail="Product not found")
    
    if "name" in update_data:
        product.name = update_data["name"]
        
    if "price" in update_data:
        product.price = update_data["price"]
    
    db.commit()
    db.close()
    
    logger.info(f"BD: Producto {product_id} actualizado")
    return product