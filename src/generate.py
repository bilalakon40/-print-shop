import json
import os
import random
import urllib.request
import urllib.error
from datetime import datetime
from config import GROQ_API_KEY, PRODUCT_PRICES, PRODUCTS_DIR, DAILY_OUTPUT

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

PRODUCT_TEMPLATES = [
    {
        "id": "copywriting",
        "title": "ChatGPT Prompts for Copywriting",
        "tagline": "Write persuasive copy that converts browsers into buyers",
        "niche": "Marketing & Copywriting",
        "prompts_count": 30,
        "description": "Tired of staring at a blank page? This pack of 30 battle-tested ChatGPT prompts will help you write high-converting copy for landing pages, emails, ads, and sales letters in minutes.",
    },
    {
        "id": "social_media",
        "title": "AI Prompts for Social Media Marketing",
        "tagline": "Generate viral content for every platform in seconds",
        "niche": "Social Media",
        "prompts_count": 35,
        "description": "Stop struggling with content ideas. This pack includes 35 ChatGPT prompts designed to help you create scroll-stopping posts, captions, and threads for Instagram, TikTok, LinkedIn, and Twitter.",
    },
    {
        "id": "email_marketing",
        "title": "ChatGPT Prompts for Email Marketing",
        "tagline": "Write emails that get opened, read, and clicked",
        "niche": "Email Marketing",
        "prompts_count": 25,
        "description": "Email is still the highest-ROI marketing channel. This pack of 25 prompts helps you write welcome sequences, sales emails, newsletters, and follow-ups that actually convert.",
    },
    {
        "id": "seo",
        "title": "SEO Content System: ChatGPT Prompts",
        "tagline": "Rank higher on Google with AI-optimized content",
        "niche": "SEO & Content",
        "prompts_count": 30,
        "description": "Create SEO-optimized content that Google loves. This pack includes 30 prompts for keyword research, outline generation, article writing, meta descriptions, and content optimization.",
    },
    {
        "id": "real_estate",
        "title": "Real Estate AI Prompt Bundle",
        "tagline": "Close more deals with AI-powered listing descriptions & scripts",
        "niche": "Real Estate",
        "prompts_count": 25,
        "description": "Stand out in a competitive market. This bundle of 25 ChatGPT prompts helps agents write compelling listing descriptions, social media posts, email scripts, and client communication templates.",
    },
    {
        "id": "freelance",
        "title": "Freelancer's ChatGPT Prompt Kit",
        "tagline": "Win more clients and deliver faster with AI",
        "niche": "Freelancing",
        "prompts_count": 40,
        "description": "40 essential ChatGPT prompts every freelancer needs. Write winning proposals, professional emails, client contracts, portfolio descriptions, and social proof content in half the time.",
    },
    {
        "id": "business",
        "title": "Business AI Prompts: Strategy & Operations",
        "tagline": "Make smarter business decisions with AI-powered analysis",
        "niche": "Business",
        "prompts_count": 30,
        "description": "Run your business like a CEO. This pack of 30 ChatGPT prompts covers business strategy, financial analysis, competitor research, operational planning, and decision-making frameworks.",
    },
    {
        "id": "content_creation",
        "title": "Content Creator AI Prompt Pack",
        "tagline": "Never run out of content ideas again",
        "niche": "Content Creation",
        "prompts_count": 35,
        "description": "Whether you're a YouTuber, podcaster, or blogger, this pack of 35 ChatGPT prompts helps you brainstorm topics, write scripts, create thumbnails, and repurpose content across platforms.",
    },
    {
        "id": "ecommerce",
        "title": "E-Commerce AI Prompts for Shopify Sellers",
        "tagline": "Boost sales with product descriptions that sell",
        "niche": "E-Commerce",
        "prompts_count": 25,
        "description": "Scale your Shopify store with AI. This pack of 25 ChatGPT prompts helps you write irresistible product descriptions, optimize listings, create email flows, and handle customer service faster.",
    },
    {
        "id": "blogging",
        "title": "Blogging AI Prompts: Write Posts That Rank",
        "tagline": "Publish high-quality blog posts 5x faster",
        "niche": "Blogging",
        "prompts_count": 30,
        "description": "Grow your blog without burning out. This pack includes 30 ChatGPT prompts for topic research, outline creation, writing engaging introductions, structuring posts, and optimizing for SEO.",
    },
]


def _groq_json(prompt, max_tokens=2000):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")
    payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.8,
    }).encode()
    req = urllib.request.Request(
        GROQ_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        result = json.loads(resp.read().decode())
    return result["choices"][0]["message"]["content"]


def generate_prompts(template, count=25):
    prompt_text = f"""You are a professional prompt engineer. Create {count} high-quality ChatGPT prompts for: {template['title']}.

Each prompt must be practical, specific, and ready to copy-paste into ChatGPT.

**Format:** Return a JSON array of objects ONLY (no markdown, no explanation):
[
  {{"category": "Category Name", "prompt": "The actual prompt text...", "use_case": "When to use this prompt"}},
  ...
]

Categories to cover: at least 5 different categories relevant to {template['niche']}.

Rules:
- Prompts must be in English
- Each prompt must be at least 1-2 sentences
- Make them specific, actionable, and professional
- Cover different aspects of {template['niche']}
- NO placeholders like [brackets] — use realistic examples instead"""
    for attempt in range(3):
        try:
            result = _groq_json(prompt_text, max_tokens=3000)
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                result = result.split("```")[1].split("```")[0]
            result = result.strip()
            prompts = json.loads(result)
            if isinstance(prompts, dict) and "prompts" in prompts:
                prompts = prompts["prompts"]
            if isinstance(prompts, list) and len(prompts) >= 5:
                return prompts
        except Exception as e:
            print(f"  Attempt {attempt+1} failed, retrying...")
    print(f"  Error generating prompts after 3 attempts")
    return []


def generate_pdf_content(template, prompts):
    now = datetime.now().strftime("%B %d, %Y")
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  {template['title']}")
    lines.append(f"  {template['tagline']}")
    lines.append(f"{'='*60}")
    lines.append(f"")
    lines.append(f"Included Prompts: {len(prompts)}")
    lines.append(f"Generated: {now}")
    lines.append(f"")
    lines.append(f"{'='*60}")
    lines.append(f"  HOW TO USE")
    lines.append(f"{'='*60}")
    lines.append(f"")
    lines.append(f"1. Copy a prompt below")
    lines.append(f"2. Paste into ChatGPT (or any AI chat)")
    lines.append(f"3. Replace the example details with your own")
    lines.append(f"4. Get professional results in seconds")
    lines.append(f"")
    lines.append(f"{'='*60}")
    lines.append(f"  THE PROMPTS")
    lines.append(f"{'='*60}")
    lines.append(f"")

    categories = {}
    for p in prompts:
        cat = p.get("category", "General")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    for cat, cat_prompts in categories.items():
        lines.append(f"")
        lines.append(f"  {'='*56}")
        lines.append(f"  {cat.upper()}")
        lines.append(f"  {'='*56}")
        lines.append(f"")
        for i, p in enumerate(cat_prompts, 1):
            lines.append(f"  Prompt #{i}: {p.get('use_case', cat)}")
            lines.append(f"  {'─'*56}")
            lines.append(f"  {p['prompt']}")
            lines.append(f"")

    lines.append(f"{'='*60}")
    lines.append(f"  Thank you for your purchase!")
    lines.append(f"  Share your results: @yourhandle")
    lines.append(f"{'='*60}")
    return "\n".join(lines)


def create_cover_svg(template, price):
    gradient_from = random.choice(["#667eea", "#764ba2", "#f093fb", "#4facfe", "#43e97b", "#fa709a", "#a18cd1", "#fbc2eb"])
    gradient_to = random.choice(["#764ba2", "#667eea", "#f5576c", "#00f2fe", "#38f9d7", "#fee140", "#fbc2eb", "#a18cd1"])
    title_color = "#fff" if "a" in gradient_from else "#1a1a2e"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 560">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{gradient_from}"/>
      <stop offset="100%" style="stop-color:{gradient_to}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="560" fill="url(#bg)" rx="10"/>
  <text x="200" y="80" text-anchor="middle" font-family="Arial,sans-serif" font-size="22" font-weight="bold" fill="{title_color}">AI Prompt Pack</text>
  <text x="200" y="120" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="{title_color}" opacity="0.9">{template['niche']}</text>
  <line x1="50" y1="140" x2="350" y2="140" stroke="{title_color}" stroke-width="1" opacity="0.3"/>
  <text x="200" y="240" text-anchor="middle" font-family="Arial,sans-serif" font-size="26" font-weight="bold" fill="{title_color}">{template['title'].replace('ChatGPT Prompts for ', '').replace('AI Prompts for ', '').replace('ChatGPT Prompts ', '').replace('AI Prompt ', '').replace(' Prompt', '').replace(' Bundle', '').replace(' Pack', '').replace(' Kit', '').replace(' System', '')}</text>
  <text x="200" y="320" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="{title_color}" opacity="0.8">{template['tagline']}</text>
  <circle cx="200" cy="400" r="50" fill="none" stroke="{title_color}" stroke-width="2" opacity="0.3"/>
  <text x="200" y="395" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" font-weight="bold" fill="{title_color}">{template.get('prompts_count', 25)}</text>
  <text x="200" y="418" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="{title_color}" opacity="0.8">PROMPTS</text>
  <text x="200" y="500" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="{title_color}">${price}</text>
  <text x="200" y="530" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="{title_color}" opacity="0.6">Instant Digital Download · PDF + TXT</text>
</svg>"""


def save_prompt_pack(template, prompts, text_content, svg):
    os.makedirs(PRODUCTS_DIR, exist_ok=True)
    slug = template["id"]
    pack_dir = os.path.join(PRODUCTS_DIR, slug)
    os.makedirs(pack_dir, exist_ok=True)
    pdf_path = os.path.join(pack_dir, f"{slug}-prompts.txt")
    with open(pdf_path, "w", encoding="utf-8") as f:
        f.write(text_content)
    cover_path = os.path.join(pack_dir, "cover.svg")
    with open(cover_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return {
        "title": template["title"],
        "tagline": template["tagline"],
        "niche": template["niche"],
        "id": slug,
        "price": PRODUCT_PRICES.get(slug, 9),
        "prompts_count": len(prompts),
        "description": template["description"],
        "text_file": f"products/{slug}/{slug}-prompts.txt",
        "cover_file": f"products/{slug}/cover.svg",
        "prompts": prompts,
    }


def research_trending_niche():
    prompt = """You are a market research expert. Analyze current digital product trends for 2025-2026 and suggest ONE specific, high-demand niche for a ChatGPT prompt pack.

Rules:
- Niche must be in high demand right now (e.g., AI video generation, no-code development, TikTok shop, etc.)
- Must be DIFFERENT from these niches: copywriting, social media, email marketing, SEO, real estate, freelance, business strategy, content creation, ecommerce, blogging
- Target audience must be willing to pay $9-14 for a prompt pack

Return ONLY a JSON object (no markdown, no explanation):
{
  "id": "unique_slug",
  "title": "ChatGPT Prompts for [Niche]",
  "tagline": "Short compelling tagline in English",
  "niche": "Category name",
  "prompts_count": 30,
  "description": "Compelling 2-sentence description of what the pack helps with"
}"""

    result = _groq_json(prompt, max_tokens=800)
    if "```json" in result:
        result = result.split("```json")[1].split("```")[0]
    elif "```" in result:
        result = result.split("```")[1].split("```")[0]
    result = result.strip()
    template = json.loads(result)
    if not all(k in template for k in ("id", "title", "tagline", "niche", "prompts_count", "description")):
        raise ValueError("Incomplete template from AI")
    print(f"  Trend -> {template['title']} ({template['niche']})")
    return template


def generate_batch(count=None):
    if count is None:
        count = DAILY_OUTPUT
    products = []
    fixed_count = max(0, count - 1)
    available = [t for t in PRODUCT_TEMPLATES]
    random.shuffle(available)
    selected = available[:fixed_count]
    if count > 0:
        try:
            print("Researching trending niche...")
            trend_template = research_trending_niche()
            selected.append(trend_template)
        except Exception as e:
            print(f"  Trend research failed: {e}. Using fixed template instead.")
            fallback = [t for t in PRODUCT_TEMPLATES if t not in selected]
            selected.append(fallback[0] if fallback else available[0])
    for i, template in enumerate(selected):
        print(f"Generating product {i+1}/{len(selected)}: {template['title']}...")
        prompts = generate_prompts(template, template.get("prompts_count", 25))
        if not prompts or len(prompts) < 5:
            print(f"  FAIL: Could not generate prompts")
            continue
        price = PRODUCT_PRICES.get(template["id"], 12)
        text_content = generate_pdf_content(template, prompts)
        svg = create_cover_svg(template, price)
        product = save_prompt_pack(template, prompts, text_content, svg)
        products.append(product)
        print(f"  OK: {product['title']} — {len(prompts)} prompts, ${price}")
    return products
