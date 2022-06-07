from urllib.parse import unquote

from commons import safe_read_json_as_obj_from_file, ensure_path_exists, safe_write_obj_as_json_to_file


class Index:
    PATH = None

    def __init__(self):
        ensure_path_exists(self.PATH)
        self.data = safe_read_json_as_obj_from_file(self.PATH, {})

    def add(self, key, value):
        if key not in self.data:
            self.data[key] = value
            safe_write_obj_as_json_to_file(self.PATH, self.data)


class SearchResultsIndex(Index):
    PATH = 'data/indices/search_results.json'

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


class RecruitersIndex(Index):
    PATH = 'data/indices/recruiters.json'
