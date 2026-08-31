import os
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8678385689:AAGJPXQdubsvmmw9fhujZ3k2YZVe-7_6D8Q"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_telegram_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

@app.route('/')
def home():
    return "Golden Box Bot is running successfully!", 200

# استقبال تنبيهات تريدنق فيو
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json or request.data.decode('utf-8')
        chat_id = request.args.get('chat_id')
        
        if chat_id and data:
            message_text = f"🚨 *تنبيه Golden Box*\n\n{str(data)}"
            send_telegram_message(chat_id, message_text)
            return "Sent successfully", 200
        else:
            return "Missing chat_id or data", 400
    except Exception as e:
        return str(e), 500

# استقبال الأوامر من تليجرام
@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    try:
        update = request.get_json()
        if update and "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text == "/start":
                reply = "أهلاً بك يا أبو أحمد! البوت جاهز لاستقبال إشارات التداول والرد على أوامرك."
            else:
                reply = f"وصلتني رسالتك: '{text}'. البوت يعمل بكفاءة لتلقي تنبيهات المؤشر."
                
            send_telegram_message(chat_id, reply)
            
        return "OK", 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
