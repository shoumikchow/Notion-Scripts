from flask import Flask, render_template, request
import add_arxiv_to_db

SECRET_KEY = "SECRET_KEY"

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def default():
    if request.method == 'POST':
        url = request.form['url']
        priority = request.form['priority']
        print(url)
        print(priority)
        response = add_arxiv_to_db.add_(SECRET_KEY, url, priority)

        if response == 200:
            return "Successfully saved to Notion database"
        else:
            return f"Error: {response}"

    else:
        return render_template('index.html')


def add_to_db(paper_url, secret, priority):
    pass