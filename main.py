from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import ProductModel, Product, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au démarrage
    db = SessionLocal()
    seed_products(db)
    db.close()
    yield
    # À l'arrêt (optionnel, tu peux mettre du cleanup ici)

app = FastAPI(lifespan=lifespan)

# Crée la table "products" si elle n'existe pas
Base.metadata.create_all(bind=engine)

# Dépendance session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Données initiales à insérer au 1er lancement
def seed_products(db: Session):
    if db.query(ProductModel).count() == 0:  # évite les doublons
        initial_products = [
            ProductModel(id=1, name="iPhone 15 Pro", description="Smartphone Apple avec puce A17 Pro, écran 6.1 Super Retina XDR", price=1199.99, quantity=25),
            ProductModel(id=2, name="Samsung Galaxy S24", description="Smartphone Samsung avec Snapdragon 8 Gen 3, écran 6.2 Dynamic AMOLED", price=899.99, quantity=40),
            ProductModel(id=3, name="Google Pixel 8", description="Smartphone Google avec puce Tensor G3, appareil photo 50MP", price=699.99, quantity=30),
            ProductModel(id=4, name="Xiaomi 14", description="Smartphone Xiaomi avec Snapdragon 8 Gen 3, charge rapide 90W", price=599.99, quantity=50),
            ProductModel(id=5, name="MacBook Pro 14", description="Laptop Apple avec puce M3 Pro, 18GB RAM, SSD 512GB", price=2199.99, quantity=15),
            ProductModel(id=6, name="Dell XPS 15", description="Laptop Dell avec Intel Core i7-13700H, 16GB RAM, RTX 4060", price=1799.99, quantity=20),
            ProductModel(id=7, name="Lenovo ThinkPad X1 Carbon", description="Ultrabook professionnel Intel Core i7, 16GB RAM, SSD 1TB", price=1499.99, quantity=18),
            ProductModel(id=8, name="ASUS ROG Zephyrus G14", description="Laptop gaming AMD Ryzen 9, RTX 4070, 32GB RAM, écran 165Hz", price=1699.99, quantity=12),
        ]
        db.add_all(initial_products)
        db.commit()


@app.get("/home")
def greet():
    return "Welcome to my First FastAPI project !"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@app.get("/product/{id}")
def get_product_byid(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if product:
        return product
    return "Product not found"

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/product/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if db_product:
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return "Product Updated Successfully"
    return "No Product Found"

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    return "No Product Found"
