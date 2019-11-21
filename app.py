from flask import Flask, render_template
from Streampy import npn_dict
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


print(npn_dict["Positive"])


if __name__ == '__main__':
    app.run()
