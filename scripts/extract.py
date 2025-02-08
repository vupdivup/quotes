import requests
import bs4
import os
import json

base_url = "https://www.litquotes.com/"

def soupify_page(url):
    r = requests.get(url)

    r.raise_for_status()

    # lxml is preferred, as it parses unorganized html better here
    return bs4.BeautifulSoup(r.text, "lxml")

def get_rel_url(url):
    return url.replace(base_url, "")

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

    # find main container
    d = soup.find(
        "div",
        style="margin: 30px 20px 0px 20px; " \
            "font-size: 110%;"
    )

    # return if there's no page navigation
    if d.contents[-4].name != "div":
        return [section_url]
    
    pagination = d.contents[-4]

    links = pagination.find_all("a")

    hrefs = [
        "https://litquotes.com" + l["href"]
        for l in links
        # exclude the next link, as it's a duplicate of another one
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

def main():
    quotes = []

    # mine down in hierarchy
    for segment_url in get_segment_urls(base_url + "quote_title.php"):
        print(f"SEGMENT {get_rel_url(segment_url)}")

        for section_url in get_section_urls(segment_url):
            print(f"SECTION {get_rel_url(section_url)}")

            for page_url in get_page_urls(section_url):
                print(f"PAGE {get_rel_url(page_url)}")

                # scrape quotes
                quotes.extend(scrape_quotes(page_url))

    # create raw dir if non-existent
    os.makedirs("raw", exist_ok=True)

    # write to file
    with open("raw/quotes.json", "w") as f:
        json.dump(quotes, f, indent=4)

if (__name__ == "__main__"):
    main()