import requests
import bs4

url1 = "https://www.litquotes.com/quote_title_resp.php?TName=Allan%20Quatermain"
url2 = "https://www.litquotes.com/quote_title_resp.php?TName=Dune"

def soupify_page(url):
    r = requests.get(url)

    r.raise_for_status()

    return bs4.BeautifulSoup(r.content, "html.parser")

def scrape_quotes(page_url):
    soup = soupify_page(page_url)

    d = soup.find(
        "div",
        style="margin: 30px 20px 0px 20px; " \
            "font-size: 110%;"
    )

    # group tags by quote
    groups = [
        d.contents[i:i + 6]
        for i in range(0, len(d.contents), 6)
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

def get_page_urls(section_url):
    soup = soupify_page(section_url)

    d = soup.find(
        "div",
        style="margin: 30px 20px 0px 20px; " \
            "font-size: 110%;"
    )

    # return if there's no navigation for more pages
    if d.contents[-4].name != "div":
        return [section_url]
    
    pagination = d.contents[-4]

    links = pagination.find_all("a")

    hrefs = [
        "https://litquotes.com" + l["href"]
        for l in links
        if l.string != "Next>>"
    ]
    
    return [section_url, *hrefs]
    
def get_section_urls(segment_url):
    soup = soupify_page(segment_url)

    # parent table of section list
    t = soup.find(
        "table",
        border="0",
        cellspacing="0",
        cellpadding="0",
        style="border-collapse: collapse; " \
            "margin-left: 40px; " \
            "width: 90%;",
        align="left"
    )

    return [a["href"] for a in t.find_all("a")]

def get_segment_urls(category_url):
    soup = soupify_page(category_url)

    # parent div of segment list
    d = soup.find(
        "div",
        style="margin: 10px 0 10px 0;"
    )

    # extract segment links
    return [a["href"] for a in d.find_all("a")]