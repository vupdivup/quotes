import requests
import bs4

url = "https://www.litquotes.com/quote_title_resp.php?TName=Allan%20Quatermain"

def get_quotes(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")

    selector = "div[style=\"" \
        "margin: 30px 20px 0px 20px; " \
        "font-size: 110%;\"]"

    # list of quotes
    list = soup.css.select_one(selector)

    # all tags within quote list, including unneeded links etc.
    tags = list(list.children)

    # group tags by quote
    groups = [
        tags[i:i + 6]
        for i in range(0, len(tags), 6)
    ]

    quotes = []

    for g in groups:
        quotes.append({
            "quote": g[0].string,
            "title": g[1].string,
            "author": g[3].string
        })

    return quotes

print(get_quotes(url))