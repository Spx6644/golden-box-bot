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
    return "Golden Box Bot with Webhook & Commands is running successfully!", 200

# مسار استقبال إشارات تريدنق فيو الوب هوك
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json or request.data.decode('utf-8')
        chat_id = request.args.get('chat_id')
        
        if chat_id and data:
            message_text = f"🚨 *تنبيه جديد من مؤشر Golden Box*\n\n{str(data)}"
            send_telegram_message(chat_id, message_text)
            return "Sent successfully", 200
        else:
            return "Missing chat_id or data", 400
    except Exception as e:
        return str(e), 500

# مسار استقبال الأوامر والتفاعل المباشر من تليجرام (Telegram Webhook)
@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    try:
        update = request.get_json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            # الردود التفاعلية والأوامر اللي يطلبها المستخدم
            if text == "/start":
                reply = "أهلاً بك يا أبو أحمد في بوت Golden Box. البوت جاهز لاستقبال إشارات التداول والرد على أوامرك."
            elif text == "/status":
                reply = "🟢 السيرفر يعمل بكفاءة عالية والإشارات متصلة بنجاح."
            elif text.startswith("/search "):
                query = text.replace("/search ", "")
                reply = f"🔍 جاري البحث عن: {query} (قريباً سيتم ربط نتائج التحليل المتقدمة هنا)."
            else:
                reply = f"أهلاً بك! وصلتني رسالتك: '{text}'. أقدر أخدمك بشيء في تحليل اليوم؟"
                
            send_telegram_message(chat_id, reply)
            
        return "OK", 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
