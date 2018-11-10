#dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

#setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraping_app")

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars = mongo.db.mars.find_one()
    
    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scraper():

    # Run scraped functions
    mars = mongo.db.mars

    # Store results into a dictionary
    mars_data = scrape_mars.scrape()
    
    # Insert data into database
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)