import requests

NEWS_API_KEY = "33404ff724604220981e6f56be06ac89"

def get_news(keyword):

    url = "https://newsapi.org/v2/everything"

    parameters = {
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }