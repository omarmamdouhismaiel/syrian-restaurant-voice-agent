# backend/api.py
from flask import Flask, request, jsonify
import uuid
import json

app = Flask(__name__)
orders = []

@app.route("/submit-order", methods=["POST"])
def submit_order():
    data = request.get_json()
    name = data.get("name")
    order_list = data.get("order")

    order_id = str(uuid.uuid4())[:8]
    eta = "15 minutes"

    order_entry = {
        "id": order_id,
        "name": name,
        "order": order_list,
        "eta": eta
    }
    orders.append(order_entry)

    # Optional: Save to JSON
    with open("orders.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

    return jsonify({"order_id": order_id, "eta": eta})
