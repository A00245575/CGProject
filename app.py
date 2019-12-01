import json
from threading import Thread

from flask import Flask, render_template, request, jsonify
import Streampy as st

app = Flask(__name__)
search_term = 'Playstation'
search_term2 = 'Xbox'


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.form['topic1'])  # parse as JSON
        search_term = request.form['topic1']
        search_term2 = request.form['topic2']
        return 'OK', 200
    # GET request
    else:
        as_json = json.dumps(st.npn_dict)
        return jsonify(as_json)  # serialize and use JSON headers


@app.route('/')
def hello_world():
    return render_template('index.html')


def start_stream():
    api = st.tweepy.API(st.auth, wait_on_rate_limit=True,
                        wait_on_rate_limit_notify=True)

    tweets_listener = st.MyStreamListener(api)
    stream = st.tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=[search_term], languages=["en"])


# def start_stream2():
#     api = st.tweepy.API(st.auth, wait_on_rate_limit=True,
#                         wait_on_rate_limit_notify=True)
#
#     tweets_listener = st.MyStreamListener(api)
#     stream = st.tweepy.Stream(api.auth, tweets_listener)
#     stream.filter(track=[search_term], languages=["en"])


thread2 = Thread(target=start_stream)
#thread3 = Thread(target=start_stream2)

thread1 = Thread(target=app.run)
thread2.start()
#thread3.start()

if __name__ == '__main__':
    thread1.start()
    thread1.join()
    thread2.join()
    #thread3.join()
