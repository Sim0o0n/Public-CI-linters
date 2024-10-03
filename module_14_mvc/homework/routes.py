from flask import Flask, render_template, redirect, request
from typing import List, Tuple
from models import init_db, get_all_books, DATA
import sqlite3
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
import secrets

app: Flask = Flask(__name__)
app.secret_key = secrets.token_hex(16)
csrf = CSRFProtect(app)


class BookForm(FlaskForm):
    book_title = StringField('Book Title', validators=[
        InputRequired(message="Title is required!"),
        Length(max=30, message="Title must be 30 characters or less")
    ])
    author_name = StringField('Author Name', validators=[
        InputRequired(message="Author name is required!"),
        Length(max=30, message="Author name must be 30 characters or less")
    ])
    submit = SubmitField('Add new book')
# Добавил так же валидатор для ограничение на кол-ва символов

def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()

    if form.validate_on_submit():
        title = form.book_title.data
        author = form.author_name.data

        with sqlite3.connect('table_books.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO `table_books` (title, author) VALUES (?, ?)",
                (title, author)
            )
            conn.commit()
            return redirect('/books')
    else:
        print("Validation errors:", form.errors)

    return render_template('add_book.html', form=form)


@app.route('/books/author/<string:author_name>')
def books_by_author(author_name: str) -> str:
    books = [book for book in get_all_books() if book.author.lower() == author_name.lower()]
    return render_template('books_by_author.html', author=author_name, books=books)

@app.route('/books/<int:book_id>')
def book_detail(book_id: int) -> str | tuple[str, int]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table_books WHERE id = ?", (book_id,))
        book = cursor.fetchone()

        if book:
            cursor.execute("UPDATE table_books SET view_count = view_count + 1 WHERE id = ?", (book_id,))
            conn.commit()

            # для отладки
            print(f"Book {book_id} viewed. Current view count: {book[3] + 1}")

            book_dict = {
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'view_count': book[3]
            }
            return render_template('book_detail.html', book=book_dict)
        else:
            return "Book not found", 404



if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
