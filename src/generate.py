import json
import os
import random
import urllib.request
import urllib.error
from config import GROQ_API_KEY, DESIGN_CATEGORIES, DESIGNS_DIR, DAILY_OUTPUT

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SVG_TEMPLATES = {
    "Minimalist Logo": "Create a minimalist SVG logo design. Simple shapes, clean lines, centered composition. Style: modern, flat, single color or two colors maximum.",
    "Typography Quote": "Create an SVG typography design featuring an inspirational quote in an artistic layout. Creative text arrangement, modern serif or sans-serif styling.",
    "Geometric Pattern": "Create an SVG geometric pattern design. Symmetrical shapes, polygons, mandala-like composition, repeating patterns. Suitable for t-shirt print.",
    "Nature & Outdoors": "Create an SVG nature-themed design. Mountains, trees, sun, moon, or landscape elements. Outdoor adventure style, clean silhouettes.",
}


def generate_svg_design(category=None):
    if not category:
        category = random.choice(DESIGN_CATEGORIES)
    prompt = SVG_TEMPLATES.get(category, SVG_TEMPLATES["Minimalist Logo"])
    title_prompt = f"Suggest a short creative title (max 5 words) for an SVG t-shirt design based on: {category}. Return ONLY the title, no quotes."
    try:
        title = _groq_chat(title_prompt, max_tokens=20)
        title = title.strip().strip('"').strip("'").strip()
        design_prompt = f"{prompt}\n\nGenerate a clean SVG file (code only, no markdown) for a t-shirt print design.\nTitle: {title}\nCategory: {category}\n\nRequirements:\n- Return ONLY valid SVG code, no explanations\n- ViewBox: 0 0 400 400\n- Max 3 colors, clean and print-friendly\n- Scale well for t-shirt printing\n- Arabic and English text if applicable\n- Do NOT wrap in svg codeblock or markdown"
        svg_code = _groq_chat(design_prompt, max_tokens=2000)
        svg_code = _clean_svg(svg_code)
        if not svg_code or "<svg" not in svg_code:
            return None
        tags = _generate_tags(category, title)
        return {"title": title, "category": category, "svg": svg_code, "tags": tags, "description": f"Premium {category.lower()} SVG design: {title}. Perfect for t-shirts, mugs, posters and more. Instant digital download."}
    except Exception as e:
        print(f"Error generating design: {e}")
        return None


def _groq_chat(prompt, max_tokens=1000):
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
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
    return result["choices"][0]["message"]["content"]


def _clean_svg(code):
    if "```svg" in code:
        code = code.split("```svg")[1]
        if "```" in code:
            code = code.split("```")[0]
    elif "```" in code:
        code = code.split("```")[1]
        if "```" in code:
            code = code.split("```")[0]
    code = code.strip()
    return code


def _generate_tags(category, title):
    base = ["svg", "print", "design", "digital download", "t-shirt", category.lower().replace(" ", "-")]
    words = title.lower().split()
    return list(set(base + words))


def save_design(design):
    os.makedirs(DESIGNS_DIR, exist_ok=True)
    filename = design["title"].lower().replace(" ", "-").replace("/", "-")[:30]
    filepath = os.path.join(DESIGNS_DIR, f"{filename}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(design["svg"])
    design["file_path"] = filepath
    design["file_name"] = f"{filename}.svg"
    return design


def generate_batch(count=None):
    if count is None:
        count = DAILY_OUTPUT
    designs = []
    for i in range(count):
        print(f"Generating design {i+1}/{count}...")
        design = generate_svg_design()
        if design:
            design = save_design(design)
            designs.append(design)
            print(f"  OK: {design['title']}")
        else:
            print(f"  FAIL: Design {i+1} failed")
    return designs
