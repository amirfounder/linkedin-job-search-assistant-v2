import json
import time

from commons import run_in_separate_thread, now
from commons.helpers.browser import open_tab
from flask import Flask, request
from flask_cors import CORS

from .daos import RecruitersIndex


recruiters = RecruitersIndex()
app = Flask(__name__)
CORS(app)


@app.route('/save-data', methods=['POST'])
def save_data():
    body = request.json
    url = body['url'].split('?')[0]
    username = url.split('linkedin.com/in/')[1].removesuffix('/')
    recruiter = recruiters.get(username, {})
    recruiter.update(body.get('results', {}))
    recruiter.update({
        'profile_has_been_scraped': True,
        'profile_last_scraped': now().isoformat()
    })
    recruiters.put(username, recruiter, flush=True)

    print('Saved: ', json.dumps(recruiter, indent=4, sort_keys=True))

    return 'OK', 200


def scrape_linkedin_profiles():
    for recruiter in recruiters.source.values():

        if recruiter.get('profile_has_been_scraped', False):
            continue

        url = recruiter['clean_url']
        open_tab(url)
        time.sleep(6)


def run_profile_scraper():
    run_in_separate_thread(lambda: app.run(port=8082))
    scrape_linkedin_profiles()
    time.sleep(30)
