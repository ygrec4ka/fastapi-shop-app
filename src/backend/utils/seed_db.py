import asyncio
import random
import argparse
from sqlalchemy import select, delete
from backend.core.models.db_helper import db_helper
from backend.core.models import Product, Category

CATEGORIES_DATA = [
    {"name": "Electronics", "slug": "electronics"},
    {"name": "Clothing", "slug": "clothing"},
    {"name": "Home & Garden", "slug": "home-garden"},
    {"name": "Sports", "slug": "sports"},
    {"name": "Books", "slug": "books"},
]

PRODUCT_NAMES = [
    "UltraHD Smart TV", "Wireless Noise-Canceling Headphones", "PowerMax Smartphone",
    "Cotton Comfort T-Shirt", "Leather Slim Wallet", "Designer Sunglasses",
    "Ergonomic Office Chair", "Instant-Heating Kettle", "Smart Home Assistant",
    "Professional DSLR Camera", "Mechanical Gaming Keyboard", "Yoga Fitness Mat",
    "Kitchen Knife Set", "Electric Coffee Grinder", "Bluetooth Soundbar",
    "Travel Laptop Backpack", "Running Performance Sneakers", "Classic Fountain Pen",
    "Mountain Explorer Bike", "Organic Tea Collection"
]

async def seed(reset: bool = False):
    async with db_helper.session_factory() as session:
        if reset:
            print("Resetting database (deleting products and categories)...")
            await session.execute(delete(Product))
            await session.execute(delete(Category))
            await session.commit()

        result = await session.execute(select(Category))
        existing_categories = result.scalars().all()
        
        if not existing_categories:
            print("Creating categories...")
            categories = [Category(**cat) for cat in CATEGORIES_DATA]
            session.add_all(categories)
            await session.commit()
            for cat in categories:
                await session.refresh(cat)
            existing_categories = categories
        else:
            print(f"Categories already exist: {len(existing_categories)}")

        result = await session.execute(select(Product))
        existing_products_count = len(result.scalars().all())
        
        needed = max(0, 50 - existing_products_count)
        if needed > 0:
            print(f"Adding {needed} products...")
            for i in range(needed):
                cat = random.choice(existing_categories)
                name_prefix = random.choice(PRODUCT_NAMES)
                name = f"{name_prefix} #{i+1}"
                new_product = Product(
                    name=name,
                    description=f"High quality {name.lower()} with amazing features. Best choice for {cat.name}.",
                    price=float(random.randint(500, 50000)),
                    category_id=cat.id,
                    image_url=None
                )
                session.add(new_product)
            
            await session.commit()
            print("Successfully added products.")
        else:
            print("Already have 50 or more products.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database with products and categories.")
    parser.add_argument("--reset", action="store_true", help="Delete all existing products and categories before seeding.")
    args = parser.parse_args()

    asyncio.run(seed(reset=args.reset))
