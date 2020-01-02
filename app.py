import json
from threading import Thread

from flask import Flask, render_template, request, jsonify, redirect, url_for
import Streampy as st
import Streampy2 as st2
import sys


app = Flask(__name__)
search_term = ''
search_term2 = ''


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        st.reset_dict()
        global search_term
        search_term = request.form['topic1']
        return 'OK', 200
    # GET request
    else:
        as_json = json.dumps(st.npn_dict)
        return jsonify(as_json)  # serialize and use JSON headers


@app.route('/hello2', methods=['GET', 'POST'])
def hello2():
    # POST request
    if request.method == 'POST':
        st2.reset_dict()
        global search_term2
        search_term2 = request.form['topic2']
        return 'OK', 200
    # GET request
    else:
        as_json = json.dumps(st2.npn_dict)
        return jsonify(as_json)  # serialize and use JSON headers


@app.route('/api', methods=['POST'])
def start():
    global search_term
    search_term = request.form['topic1']
    global search_term2
    search_term2 = request.form['topic2']
    st.reset_dict()
    st2.reset_dict()
    thread2 = Thread(target=start_stream)
    thread3 = Thread(target=start_stream2)
    thread2.start()
    thread3.start()
    thread2.join()
    thread3.join()
    return redirect(url_for('index', topic1=search_term, topic2=search_term2))


@app.route('/')
def hello_world():
    return render_template('index.html', topic1=search_term, topic2=search_term2)


def start_stream():
    api = st.tweepy.API(st.auth, wait_on_rate_limit=True,
                        wait_on_rate_limit_notify=True)

    tweets_listener = st.MyStreamListener(api)
    stream = st.tweepy.Stream(api.auth, tweets_listener)
    global search_term
    stream.filter(track=[search_term], languages=["en"])


def start_stream2():
    api = st2.tweepy.API(st2.auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

    tweets_listener = st2.MyStreamListener(api)
    stream = st2.tweepy.Stream(api.auth, tweets_listener)
    global search_term2
    stream.filter(track=[search_term2], languages=["en"])


thread1 = Thread(target=app.run)


if __name__ == '__main__':
    thread1.start()
    thread1.join()

