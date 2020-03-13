from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_info = mongo.db.data.find_one()
    return render_template("index.html", mars=mars_info)


@app.route("/scrape")
def scrape():
    mongo.db.data.drop()
    scraped_data = scrape_mars.scrape()
    mongo.db.data.insert_one(scraped_data)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)