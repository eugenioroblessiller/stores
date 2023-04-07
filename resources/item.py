import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except:
            abort(404, message="Item not found")

    def put(self):
        pass

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"Item: {item_id} has been deleted"}
        except:
            abort(400, message="Error deleting item")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"stores": list(items.values())}

    def post(self):
        pass
