from flask import Flask
app = Flask(__name__)

@app.route("/<string:action>")
def hello(action):
    return "Hello, World %s" % action

if __name__ == "__main__":
    app.run(debug=True)
