from urllib.parse import unquote

from commons.daos.json_index import AbstractJsonIndex


class SearchResultsIndex(AbstractJsonIndex):
    def __init__(self):
        super().__init__('data/indices/search_results.json')

    @staticmethod
    def build_key_from_search_query(search_query, page):
        search_query = search_query.lower().replace(" ", '_').replace('"', '')
        return f'{search_query}_{page}'

    @staticmethod
    def build_key_from_request_body(body):
        keywords = unquote(body['url_params']['keywords']).lower().replace(' ', '_').replace('"', '')
        page = body['url_params'].get('page', '1')
        return f'{keywords}_{page}'

    @staticmethod
    def build_prev_idx_key_from_curr_idx_key(idx_key: str, curr_page: int):
        return idx_key.replace(str(curr_page), str(curr_page - 1))


class RecruitersIndex(AbstractJsonIndex):
    def __init__(self):
        super().__init__('data/indices/recruiters.json')
