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

import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/billboard_db")
music = mongo.db.all_number_one_songs


analyser = SentimentIntensityAnalyzer()



df = pd.DataFrame(list(music.find()))

df.head()

#df2 = df.drop(['_id'], axis=1)
reduced_df = df.dropna(how='any')
lyrics_index = reduced_df.set_index("lyrics")
i=0 #counter

compval1 = [ ]  #empty list to hold our computed 'compound' VADER scores


while (i<len(reduced_df)):

    k = analyser.polarity_scores(reduced_df.iloc[i]['lyrics'])
    compval1.append(k['compound'])
    
    i = i+1
    
#converting sentiment values to numpy for easier usage

compval1 = np.array(compval1)

len(compval1)
reduced_df['VADER'] = compval1

#Assigning score categories and logic
i = 0
predicted_value =[]

while(i<len(reduced_df)):
    if ((reduced_df.iloc[i]['VADER'] >= 0.5)):
        predicted_value.append('positive')
        i = i+1
    elif ((reduced_df.iloc[i]['VADER'] > 0) & (reduced_df.iloc[i]['VADER'] < 0.5)):
        predicted_value.append('neutral')
        i = i+1
    elif ((reduced_df.iloc[i]['VADER'] == 0)):
        predicted_value.append('NA')
        i = i+1
    elif ((reduced_df.iloc[i]['VADER'] < (0))):
        predicted_value.append('negative')
        i = i+1
reduced_df['sentiment'] = predicted_value
reduced_df.drop(reduced_df[reduced_df['sentiment'] == 'NA'].index , inplace=True)
bins = [1950,1960,1970,1980,1990,2000,2010,2020]
group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
# Slice the data and place it into bins
reduced_df["decade"] = pd.cut(reduced_df["year"], bins, labels=group_names, right=False)




#set the routes and render remplates for all the html files
# @app.route("/")
# def index():

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

# @app.route("/wordcloud")
# def wordcloud():
#     df60s = reduced_df[reduced_df['decade']=='60s']
#     comment_words =''
# # iterate through the csv file 
#     for val in df60s['lyrics']: 
      
#     # typecaste each val to string 
#         val = str(val) 
  
#     # split the value 
#         tokens = val.split() 
      
#     # Converts each token into lowercase 
#         for i in range(len(tokens)): 
#             tokens[i] = tokens[i].lower() 
          
#         for words in tokens: 
#             comment_words = comment_words + words + ' '

#     words = word_tokenize(comment_words)

#         # get stopwords
#     stop_words = set(stopwords.words('english'))

#         # remove stopwords from our words list and also remove any word whose length is less than 3
#         # stopwords are commonly occuring words like is, am, are, they, some, etc.
#     words = [word for word in words if word not in stop_words and len(word) > 3]

#         # now, get the words and their frequency
#     words_freq = Counter(words)

#         # JQCloud requires words in format {'text': 'sample', 'weight': '100'}
#         # so, lets convert out word_freq in the respective format
#     words_json = [{'word': word, 'weighted': count} for word, count in words_freq.items()]
#     newlist = sorted(words_json, key=lambda i: i['weighted'],reverse=True) 
#     finallist = newlist[:100]
#     return json.dumps(finallist)
# @app.route("/the1960s")
# def artist_count_data_60s():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
# # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
# # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()
#     df = df[df['decade']=='60s']
#     df1960 = df.sort_values(by='Length', ascending=False)
#     df1960 = df1960.head(10)
#     # Format the data for Plotly
#     trace = {
#         "x": df1960["title"].values.tolist(),
#         "y": df1960["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)

# @app.route("/the1970s")
# def artist_count_data_70s():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
#     # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
#     # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()

#     df = df[df['decade']=='70s']
#     df1970 = df.sort_values(by='Length', ascending=False)
#     df1970 = df1970.head(10)
#     # Format the data for Plotly
#     trace = {
#         "x": df1970["title"].values.tolist(),
#         "y": df1970["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)

# @app.route("/the1980s")
# def artist_count_data_80s():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
#     # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
#     # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()

#     df = df[df['decade']=='80s']
#     df1980 = df.sort_values(by='Length', ascending=False)
#     df1980 = df1980.head(10)
#     # Format the data for Plotly
#     trace = {
#         "x": df1980["title"].values.tolist(),
#         "y": df1980["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)

# @app.route("/the1990s")
# def artist_count_data_90s():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
#     # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
#     # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()

#     df = df[df['decade']=='90s']
#     df1990 = df.sort_values(by='Length', ascending=False)
#     df1990 = df1990.head(10)
#     # Format the data for Plotly
#     trace = {
#         "x": df1990["title"].values.tolist(),
#         "y": df1990["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)

# @app.route("/the2000s")
# def artist_count_data_2000s():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
#     # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
#     # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()

#     df = df[df['decade']=='2000s']
#     df2000 = df.sort_values(by='Length', ascending=False)
#     df2000 = df2000.head(10)
#     # Format the data for Plotly
#     trace = {
#         "x": df2000["title"].values.tolist(),
#         "y": df2000["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)


# @app.route("/the2010s")
# def artist_count_data_2010s():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
#     # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
#     # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()

#     df = df[df['decade']=='2010s']
#     df2010 = df.sort_values(by='Length', ascending=False)
#     df2010 = df2010.head(10)
#     # Format the data for Plotly
#     trace = {
#         "x": df2010["title"].values.tolist(),
#         "y": df2010["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)



# @app.route("/alltime")
# def artist_count_data_alltime():
#     df = pd.DataFrame(list(music.find()))
#     # Create bins in which to place values based upon TED Talk views
#     bins = [1950,1960,1970,1980,1990,2000,2010,2020]
#     # Create labels for these bins
#     group_names =["50s","60s","70s","80s","90s","2000s","2010s"]
#     # Slice the data and place it into bins
#     df["decade"] = pd.cut(df["year"], bins, labels=group_names, right=False)
#     df['Length'] = df['issue_date'].str.len()    
#     df2010 = df.sort_values(by='Length', ascending=False)
#     df2010 = df2010.head(30)
#     # Format the data for Plotly
#     trace = {
#         "x": df2010["title"].values.tolist(),
#         "y": df2010["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)


# @app.route("/line")
# def testline():
#     df = pd.DataFrame(list(music.find()))
#     df['Length'] = df['issue_date'].str.len()
#     df =df.groupby("year")
# # Get the average of each column within the GroupBy object
# # Get the average of each column within the GroupBy object
#     meandf = df[["Length"]].mean()
#     meandf= meandf.reset_index()
#     data = [{
#         "x": meandf["year"].values.tolist(),
#         "y": meandf["Length"].values.tolist()
#         }]

#     return jsonify(data)


# @app.route("/testjson")
# def testjson():
#     df = pd.DataFrame(list(music.find()))
#     df['Length'] = df['issue_date'].str.len()
#     df =df.groupby("artist")
#     dfsum = df[["Length"]].sum()
#     dfsum= dfsum.reset_index()
#     dfsum = dfsum.sort_values(by='Length', ascending=False)
#     dfsum = dfsum.head(30)
#     trace = {
#         "x": dfsum["artist"].values.tolist(),
#         "y": dfsum["Length"].values.tolist(),
#         "type": "bar"
#     }
#     return jsonify(trace)

# FIELDS = {'year': True, 'issue_date': True, 'title': True, 'artist': True, '_id': False}
# @app.route("/artists")
# def artistschoose():
#     projects = music.find(projection=FIELDS)
#     json_projects = []
#     for project in projects:
#         json_projects.append(project)
#     json_projects = json.dumps(json_projects, default=json_util.default)
#     return json_projects



if __name__ == "__main__":
    app.run(debug=True)
