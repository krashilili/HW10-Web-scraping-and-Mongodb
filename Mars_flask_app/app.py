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
    # Overwrite with new data
    db['data'].update_one({}, {'$set': mars_data}, upsert=False)
    return "Data has been stored to Mongodb!"


@app.route('/')
def view():
    mars_data = db['data'].find_one({})
    mars_data.pop('_id')
    # return jsonify(mars_data)
    # return "Data stored to Mongodb!"
    # table = LH.fromstring(mars_data.get('mars_facts'))
    html_table = mars_data.get('mars_facts')
    html_table= html_table.replace('\n', '')
    mars_data['mars_facts']=html_table
    return render_template('index.html',mars_data=mars_data)



if __name__ == '__main__':
    app.run()
