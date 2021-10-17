from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars

app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

db_name = "mars_app"
mars_collection = "Mars_info"
mongo_url = "mongodb://localhost:27017/mars_app"
client = MongoClient(mongo_url)
db = client[db_name]

@app.route("/index.html")
def index(): 
    collection = db[mars_collection]
    results = collection.find()
    mars_data = mongo.db.Mars_info.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scraper():
 # Run the scrape function
    collection = db[mars_collection]
    results = collection.find()
    Mars_info = scrape_mars.scrape()
    mongo.db.collection.update({}, Mars_info, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)
if __name__ == "__main__":
    app.run(debug=True)