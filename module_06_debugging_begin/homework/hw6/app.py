"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, render_template_string

app = Flask(__name__)

def register_route(rule, **options):
    def decorator(f):
        app.add_url_rule(rule, view_func=f, **options)
        return f
    return decorator

@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.errorhandler(404)
def page_not_found(e):
    routes = [(str(rule.rule), str(rule.endpoint)) for rule in app.url_map.iter_rules()]

    routes_html = ''.join(f'<li><a href="{rule}">{rule}</a></li>' for rule, _ in routes)
    html = f'''
    <!doctype html>
    <html>
    <head><title>Страница не найдена</title></head>
    <body>
        <h1>Ошибка 404: Страница не найдена</h1>
        <p>Доступные страницы:</p>
        <ul>
            {routes_html}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html), 404


if __name__ == '__main__':
    app.run(debug=True)
