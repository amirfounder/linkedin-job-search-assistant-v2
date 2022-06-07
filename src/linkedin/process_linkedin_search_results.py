from .commons import SearchResultsIndex, RecruitersIndex


search_results_index = SearchResultsIndex()
recruiters_index = RecruitersIndex()


def process_linkedin_search_results():
    data = search_results_index.data
    for key, obj in data.items():
        results = obj['results']
        for result in results:
            profile_url = result['link'].split('?')[0]
            recruiter_obj = {
                'dirty_profile_url': result.get('link', 'N/A'),
                'clean_profile_url': profile_url,
                'search_results_idx_key': key,
                'name': result.get('name', 'N/A'),
                'position': result.get('position', 'N/A')
            }
            recruiters_index.add(profile_url, recruiter_obj)
        print(f'Done with IDX key: {key}')
    print(len([x for x in recruiters_index.data.values() if 'hir' in x.get('position', '').lower()]))
