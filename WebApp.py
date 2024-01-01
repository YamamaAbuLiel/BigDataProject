#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterdb']
tweet_collection = db['tweets']
app.static_folder = 'static'

# Function to fetch top 20 users
def get_top_users():
    top_users = tweet_collection.aggregate([
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ])
    return list(top_users)

# Function to fetch tweet distribution over time
def get_tweet_distribution():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)  # Adjust the time range as needed

    tweet_distribution = tweet_collection.aggregate([
        {"$match": {"createdAt": {"$gte": start_date}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ])
    return list(tweet_distribution)

# Schedule the background job to fetch data every minute
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_top_users, trigger="interval", minutes=1)
scheduler.add_job(func=get_tweet_distribution, trigger="interval", minutes=1)
scheduler.start()

# Route to render the dashboard
@app.route('/')
def index():
    return render_template('index.html')

# API route to fetch top users
@app.route('/api/top_users')
def api_top_users():
    data = get_top_users()
    return jsonify(data)

# API route to fetch tweet distribution
@app.route('/api/tweet_distribution')
def api_tweet_distribution():
    data = get_tweet_distribution()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:





# In[ ]:




