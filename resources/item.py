import uuid
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models import ItemModel
from schemas import ItemSchema, ItemupdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except:
            abort(404, message="Item not found")

    @blp.arguments(ItemupdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
        except:
            abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"Item: {item_id} has been deleted"}
        except:
            abort(400, message="Error deleting item")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error ocurred inserting the item")
        return item