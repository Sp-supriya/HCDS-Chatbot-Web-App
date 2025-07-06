from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Company Content
RESPONSES = {
    "Main Menu": {
        "text": "👋 Welcome to **HCDS Technologies** Chatbot!\nHow can I help you today?",
        "options": ["About Us", "Services", "Careers", "News/Updates", "Contact"]
    },
    "About Us": {
        "text": "💼 **About HCDS Technologies**\nWe are an IT services company delivering innovative software solutions, AI/ML consulting, and digital transformation for clients worldwide.",
        "options": ["Services", "Careers", "News/Updates", "Contact", "Home"]
    },
    "Services": {
        "text": "🛠️ **Our Services**\n- Software Development\n- AI/ML Consulting\n- Data Analytics\n- Cloud Solutions\n- Enterprise IT Consulting",
        "options": ["About Us", "Careers", "News/Updates", "Contact", "Home"]
    },
    "Careers": {
        "text": "📑 **Careers at HCDS**\nWe’re hiring talented engineers, analysts, and consultants.\nApply at: careers@hcdstech.in",
        "options": ["About Us", "Services", "News/Updates", "Contact", "Home"]
    },
    "News/Updates": {
        "text": "📰 **Latest News from HCDS**\n- Expanding our Hyderabad office.\n- New partnership for AI solutions.\n- Recent client success in cloud migration projects.",
        "options": ["About Us", "Services", "Careers", "Contact", "Home"]
    },
    "Contact": {
        "text": "📞 **Contact Us**\nPhone: +91-XXXXXXXXXX\nEmail: info@hcdstech.in\nWebsite: www.hcdstech.in",
        "options": ["About Us", "Services", "Careers", "News/Updates", "Home"]
    }
}

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>HCDS Technologies Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f7f7; margin: 0; }
        .chat-container { max-width: 800px; margin: 30px auto; background: #fff; border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);}
        .header { background-color: #10a37f; color: white; padding: 20px; text-align: center; font-size: 1.5em;}
        .messages { padding: 20px; max-height: 600px; overflow-y: auto;}
        .message { margin: 10px 0; padding: 12px 18px; border-radius: 20px; display: inline-block; max-width: 80%; }
        .user { background-color: #dcf8c6; float: right; clear: both; }
        .bot { background-color: #f1f0f0; float: left; clear: both; white-space: pre-wrap;}
        form { padding: 20px; border-top: 1px solid #eee; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;}
        button { padding: 10px 20px; background-color: #10a37f; color: white; border: none;
            border-radius: 20px; cursor: pointer; flex: 1 1 auto; min-width: 120px;}
        button:hover { background-color: #0d8a6c;}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">🤖 HCDS Tech Assistant</div>
        <div class="messages">
            {% for role, text in chat_history %}
                <div class="message {{ role }}">{{ text }}</div>
            {% endfor %}
        </div>
        {% if options %}
        <form method="post">
            {% for option in options %}
                <button name="user_choice" value="{{ option }}">{{ option }}</button>
            {% endfor %}
        </form>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []
        session["last_options"] = RESPONSES["Main Menu"]["options"]
        session["chat_history"].append(("bot", RESPONSES["Main Menu"]["text"]))

    if request.method == "POST":
        user_choice = request.form.get("user_choice")
        if user_choice:
            session["chat_history"].append(("user", user_choice))
            reply_data = RESPONSES.get(user_choice, RESPONSES["Main Menu"])
            session["chat_history"].append(("bot", reply_data["text"]))
            session["last_options"] = reply_data["options"]
            session.modified = True
        return redirect(url_for("chat"))

    return render_template_string(HTML_TEMPLATE,
                                  chat_history=session["chat_history"],
                                  options=session["last_options"])

if __name__ == "__main__":
    app.run(debug=True)
