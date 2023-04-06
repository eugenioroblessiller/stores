from flask import Flask, request
from flask_smorest import abort

import uuid

from db import items, stores

app = Flask(__name__)


@app.route("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.route("/store/<string:store_id>", methods=["GET"])
def get_store(store_id):
    try:
        return stores[store_id]
    except:
        abort(404, message="Store not found")


@app.route("/store", methods=["POST"])
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.route("/item", methods=["POST"])
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.route("/items", methods=["GET"])
def get_items():
    return {"items": list(items.values())}


@app.route("/tem/<string:item_id>", methods=["GET"])
def get_items_in_store(item_id):
    try:
        return items[item_id]
    except:
        abort(404, message="Store not found")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
