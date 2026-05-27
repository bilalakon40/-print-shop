import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN", "")

PRODUCT_PRICES = {
    "copywriting": 9,
    "social_media": 9,
    "email_marketing": 9,
    "seo": 12,
    "real_estate": 12,
    "freelance": 14,
    "business": 14,
    "content_creation": 9,
    "ecommerce": 12,
    "blogging": 9,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_DIR = os.path.join(BASE_DIR, "products")
STORE_FILE = os.path.join(BASE_DIR, "docs", "index.html")

DAILY_OUTPUT = 2
