import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your Paystack API secret key
PAYSTACK_SECRET_KEY = 'your_paystack_secret_key'

# Replace with your business details
BUSINESS_NAME = 'Your Business Name'
BUSINESS_EMAIL = 'brainyshanhoops@gmail.com'  # Default email
BUSINESS_PHONE = 'your_phone_number'  # Replace with your phone number

# Install necessary libraries
try:
    import requests
    from flask import Flask, request, jsonify
except ImportError:
    print("Please install the required libraries using 'pip install requests flask'")

@app.route('/pay', methods=['POST'])
def initiate_payment():
    try:
        data = request.get_json()

        # Retrieve user's phone number from the request
        user_phone = data['phone']

        # Replace with your desired payment amount
        amount = 100.00  # Replace with the actual amount you want to charge

        # Create a Paystack customer
        customer_data = {
            "email": BUSINESS_EMAIL,
            "phone": BUSINESS_PHONE,
            "first_name": BUSINESS_NAME,
            "last_name": "Customer",
        }
        customer_response = requests.post(
            'https://api.paystack.co/customer', json=customer_data, headers={'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'}
        )

        if customer_response.status_code == 201:
            customer_id = customer_response.json()['data']['customer_code']

            # Initialize a transaction
            transaction_data = {
                "customer": customer_id,
                "amount": amount * 100,  # Amount in pesewas (100 pesewas = 1 GHS)
                "currency": "GHS",
                "channels": ["mobile_money"],
                "reference": "your_unique_reference",  # Replace with your unique reference
            }
            transaction_response = requests.post(
                'https://api.paystack.co/transaction/initialize', json=transaction_data, headers={'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'}
            )

            if transaction_response.status_code == 201:
                authorization_url = transaction_response.json()['data']['authorization_url']
                return jsonify({'payment_url': authorization_url})
            else:
                return jsonify({'error': 'Failed to initialize payment'}), 500
        else:
            return jsonify({'error': 'Failed to create customer'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
