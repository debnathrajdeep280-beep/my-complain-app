from flask import Flask, render_template, request, redirect, url_for
import urllib.parse
import os  # <-- Step 1: os library ko yahan import kiya

app = Flask(__name__)

# Data store karne ke liye temporary dicts aur lists
global_users_db = {}
global_complains_db = []

# ⚠️ APNA WHATSAPP NUMBER YAHAN DALEIN
YOUR_WHATSAPP_NUMBER = "918415015059" 

current_logged_in_email = None

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    global current_logged_in_email
    email = request.form.get('email')
    current_logged_in_email = email
    
    global_users_db[email] = {
        "name": request.form.get('name'),
        "phone": request.form.get('phone'),
        "state": request.form.get('state'),
        "district": request.form.get('district'),
        "address": request.form.get('address'),
        "pincode": request.form.get('pincode'),
        "password": request.form.get('password')
    }
    print(f"\n[DATABASE SUCCESS] User Registered via Email: {email}")
    return redirect(url_for('complain_page'))

@app.route('/complain')
def complain_page():
    return render_template('complain.html')

@app.route('/submit-complain', methods=['POST'])
def submit_complain():
    global current_logged_in_email
    headline = request.form.get('headline')
    language = request.form.get('language')
    complain_text = request.form.get('complain_text')
    
    user_info = global_users_db.get(current_logged_in_email, {
        "name": "Unknown User", "phone": "N/A", "state": "N/A", 
        "district": "N/A", "address": "N/A", "pincode": "N/A"
    })
    
    global_complains_db.append({
        "headline": headline, "language": language, 
        "text": complain_text, "user_email": current_logged_in_email
    })
    
    whatsapp_msg = (
        f"📝 *NEW COMPLAIN RECEIVED*\n\n"
        f"👤 *USER DETAILS:*\n"
        f"▪️ *Naam:* {user_info['name']}\n"
        f"▪️ *Mobile:* {user_info['phone']}\n\n"
        f"📍 *LOCATION:*\n"
        f"▪️ *State:* {user_info['state']}\n"
        f"▪️ *District:* {user_info['district']}\n"
        f"▪️ *PIN Code:* {user_info['pincode']}\n\n"
        f"📋 *COMPLAIN:*\n"
        f"▪️ *Headline:* {headline}\n"
        f"▪️ *Message:* {complain_text}"
    )
    
    encoded_msg = urllib.parse.quote(whatsapp_msg)
    whatsapp_url = f"https://wa.me/{YOUR_WHATSAPP_NUMBER}?text={encoded_msg}"
    
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; text-align: center; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background: white;">
        <h3 style="color: #28a745;">Thank You! Your complain has been registered successfully.</h3>
        <p style="color: #666; margin-bottom: 20px;">Apni shikayat ko WhatsApp par bhejne ke liye niche click karein:</p>
        <a href="{whatsapp_url}" target="_blank" style="display: inline-block; padding: 12px 25px; background-color: #25D366; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">
            💬 Share on WhatsApp
        </a>
    </div>
    """

# <-- Step 1 ka Python badlav yahan hai -->
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
