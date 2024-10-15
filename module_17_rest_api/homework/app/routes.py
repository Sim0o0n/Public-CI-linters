from flask import request
from flask_restful import Resource, Api
from models import (
    get_author_by_id, add_author, delete_author_by_id, get_books_by_author_id,
    add_book, get_book_by_id, update_book_by_id, delete_book_by_id
)
from schemas import AuthorSchema, BookSchema

author_schema = AuthorSchema()
book_schema = BookSchema()

class AuthorListResource(Resource):
    def post(self):
        data = request.get_json()
        errors = author_schema.validate(data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 400

        author = add_author(data['first_name'], data['last_name'], data.get('middle_name'))
        return author_schema.dump(author), 201

class AuthorResource(Resource):
    def get(self, author_id):
        author = get_author_by_id(author_id)
        if not author:
            return {"message": "Author not found"}, 404

        books = get_books_by_author_id(author_id)
        return {
            "author": author_schema.dump(author),
            "books": book_schema.dump(books, many=True)
        }

    def delete(self, author_id):
        author = get_author_by_id(author_id)
        if not author:
            return {"message": "Author not found"}, 404

        delete_author_by_id(author_id)
        return {"message": "Author and their books deleted"}, 200

class BookResource(Resource):
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book_schema.dump(book), 200

    def put(self, book_id):
        data = request.get_json()
        errors = book_schema.validate(data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 400

        updated_book = update_book_by_id(book_id, data['title'], data['author_id'])
        if not updated_book:
            return {"message": "Book not found"}, 404

        return book_schema.dump(updated_book), 200

    def delete(self, book_id):
        book = get_book_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404

        delete_book_by_id(book_id)
        return {"message": "Book deleted"}, 200
