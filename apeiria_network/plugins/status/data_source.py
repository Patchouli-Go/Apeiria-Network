import requests

def request_api_params(url, params):
    headers = {'User-Agent': 'Mozilla/5.0 4240.75 Safari/537.36'}
    response = requests.get(url, headers=headers, params=params, timeout=(1, 30))
    html = response.text
    return html