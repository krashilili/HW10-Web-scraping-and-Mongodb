from flask import Flask, jsonify
from scrape_mars import scrape
from pymongo import MongoClient
from splinter import Browser

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


client = MongoClient('localhost', 27017)
db = client['Mars']


app = Flask(__name__)


@app.route('/scrape')
def scrape_mars_data():
    mars_data = scrape(browser)
    db['data'].insert(mars_data)
    return "Data stored to Mongodb!"


@app.route('/')
def view():
    mars_data = db['data'].find_one({})
    mars_data.pop('_id')
    return jsonify(mars_data)
    # return "Data stored to Mongodb!"



if __name__ == '__main__':
    app.run()
