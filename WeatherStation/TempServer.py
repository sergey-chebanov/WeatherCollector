from flask import Flask

from sensor import command

app = Flask(__name__) 

@app.route('/')
def hello():
	return ''.join(command('t'))


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
