import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN", "")
GUMROAD_PRODUCT_ID = os.environ.get("GUMROAD_PRODUCT_ID", "")

SHOP_NAME = "PrintMint Shop"
SHOP_DESCRIPTION = "Premium AI-crafted SVG designs for t-shirts, mugs, posters & more"
SHOP_URL = "https://bybilal.gumroad.com"

PRODUCT_PRICE = 2.99

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGNS_DIR = os.path.join(BASE_DIR, "docs", "designs")
STORE_FILE = os.path.join(BASE_DIR, "docs", "index.html")

DESIGN_CATEGORIES = [
    "Minimalist Logo",
    "Typography Quote",
    "Geometric Pattern",
    "Nature & Outdoors",
    "Tech & Programming",
    "Fitness & Sports",
    "Music & Arts",
    "Animals & Pets",
    "Funny & Meme",
    "Vintage Retro",
    "Abstract Art",
    "Gaming",
    "Travel & Adventure",
    "Space & Science",
    "Fantasy & Magic",
]

DAILY_OUTPUT = 3
