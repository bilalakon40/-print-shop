import json
import os
import urllib.request
from config import GUMROAD_TOKEN, PRODUCTS_DIR

GUMROAD_API = "https://api.gumroad.com/v2"


def create_product(product):
    if not GUMROAD_TOKEN:
        print("GUMROAD_TOKEN not set, saving locally only")
        return None
    description = product["description"]
    description += f"\n\n✅ {product['prompts_count']} ready-to-use ChatGPT prompts"
    description += f"\n✅ Organized by category for easy browsing"
    description += f"\n✅ Instant PDF + TXT download"
    description += f"\n✅ Works with ChatGPT, Claude, Gemini & more"
    description += f"\n✅ Lifetime access — never expires"
    payload = json.dumps({
        "access_token": GUMROAD_TOKEN,
        "name": product["title"],
        "description": description,
        "price": product["price"] * 100,
        "tags": ["chatgpt", "ai prompts", "chatgpt prompts", product["niche"].lower().replace(" ", "-"), "digital product"],
        "currency": "usd",
        "require_shipping": False,
        "customizable_price": False,
    }).encode()
    try:
        req = urllib.request.Request(
            f"{GUMROAD_API}/products",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        if result.get("success"):
            product_data = result["product"]
            product_url = product_data.get("short_url", product_data.get("url", ""))
            print(f"  OK: {product_url}")
            return {"id": product_data["id"], "url": product_url}
        else:
            msg = result.get("message", str(result))
            print(f"  ERROR: {msg}")
            return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def publish_products(products):
    results = []
    for p in products:
        print(f"Uploading {p['title']} to Gumroad...")
        p["gumroad"] = create_product(p)
        results.append(p)
    return results
