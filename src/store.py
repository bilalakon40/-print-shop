import os
import json
from config import SHOP_NAME, SHOP_DESCRIPTION, SHOP_URL, PRODUCT_PRICE, STORE_FILE, DESIGNS_DIR


def generate_store_page(designs):
    cards = ""
    for d in designs:
        gumroad_info = d.get("gumroad") or {}
        gumroad_url = gumroad_info.get("url", "#")
        file_name = d.get("file_name", "design.svg")
        cards += f"""
        <div class="product" onclick="window.open('{gumroad_url}','_blank')">
            <img src="designs/{file_name}" alt="{d['title']}">
            <div class="info">
                <h3>{d['title']}</h3>
                <span class="tag">{d['category']}</span>
                <span class="price">${PRODUCT_PRICE}</span>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SHOP_NAME}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #fff; min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        header {{ text-align: center; margin-bottom: 50px; }}
        header h1 {{ font-size: 2.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        header p {{ color: #888; margin-top: 10px; font-size: 1.1em; }}
        .store-link {{ display: inline-block; margin-top: 15px; padding: 12px 30px; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; text-decoration: none; border-radius: 25px; font-weight: 600; transition: transform 0.2s; }}
        .store-link:hover {{ transform: scale(1.05); }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }}
        .product {{ background: #1a1a1a; border-radius: 15px; overflow: hidden; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s; }}
        .product:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(102,126,234,0.2); }}
        .product img {{ width: 100%; height: 280px; object-fit: contain; background: #fff; padding: 20px; }}
        .product .info {{ padding: 20px; }}
        .product h3 {{ font-size: 1.1em; margin-bottom: 8px; }}
        .product .tag {{ display: inline-block; padding: 4px 12px; background: #333; border-radius: 12px; font-size: 0.8em; color: #aaa; }}
        .product .price {{ float: right; color: #667eea; font-weight: bold; font-size: 1.2em; }}
        .buy-btn {{ display: block; width: 100%; padding: 12px; margin-top: 15px; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; border: none; border-radius: 8px; font-size: 1em; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }}
        .buy-btn:hover {{ opacity: 0.9; }}
        footer {{ text-align: center; color: #555; margin-top: 60px; padding: 20px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{SHOP_NAME}</h1>
            <p>{SHOP_DESCRIPTION}</p>
            <a class="store-link" href="{SHOP_URL}" target="_blank">Visit Full Store on Gumroad →</a>
        </header>
        <div class="grid">
            {cards}
        </div>
        <footer>
            <p>© 2026 {SHOP_NAME}. Instant digital download. Print at home or use a print-on-demand service.</p>
        </footer>
    </div>
</body>
</html>"""

    os.makedirs(os.path.dirname(STORE_FILE), exist_ok=True)
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Store page generated: {STORE_FILE}")


def generate_catalog_json(designs):
    catalog = []
    for d in designs:
        gumroad_info = d.get("gumroad") or {}
        catalog.append({
            "title": d["title"],
            "category": d["category"],
            "description": d["description"],
            "price": PRODUCT_PRICE,
            "file": d.get("file_name", ""),
            "gumroad_url": gumroad_info.get("url", ""),
            "tags": d.get("tags", []),
        })
    catalog_path = os.path.join(os.path.dirname(STORE_FILE), "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Catalog JSON generated: {catalog_path}")
