from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY in .env file.")

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Initialize Groq LLM
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7,
    max_tokens=150,
    api_key=GROQ_API_KEY,
)

# Assistant prompt setup
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a warm, humorous, validating mental health assistant. Keep replies under 30 words."),
    ("human", "{input}")
])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/games")
def games():
    return render_template("game.html")

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_msg = request.form["msg"]
        chain = prompt | llm
        response = chain.invoke({"input": user_msg})
        return jsonify({"response": response.content})
    except Exception as e:
        return jsonify({"response": "Oops! Something went wrong. But I'm still here for you 💛"})

@app.route("/emoji-game")
def emoji_game():
    return render_template("emoji_game.html")

@app.route("/bubble-shooter")
def bubble_shooter():
    return render_template("bubble_shooter.html")

@app.route("/word-match")
def word_match():
    return render_template("word_match.html")

# 💫 Interpret season essence
def season_traits(season):
    return {
        "spring": "new beginnings and tender hopes",
        "summer": "radiant energy and creative fire",
        "autumn": "deep reflection and artistic spirit",
        "winter": "quiet wisdom and soft introspection"
    }.get(season, "a beautiful mystery")

# 🎨 Translate color hex to emotion
def color_feeling(color_code):
    return {
        "#ffcccc": "a gentle blush of softness and compassion",
        "#add8e6": "a sky-touched spirit full of calm and dreams",
        "#90ee90": "a fresh bloom of peace and renewal",
        "#f4a261": "a warm hug of earthy optimism",
        "#d291bc": "a poetic soul wrapped in lavender dusk",
        "#ffffff": "a quiet openness, pure and full of possibility"
    }.get(color_code.lower(), "a mystery hue that makes you uniquely you")

@app.route("/personality-check", methods=["GET", "POST"])
def personality_check():
    vibe = None
    surprise = None

    if request.method == "POST":
        color = request.form.get("color", "#ffffff")
        season = request.form.get("season", "unknown")
        food = request.form.get("food", "unknown")
        sound = request.form.get("sound", "silence")
        word = request.form.get("word", "peace").lower()

        # 📝 Vibe output (no raw hex code shown)
        vibe = f"""
        🎨 Your color reflects {color_feeling(color)}.<br>
        🍃 You are drawn to {season}, a season of {season_traits(season)}.<br>
        🍽️ Your comfort food is {food}, which speaks of how you nurture your inner self.<br>
        🎵 The sound of {sound} calms you — a mirror to your inner rhythm.<br>
        💬 “{word}” is your soul’s whisper today — hold it close like a sacred note.
        """

        # 🎁 Surprise messages
        surprises = [
            "💌 You are allowed to take up space. Breathe deep.",
            "🌙 Rest is not laziness — it’s sacred.",
            "🕯️ You carry a quiet strength that lights rooms.",
            "🌼 Bloom slow. The wildflowers do.",
            "📖 Write down something lovely about yourself today.",
            "🎨 Create for joy, not perfection.",
            "🌈 You’re not behind — you’re on your own path.",
            "🍵 Go drink some water and stretch. Your body thanks you.",
            "🧩 You're made of stardust and stumbles. Both are divine.",
            "🌻 Some days you shine, some days you root. Both matter."
        ]
        surprise = random.choice(surprises)

    return render_template("personality-check.html", vibe=vibe, surprise=surprise)

if __name__ == "__main__":
    app.run(debug=True)
