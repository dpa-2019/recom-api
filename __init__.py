import markdown
import os
from flask import flask

# create an instance of Flask

app=Flask(__name__)

@app.route("/")
    def index():
        """Present Doc"""

    # Open README

    with open (os.path.dirname(app.root_path) + '/README.md','r') as markdown_file:

        #Read content of file
        content= markdown_file.read()

        #convert to HTML
        return markdown.markdown(content)