import requests
import bs4

url1 = "/quote_title_resp.php?TName=Allan%20Quatermain"
url2 = "/quote_title_resp.php?TName=Dune"

def soupify_page(url):
    base = "https://www.litquotes.com"
    r = requests.get(base + url)
    return bs4.BeautifulSoup(r.content, "html.parser")

def get_container(url):
    soup = soupify_page(url)

    # style selector, there isn't a more precise direct alternative
    selector = "div[style=\"" \
        "margin: 30px 20px 0px 20px; " \
        "font-size: 110%;\"]"

    # list of quotes
    return soup.css.select_one(selector)


def get_quotes(url):
    container = get_container(url)

    # all tags within quote list, including unneeded links etc.
    tags = list(container.children)

    # group tags by quote
    groups = [
        tags[i:i + 6]
        for i in range(0, len(tags), 6)
    ]

    # ensure compliance with quote group format
    # this filters out leading and trailing misc tags
    groups = [
        g
        for g in groups
        if [t.name for t in g] == [None, "i", None, "a", None, "div"]
    ]

    quotes = []

    # extract quote data
    for g in groups:
        quotes.append({
            "quote": g[0].string,
            "title": g[1].string,
            "author": g[3].string
        })

    return quotes

# print(get_quotes(url))

def get_indices(url):
    container = get_container(url)

    tags = list(container.children)

    # return if there's no navigation for more pages
    if tags[-4].name != "div":
        return [url]
    
    pagination = tags[-4]

    links = pagination.find_all("a")

    hrefs = [
        l["href"]
        for l in links
        if l.string != "Next>>"
    ]
    
    return [url, *hrefs]
    

# print(get_quotes(url2))