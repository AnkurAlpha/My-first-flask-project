from flask import Flask , render_template
app = Flask(__name__)  # just to refernce the file


# setting up route
@app.route('/')
def index():
    return "Hello, World"


if __name__ == "__main__":
    app.run(debug=True) # if there is some error then it will pop up on the page
