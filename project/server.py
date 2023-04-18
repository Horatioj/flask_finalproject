import os
from flask import Flask, redirect, request, Blueprint, url_for, render_template, jsonify

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51Mxi9uGGlgefyoZtkNi1KF4iPxWK4FapGJphvmxxftZrB7RrPvnrNv4b7NHuWUZh6hTtHhioHJLvVGfUuUsRuzgO00NqtPatGR'
# stripe.PaymentIntent.create(payment_method_types=["alipay"], amount=8.8, currency='hkd')
server = Blueprint('server', __name__)
YOUR_DOMAIN = 'http://localhost:5000'

@server.route('/create-checkout-session', methods=['POST', 'GET'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1MxiR5GGlgefyoZtlh1Vpmir',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + url_for('server.success'),
            cancel_url=YOUR_DOMAIN + url_for('server.cancel'),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@server.route('/success')
def success():
    return render_template('success.html')

@server.route('/cancel')
def cancel():
    return render_template('cancel.html')

@server.route('/secret')
def secret():
    intent = 123 # ... Create or retrieve the PaymentIntent
    return jsonify(client_secret=intent.client_secret)