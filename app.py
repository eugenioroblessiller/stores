from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My store",
        "items": [
            {"name": "chair", "price": 15.99}
        ]
    }
]


@app.route("/stores")
def get_stores():
    return {"stores": stores}


@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store was not found"}, 404


@app.route("/store/<string:name>/item", methods=["GET"])
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store was not found"}, 404


@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store was not found"}, 404


if __name__ == "__main__":
    app.run(port=5001, debug=True)
