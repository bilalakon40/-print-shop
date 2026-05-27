import os
import sys
from datetime import datetime
from generate import generate_batch
from gumroad import publish_designs
from store import generate_store_page, generate_catalog_json


def main():
    print(f"[{datetime.now()}] Print Shop Bot starting...")
    designs = generate_batch()
    if not designs:
        print("No designs generated. Exiting.")
        return
    print(f"\nGenerated {len(designs)} designs")
    results = publish_designs(designs)
    published = [d for d in results if d.get("gumroad")]
    print(f"\nPublished {len(published)}/{len(results)} to Gumroad")
    generate_store_page(results)
    generate_catalog_json(results)
    print(f"\n[{datetime.now()}] Print Shop Bot complete!")


if __name__ == "__main__":
    main()
