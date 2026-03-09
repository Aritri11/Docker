from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Multiplication Table</title>
</head>
<body>
  <h1>Multiplication Table Generator</h1>

  <form method="post">
    <label for="num">Enter a number:</label>
    <input type="number" id="num" name="num" required min="1" max="10">
    <button type="submit">Generate</button>
  </form>

  {% if error %}
    <p style="color:red;">{{ error }}</p>
  {% endif %}

  {% if table %}
    <h2>Table for {{ n }}</h2>
    <ul>
      {% for row in table %}
        <li>{{ row }}</li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    table = []
    error = None
    n = None

    if request.method == "POST":
        num_str = request.form.get("num")
        try:
            n = int(num_str)
            if n < 1 or n > 10:
                raise ValueError("Number must be between 1 and 10.")
            table = [f"{n} × {i} = {n * i}" for i in range(1, 11)]
        except (TypeError, ValueError):
            error = "Please enter a valid integer between 1 and 10."

    return render_template_string(TEMPLATE, table=table, n=n, error=error)

if __name__ == "__main__":
    # host=0.0.0.0 so it works inside Docker with port mapping
    app.run(host="0.0.0.0", port=5000, debug=False)
