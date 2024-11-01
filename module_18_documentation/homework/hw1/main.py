from flasgger import swag_from
from flask import request
from flask_restful import Resource
from module_17_rest_api.homework.app.models import get_all_books, add_book
from module_17_rest_api.homework.app.schemas import BookSchema
from marshmallow import ValidationError

class BookList(Resource):
    @swag_from('books_spec.yml')
    def get(self):
        schema = BookSchema()
        books = get_all_books()
        return schema.dump(books, many=True), 200

    @swag_from('books_spec.yml')
    def post(self):
        schema = BookSchema()
        data = request.get_json()

        try:
            book = schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        added_book = add_book(book)
        return schema.dump(added_book), 201



