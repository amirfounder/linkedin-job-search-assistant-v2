from .daos import SearchResultsIndex, RecruitersIndex


search_results_index = SearchResultsIndex()
recruiters_index = RecruitersIndex()


def process_linkedin_search_results():
    invalid_profiles = []

    for key, obj in search_results_index.source.items():
        results = obj['results']

        for result in results:
            profile_url: str = result['link'].split('?')[0]
            sep = 'linkedin.com/in/'
            username = profile_url.split(sep)[1] if len(profile_url.split(sep)) == 2 else None

            new_obj = {
                'name': result.get('name', 'N/A'),
                'position': result.get('position', 'N/A'),
                'url': result.get('link', 'N/A'),
                'clean_url': profile_url,
                'username': username,
                'search_results_idx_key': key
            }

            if username is None:
                invalid_profiles.append(new_obj)
            else:
                recruiters_index.put(username, new_obj)

        recruiters_index.flush()
        print(f'Done with IDX key: {key}')

    print(len(recruiters_index))
    print(len(invalid_profiles))
