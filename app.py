import markdown
import os

from flask import Flask

# create an instance of Flask

app = Flask(__name__)


@app.route('/')
def hello():
    count = 1
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)