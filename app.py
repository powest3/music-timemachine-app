from flask import (
    Flask,
    render_template,
    jsonify)
from flask_pymongo import PyMongo
import pandas as pd
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
#import dash
#import dash_core_components as dcc
#import dash_html_components as html
import plotly.graph_objs as go
# import matplotlib.pyplot as plt
import numpy as np #importing Numpy

# from nltk.tokenize import word_tokenize  # to split sentences into words
# from nltk.corpus import stopwords  # to get a list of stopwords
# from collections import Counter  # to get words-frequency

#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #initiating VADER instance

# import nltk
# nltk.download('vader_lexicon')
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/billboard_db")
music = mongo.db.all_number_one_songs
word = mongo.db.word_cloud_data


df = pd.DataFrame(list(music.find()))
reduced_df = df.drop(['_id'], axis=1)

df2 = pd.DataFrame(list(word.find()))
word_data = df2.drop(['_id'], axis=1)


@app.route("/")
def index():

    return render_template("Index.html")

@app.route("/Index.html")
def index2():

    return render_template("Index.html")

@app.route("/Songs.html")
def artist():


    return render_template("Songs.html")

@app.route("/Machine.html")
def artistcomp():

    return render_template("Machine.html")
@app.route("/Artist.html")
def atrist():

    return render_template("Artist.html")

@app.route("/History.html")
def history():

    return render_template("History.html")



@app.route("/alldata")
def alldata():
    result = reduced_df.to_json(orient = "records")
    return (result)

@app.route("/wordcloud")
def wordcloud():
    
    # finalresults = word_data.to_dict('records')
    finalresults = word_data.to_json(orient = "records")
    return (finalresults)
# json.dumps

if __name__ == "__main__":
    app.run(debug=True)
