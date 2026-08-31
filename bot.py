import os
from flask import Flask, request
from telegram import Bot

app = Flask(__name__)

# توكن بوتك الخاص المعتمد
TOKEN = "8678385689:AAGJPXQdubsvmmw9fhujZ3k2YZVe-7_6D8Q"
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return "Golden Box Bot is running successfully!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json or request.data.decode('utf-8')
        # الحصول على معرف الشات أو استخدام رقم افتراضي إذا لم يتم تحديده
        # يمكنك تعديل رقم الشات لاحقاً أو جعله يستقبل رسالة عامة
        chat_id = request.args.get('chat_id') 
        
        if chat_id and data:
            bot.send_message(chat_id=chat_id, text=str(data))
            return "Sent successfully", 200
        else:
            return "Missing chat_id or data", 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
