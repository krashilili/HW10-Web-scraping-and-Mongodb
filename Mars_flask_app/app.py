from flask import Flask, jsonify, render_template
from scrape_mars import scrape
from pymongo import MongoClient
from splinter import Browser
import lxml.html as LH

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


client = MongoClient('localhost', 27017)
db = client['Mars']


app = Flask(__name__)


@app.route('/scrape')
def scrape_mars_data():
    mars_data = scrape(browser)
    # Insert data to db for the first time
    doc = db.data.find_one({})
    if not doc:
        db['data'].insert(mars_data)
    else:
        # Overwrite with new data
        db['data'].update_one({}, {'$set': mars_data}, upsert=False)
    return "Data has been stored to Mongodb!"


@app.route('/')
def view():
    try:
        mars_data = db['data'].find_one({})
        mars_data.pop('_id')
        html_table = mars_data.get('mars_facts')
        html_table= html_table.replace('\n', '')
        mars_data['mars_facts']=html_table
        return render_template('index.html',mars_data=mars_data)
    except:
        return "No data in Mongodb! Please scrape first by `127.0.0.0/scrape`. "



if __name__ == '__main__':
    app.run()
