from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()

@router.get("/", response_model=List[ProductResponse], summary="List all products")
def read_products(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max items to return"),
    db: Session = Depends(get_db),
):
    """Retrieve all products with pagination."""
    return get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by its primary key ID."""
    db_product = get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return db_product

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
def create_new_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product record in the database."""
    return create_product(db, product_in=product_in)

@router.patch("/{product_id}", response_model=ProductResponse, summary="Update product")
def update_existing_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    """Partially update an existing product."""
    db_product = get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return update_product(db, db_product=db_product, product_in=product_in)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product",
)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product from the database."""
    db_product = delete_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return {"message": f"Product {product_id} deleted successfully"}
