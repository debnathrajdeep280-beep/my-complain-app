from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. Sabse pehle jab koi website kholega toh Signup page dikhega
@app.route('/')
def home():
    return render_template('signup.html')

# 2. Signup form submit hone par yeh code chalega
@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    print(f"[DATABASE SUCCESS] User Registered via Email: {email}")
    # Registration ke baad yeh user ko seedhe complaint page par bhej dega
    return redirect(url_for('complain'))

# 3. Complaint page kholne ka raasta
@app.route('/complain')
def complain():
    return render_template('complain.html')

# 4. Complaint form submit hone ka sahi raasta (Jo 404 error de raha tha)
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    location = request.form.get('location')
    
    print(f"[NEW COMPLAINT] Title: {title}, Category: {category}, Location: {location}")
    
    # Successful submit hone ke baad screen par yeh message dikhega
    return """
    <div style='text-align: center; margin-top: 50px; font-family: Arial;'>
        <h2 style='color: green;'>Shikayat Safaltapurvak Darj Ho Gayi Hai! ✔</h2>
        <p>Aapki shikayat par jald hi karwayi ki jayegi.</p>
        <br>
        <a href='/complain' style='padding: 10px 20px; background-color: #ff4d4d; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;'>Ek aur shikayat darj karein</a>
    </div>
    """

if __name__ == '__main__':
    # Server chalane ke liye port 10000 set kiya hai jo Render par zaroori hai
    app.run(host='0.0.0.0', port=10000)
