from bs4 import BeautifulSoup
import requests

def parse_rss():
    response = []
    try:
        req = requests.get('http://yvision.kz/feed')
    except requests.exceptions.RequestException as e:
        return (-1, response)

    if req.status_code == 200:
        soup = BeautifulSoup(req.content,"html.parser")
        some = soup.find_all('item')[:5]

        for item in some:
            res = {}
            res['title'] = item.title.string
            res['link'] = item.link.string
            response.append(res)
    return (req.status_code, response)