import os
import sys
from datetime import datetime
from generate import generate_batch
from gumroad import publish_products
from store import generate_store_page, generate_catalog_json


def main():
    print(f"[{datetime.now()}] AI Prompt Store Bot starting...")
    products = generate_batch()
    if not products:
        print("No products generated. Exiting.")
        return
    print(f"\nGenerated {len(products)} products")
    results = publish_products(products)
    published_count = sum(1 for p in results if p.get("gumroad"))
    print(f"\nPublished {published_count}/{len(results)} to Gumroad")
    generate_store_page(results)
    generate_catalog_json(results)
    print(f"\n[{datetime.now()}] AI Prompt Store Bot complete!")


if __name__ == "__main__":
    main()
