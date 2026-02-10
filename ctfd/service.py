import requests
from django.conf import settings
from django.core.cache import cache

class CTFdService:

    @staticmethod
    def get_team_scores():
        cache_key = 'ctfd_leadearboard_scores'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data
        
        ctfd_url = settings.CTFD_URL
        ctfd_token = settings.CTFD_API_TOKEN
        headers = {
            'Authorization': f'Token {ctfd_token}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(f'{ctfd_url}/api/v1/scoreboard', headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json().get('data', [])
                scores = {team['account_id']: team['score'] for team in data}
                cache.set(cache_key, scores, timeout=300)  # Cache for 5 minutes
                return scores
        
        except requests.RequestException as e:
            print(f"Error fetching CTFd scores: {e}")
            return {}
        return {}
    
    @staticmethod
    def get_team_score(team_id):
        cache_key = f'ctfd_team_score_{team_id}'
        cached_score = cache.get(cache_key)
        if cached_score:
            return cached_score
        
        ctfd_url = settings.CTFD_URL
        ctfd_token = settings.CTFD_API_TOKEN

        headers = {
            'Authorization': f'Token {ctfd_token}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(f'{ctfd_url}/api/v1/teams/{team_id}', headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json().get('data',{})
                score = data.get('score', 0)
                cache.set(cache_key, score, timeout=300)  # Cache for 5 minutes
                return score
        except requests.RequestException as e:
            print(f"Error fetching CTFd team score: {e}")
            return 0
        return 0
    



