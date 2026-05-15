import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
ACCESS_TOKEN = "EAAVDidZBZB58gBRczzjPejFryksHl614c7KMmaPBsLj9iu4WdGh5l9FHVJUrwHE6n1pJCShnyY9Gy6wo19ulQt2ZBRanhFFw9mU4dy9ZCr2f3Erntr9ZCRXIhjUaRzDSrUImdHoqlGjcNZCZBsSgZCRueyBFTMuZA5owiYDOtgxsZBytgkjH3xuAZBFQoDLgeGBWRNxCtMa75QOJVGyRj0iCaDhPdiDK69vtRg2ZASHm0TlniN3yhEpqrgZDZD"
PHONE_NUMBER_ID = "1015857034952741"
VERIFY_TOKEN = "luxurys_ghana_secure_token_123"

# --- KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "about": "Luxurys is a bedding and fragrance brand focused on custom-made products for homes. 🏠✨",
    "products": "We specialize in:\n- Bedsheets 🛏️\n- Duvets and covers ☁️\n- Pillows 😴\n- Bathroom mats 🛁\n- Perfumes and diffusers 🌸",
    "price": "Our prices are custom based on size and fabric. Typical ranges:\n- Bedsheets: GHS 250 - 800+\n- Duvets: GHS 400 - 1,200+\n- Pillows: GHS 80 - 300\n- Fragrances: GHS 100 - 500+\n\nFinal prices are confirmed after your order details!",
    "custom": "Yes! You can choose your own size, color, fabric, and design for a truly personalized touch. 🎨",
    "delivery": "Yes, we deliver nationwide across Ghana! 🇬🇭\n\n💡 Tip: To reduce delivery costs, pick the branch closest to you before ordering.",
    "branches": "We have branches in:\n📍 Accra, Kumasi, Tamale, Takoradi, Sunyani, Madina, and Nungua.",
    "order": "To place an order:\n1. Select your nearest branch.\n2. Choose your product.\n3. Confirm specifications (size/color).\n4. Get your final price & pay.",
    "return": "Please contact the specific branch where you placed your order; they handle returns on a case-by-case basis.",
    "quality": "Luxurys stands out because of our custom sizing, premium materials, and personalized scent options. 💎"
}

def send_whatsapp_message(recipient_id, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    data = request.get_json()
    try:
        if "messages" in data["entry"][0]["whatsapp"]:
            message = data["entry"][0]["whatsapp"]["messages"][0]
            recipient_id = message["from"]
            text = message["text"]["body"].lower()

            response_text = "I'm not sure about that. Would you like to know about our products, pricing, or how to order? 😊"
            
            if any(word in text for word in ["who", "what", "about", "company"]):
                response_text = KNOWLEDGE_BASE["about"]
            elif any(word in text for word in ["product", "sell", "list", "items"]):
                response_text = KNOWLEDGE_BASE["products"]
            elif any(word in text for word in ["price", "cost", "how much", "range"]):
                response_text = KNOWLEDGE_BASE["price"]
            elif any(word in text for word in ["custom", "design", "color", "size"]):
                response_text = KNOWLEDGE_BASE["custom"]
            elif any(word in text for word in ["delivery", "ship", "deliver"]):
                response_text = KNOWLEDGE_BASE["delivery"]
            elif any(word in text for word in ["branch", "location", "where", "city"]):
