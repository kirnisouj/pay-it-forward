from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)

donors = {
    "John S.": 25
}

@app.route('/')
def index():
    return render_template('index.html', no_back=True)

@app.route('/donate', methods=['POST'])
def donate():
    return render_template('pay_it_forward.html', donor="John S.", amount=donors["John S."], show_envelope=True, no_back=True)

@app.route('/redeem', methods=['POST'])
def redeem():
    nonprofit = request.form.get('nonprofit')
    return render_template('pay_forward.html', allocated_to=nonprofit, amount=donors["John S."], no_back=True)

@app.route('/pay_forward', methods=['POST'])
def pay_forward():
    amount = request.form.get('amount')
    return render_template('thank_you.html', allocated_to=f'Paid Forward: ${amount}', amount=amount, no_back=True)

@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
   
    amount = request.form.get('amount', '25.99')
    
    card_type = "VISA"
    last4 = "0759"
    address_line1 = "5855 Wadsworth Bypass, Unit A"
    city = "Arvada"
    state = "CO"
    zip_code = "80003"
    country = "USA"

    return render_template('confirm_payment.html',
                           amount=amount,
                           card_type=card_type,
                           last4=last4,
                           address_line1=address_line1,
                           city=city,
                           state=state,
                           zip_code=zip_code,
                           country=country)



@app.route('/thank_you', methods=['POST'])
def thank_you():
    message = request.form.get('message')
    return render_template('thank_you.html', message=message, no_back=True)

@app.route('/email_confirmation', methods=['POST'])
def email_confirmation():
    message = request.form.get('message')
    return render_template('email_confirmation.html', message=message, no_back=True)

@app.route('/get_nonprofits', methods=['GET'])
def get_nonprofits():
    nonprofits = ["Step Denver", "Colorado Gives", "Another Nonprofit"]
    return jsonify(nonprofits=nonprofits)

@app.after_request
def prevent_back(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the port Render provides
    app.run(host="0.0.0.0", port=port, debug=True)

# Frontend Templates

# Updated with Colorado Gives Foundation design elements

# templates/style.css
style_css = '''
body {
    font-family: 'Arial', sans-serif;
    background-color: #f8f9fa;
    text-align: center;
    margin: 0;
    padding: 0;
    overscroll-behavior: none;
}
.container {
    width: 50%;
    margin: auto;
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
.btn {
    background-color: #0077cc;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-size: 16px;
    text-transform: uppercase;
    font-weight: bold;
    transition: all 0.3s;
}
.btn:hover {
    background-color: #005fa3;
}
.dropdown, input[type='number'] {
    padding: 10px;
    width: 100%;
    margin-top: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

/* Prevent back navigation */
<script>
    window.onload = function () {
        history.pushState(null, null, document.URL);
    };
    window.onpopstate = function () {
        history.pushState(null, null, document.URL);
    };
</script>
''' 

# Save CSS template

def save_static_files():
    static_files = {
        "static/style.css": style_css,
    }
    for filename, content in static_files.items():
        with open(filename, "w") as f:
            f.write(content)

if __name__ == "__main__":
    save_static_files()
    app.run(debug=True)