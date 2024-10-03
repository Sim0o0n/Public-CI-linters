from flask import Flask, render_template
from typing import List

from models import init_db, get_all_books, DATA

app: Flask = Flask(__name__)

BOOKS = [{'id':0,'title': 'A Byte of Python','author': 'Swaroop C. H.'},
         {'id':1,'title': 'Moby-Dick; or, The Whale','author' : 'Herman Melville'},
         {'id':2,'title': 'War and Peace','author': 'Leo Tolstoy'}
]
def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table class="customTable">
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
   #  return """
   #      <html>
   #          <head>
   #          </head>
   #          <body>
   #              <h1>Books:</h1>
   #              {table}
   #          </body>
   #      </html>
   #      """.format(table=_get_html_table_for_books(BOOKS))



@app.route('/books/form')
def get_books_form() -> str:
   return render_template('add_book.html')


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
