import json
import logging
import webbrowser
from time import sleep
from threading import Thread
from urllib.parse import unquote

from flask import Flask, request
from flask_cors import CORS


logging.getLogger('werkzeug').setLevel(logging.ERROR)
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


PEOPLE_SEARCH_QUERY_TEMPLATES = [
    "{company} technical recruiter",
    "{company} technical sourcing",
    "{company} director of recruiting",
    "{company} early career technical recruiter"
]
PEOPLE_SEARCH_MAX_PAGES = 2
PEOPLE_SEARCH_URL = 'https://www.linkedin.com/search/results/people/?keywords={}&origin=CLUSTER_EXPANSION&page={}'


def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.loads(f.read())
    except Exception:
        return


def save_as_json(path, obj: dict):
    dict_obj = json.dumps(obj, indent=4, sort_keys=True)
    try:
        with open(path, 'w') as f:
            f.write(dict_obj)
    except Exception as e:
        print(f'{type(e).__name__} Exception caught: {str(e)}')


def open_browser_tab(url: str):
    webbrowser.get('chrome').open_new(url)


def merge_lists(*args):
    res = []
    for arg in args:
        if isinstance(arg, list):
            res.extend(arg)
    return res


top_tech_companies: list[str] = merge_lists(*[obj['results'] for obj in read_json('data/top_tech_companies.json')])
top_tech_companies_search_results: dict = read_json('data/top_tech_companies_search_results.json') or {}
top_tech_companies_recruiters = None

ttcsr = top_tech_companies_search_results

tech_companies_search_results_lt_3_results = [x for x in ttcsr if len(ttcsr[x]['results']) == 3]


app = Flask(__name__)
CORS(app)


@app.route('/save-html', methods=['POST'])
def save_html():
    body = request.json

    keywords = body['url_params']['keywords']
    keywords = unquote(keywords)
    keywords = keywords.replace(' ', '_')
    page = body['url_params'].get('page', 1)

    idx_key = '{}_{}'.format(keywords, page)

    if idx_key not in top_tech_companies_search_results or idx_key in tech_companies_search_results_lt_3_results:
        top_tech_companies_search_results[idx_key] = body
        save_as_json('data/top_tech_companies_search_results.json', top_tech_companies_search_results)
        print('saved: ', idx_key)

    return 'OK', 200


def main():
    t = Thread(target=lambda: app.run(port=8082))
    t.start()

    for page in range(1, PEOPLE_SEARCH_MAX_PAGES + 1):
        for company in top_tech_companies:
            for template in PEOPLE_SEARCH_QUERY_TEMPLATES:

                idx_key = '{company}_{position}_{page}'.format(
                    company=company.lower(),
                    position=template.replace('{company} ', '').replace(' ', '_'),
                    page=page
                ).replace(' ', '_')

                # Check to if result has already been recorded
                if idx_key in top_tech_companies_search_results:
                    continue

                # Check to make sure that the previous page
                prev_page_idx_key = idx_key.replace(f'{page}', f'{page - 1}')
                if prev_page_idx_key in top_tech_companies_search_results:
                    obj = top_tech_companies_search_results[prev_page_idx_key]

                    # if the previous page results were 0, then we don't need to scape current page.
                    if len(obj.get('results', [])) == 0:
                        continue

                url = PEOPLE_SEARCH_URL.format(template.format(company=company.lower()), page)
                open_browser_tab(url)
                print('opened: ', idx_key)
                sleep(3)


if __name__ == '__main__':
    main()
