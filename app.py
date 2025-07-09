from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = '7889097363:AAF1Nu5bxJDqeEDoJzHzdQ3A0rsUvKwg2Hk'
TELEGRAM_CHAT_ID = '8011328234'

# Send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": 8011328234,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print("Telegram Error:", e)
        return False

# --- Route: Location ---
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")
    if not lat or not lon:
        return jsonify({"error": "Missing location"}), 400
    msg = f"📍 *New Location*\nLatitude: {lat}\nLongitude: {lon}"
    send_telegram_message(msg)
    return jsonify({"status": "success"})

# --- Route: Subscription ---
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    message = f"📬 *New Subscription!*\nEmail: {email}"
    if send_telegram_message(message):
        return jsonify({"status": "Subscription sent successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send"}), 500


# --- Route: Callback ---
@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')

    if not all([name, phone]):
        return jsonify({'error': 'Missing data'}), 400

    msg = f"📲 *Callback Request!*\nName: {name}\nPhone: {phone}"
    if send_telegram_message(msg):
        return jsonify({"status": "Callback sent"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send"}), 500

# --- Route: Contact Us ---
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    message = data.get('message')

    if not all([name, email, phone]):
        return jsonify({'error': 'Missing fields'}), 400

    text = f"📞 *New Contact Request!*\nName: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\nMessage: {message}"
    if send_telegram_message(text):
        return jsonify({"status": "Contact message sent"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send"}), 500

if __name__ == '__main__':
    app.run(debug=True)
