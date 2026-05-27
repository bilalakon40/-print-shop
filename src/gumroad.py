import json
import urllib.request
from config import GUMROAD_TOKEN, PRODUCT_PRICE

GUMROAD_API = "https://api.gumroad.com/v2"


def create_product(design):
    if not GUMROAD_TOKEN:
        print("GUMROAD_TOKEN not set, saving locally only")
        return None
    payload = json.dumps({
        "access_token": GUMROAD_TOKEN,
        "name": f"{design['title']} - {design['category']} SVG",
        "description": design["description"],
        "price": int(PRODUCT_PRICE * 100),
        "tags": design["tags"][:5],
        "currency": "usd",
        "require_shipping": False,
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
            product = result.get("product", {})
            product_url = product.get("short_url", product.get("url", ""))
            product_id = product.get("id", "")
            print(f"  OK: {product_url}")
            return {"id": product_id, "url": product_url}
        else:
            print(f"  ERROR: {result.get('message', result)}")
            return None
    except Exception as e:
        print(f"  ERROR: Gumroad API error: {e}")
        return None


def publish_designs(designs):
    results = []
    for d in designs:
        print(f"Uploading {d['title']} to Gumroad...")
        d["gumroad"] = create_product(d)
        results.append(d)
    return results
