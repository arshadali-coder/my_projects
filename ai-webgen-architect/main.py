from flask import Flask, render_template, request
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

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
        gemini_prompt = f"""Generate a complete, single-file advanced frontend web application in pure HTML.
Include embedded CSS (within <style>) and JavaScript (within <script>).
The output must be self-contained, without external files (except for linked fonts or libraries).

✅ Design Requirements:

Use Tailwind CSS via CDN: <script src="https://cdn.tailwindcss.com"></script>

Use a Google Font M PLUS Rounded 1c - <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700&display=swap" rel="stylesheet">

Layout must be modern, responsive, and aesthetically vibrant using a funky Gen-Z color scheme.

Build layout using advanced CSS Grid / Flexbox (with overlapping elements, layered sections, etc.).

Add smooth animations & transitions with easing like ease-in-out or cubic-bezier on hover, scroll, click, etc.

⚙️ Functional Features:
A responsive image slider/carousel with swipe/autoplay.

Expandable/collapsible sections (like FAQs or descriptions).

Interactive forms with real-time validation/feedback.

Dynamic UI updates using JavaScript for better interactivity.

🧠 Technical Note:
This project is built using vanilla JavaScript only, without frameworks like React or Next.js.
This ensures:

Faster loading with zero build setup.

Full control over the DOM.

Easy embedding and portability as a single HTML file.

🎨 Optional Enhancements based on purpose:
Theme toggle (light/dark mode)

Parallax scrolling

Lottie animations

Page loader or progress bar

🖼️ Images:
Use descriptive placeholder images from:
https://placehold.co/{{width}}x{{height}}/{{bg_hex}}/{{text_hex}}?text={{text}}
if no inline images are provided.

❌ Restrictions:
Do not include any branding, credits, watermarks, or mentions of “Arshad Ali”.

Do not include any markdown, comments, or explanations — only raw HTML code.

🔧 Purpose:
{user_requirement}"""

        response = genai.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    contents=gemini_prompt
        )

        raw_html = response.text
        cleaned_html = clean_gemini_output(raw_html)
        print("Raw HTML:", raw_html)
        print("Cleaned HTML:", cleaned_html)
        
        os.makedirs(STATIC_DIR, exist_ok=True)

        with open(os.path.join(STATIC_DIR, "generated_site.html"), "w", encoding="utf-8") as f:
            f.write(cleaned_html)

    show_iframe = os.path.exists(f"{STATIC_DIR}/generated_site.html")
    return render_template("trial.html", show_iframe=show_iframe)

if __name__ == "__main__":
    app.run(debug=True,)
