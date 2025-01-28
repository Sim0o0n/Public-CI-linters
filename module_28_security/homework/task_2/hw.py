from flask import Flask, Response, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>Title</title>
</head>
<body>
    <h1>Hello, CSP Example!</h1>
    <script>alert('This inline script should NOT run.');</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.after_request
def apply_csp(response: Response):
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    return response

if __name__ == "__main__":
    app.run(port=8080, debug=True)

