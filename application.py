from flask import Flask, jsonify, request

application = Flask(__name__)

items = [
    {"id": 1, "name": "Cupboard", "price": 5000},
    {"id": 2, "name": "Table", "price": 3500},
    {"id": 3, "name": "Mixer", "price": 2200},
    {"id": 4, "name": "Pan", "price": 900},
]


@application.get("/")
def welcome():
    return jsonify({
        "message": "Python REST API is running!",
        "status": "success",
    })


@application.get("/health")
def health():
    return jsonify({"status": "healthy"})


@application.get("/api/items")
def get_items():
    return jsonify(items)


@application.get("/api/items/<int:item_id>")
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@application.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "name is required"}), 400
    if not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0:
        return jsonify({"error": "price must be a non-negative number"}), 400

    item = {
        "id": max((existing["id"] for existing in items), default=0) + 1,
        "name": name.strip(),
        "price": price,
    }
    items.append(item)
    return jsonify(item), 201


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
