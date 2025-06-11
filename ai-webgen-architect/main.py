from flask import Flask, render_template, request
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

app = Flask(__name__, static_folder='static')

def clean_gemini_output(raw_html):
        lines = raw_html.strip().splitlines()

        # Agar pehli line '''html ya ```html hai, hata do
        if lines[0].strip().lower() in ["'''html", "```html"]:
            lines = lines[1:]

        # Agar last line ''' ya ``` hai, hata do
        if lines and lines[-1].strip() in ["'''", "```"]:
            lines = lines[:-1]

        return "\n".join(lines).strip()

@app.route("/", methods=["GET", "POST"])
def home():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    cleaned_html=""
    if request.method == "POST":
        user_requirement = request.form.get("prompt")
        gemini_prompt = f"""
Generate a complete, well-structured, and **highly advanced** web application in a single HTML file.
Include all necessary HTML, CSS (within <style> tags) and JavaScript (within <script> tags). Ensure the design is **modern, visually stunning, highly responsive across all devices (mobile, tablet, desktop), and aesthetically pleasing with a professional product feel**.

**Prioritize an engaging default background that makes the entire design look cohesive and good.**
**Use funky, vibrant, and contemporary color palettes** that resonate with today's generation's aesthetic.
**Implement sophisticated layouts** using advanced CSS Grid or Flexbox, possibly with overlapping elements, complex section divisions, and innovative spacing.
**Incorporate dynamic animations and transitions** for elements, especially on hover, click, and view changes, using smooth, non-linear easing functions for a fluid user experience.
**Include rich interactive elements**, such as:
- A responsive image carousel/slider with smooth transitions.
- Detailed sections that might have expandable/collapsible content (e.g., FAQs, feature descriptions).
- Interactive forms or input elements with visual feedback.
- Smooth JavaScript interactions for dynamic content loading or user interface updates.

Use Tailwind CSS classes loaded from CDN by including `<script src="https://cdn.tailwindcss.com"></script>` in the head. Use the 'Inter' font.
If any images are provided as inline data, use them directly. If no images are provided, then use descriptive placeholder images from 'https://placehold.co/{{width}}x{{height}}/{{background hex}}/{{text hex}}?text={{text}}'.

**Do NOT include any branding related to "Design with Love From India BY Soumya Sagar" or any associated logo or link.** The generated website should be a clean, standalone product.

Do not include any conversational text, explanations, or markdown fences. Focus solely on the code required to build the website described above.

The website is for {user_requirement}
"""
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents=gemini_prompt
        )

        raw_html = response.text
        cleaned_html = clean_gemini_output(raw_html)
        print("Raw HTML:", raw_html)
        print("Cleaned HTML:", cleaned_html)
        
        os.makedirs(STATIC_DIR, exist_ok=True)

        with open(os.path.join(STATIC_DIR, "generated_site.html"), "w", encoding="utf-8") as f:
            f.write(cleaned_html)

    show_iframe = os.path.exists(f"{STATIC_DIR}/generated_site.html")
    return render_template("index.html", show_iframe=show_iframe)

if __name__ == "__main__":
    app.run(debug=True)
