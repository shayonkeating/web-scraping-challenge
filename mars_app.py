# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# flask
app = Flask(__name__)

# pymongo for connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route for index.html
@app.route("/")
def home(): 

    # find the data
    mars_facts = mongo.db.collection.find_one()

    # return template and data
    return render_template("index.html", mars=mars_facts)

# scrapy scrape
@app.route("/scrape")
def scrape():

    # run the scrape function
    mars_data = scrape_mars.scrape()

    # update the db database
    mongo.db.collection.update({}, mars_data, upsert=True)

    # redirect to the homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)