import os
import re
import requests

BASE_URL = "https://free4.xyz"
SEARCH_URL = "https://free4.xyz/?s="

HTML_ENTITIES = {
    "&#8211;": "-",
    "&#8217;": "'",
    "&#038;": "&",
    "&#8216;": "'",
    "&#8220;": '"',
    "&#8221;": '"',
    "&#amp;": "&",
}


def clean_html_entities(text):
    for entity, char in HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return text


def fetch_latest():
    response = requests.get(BASE_URL, timeout=30)
    response.raise_for_status()

    titles = []
    links = []
    for line in response.text.splitlines():
        if '<a class="overlay-link"' in line:
            match = re.search(r'aria-label="([^"]+)"', line)
            if match:
                titles.append(clean_html_entities(match.group(1)))
            match = re.search(r'href="([^"]+)"', line)
            if match:
                links.append(match.group(1))

    results = []
    for i in range(min(5, len(titles), len(links))):
        results.append({"title": titles[i], "url": links[i]})

    total_count = len(titles)
    return results, total_count


def search(keyword):
    url = SEARCH_URL + keyword
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    titles = []
    links = []
    for line in response.text.splitlines():
        if '<a class="penci-image-holder penci-lazy"' in line:
            match = re.search(r'title="([^"]+)"', line)
            if match:
                titles.append(clean_html_entities(match.group(1)))
            match = re.search(r'href="([^"]+)"', line)
            if match:
                links.append(match.group(1))

    results = []
    for i in range(min(5, len(titles), len(links))):
        results.append({"title": titles[i], "url": links[i]})

    total_count = len(titles)
    return results, total_count


def get_download_links(page_url):
    response = requests.get(page_url, timeout=30)
    response.raise_for_status()

    links = {}
    patterns = {
        "KatFile": '<p>KatFile Download Link</p>',
        "RapidGator": '<p>RapidGator Download Link</p>',
        "NitroFlare": '<p>NitroFlare Download Link</p>',
    }

    for name, pattern in patterns.items():
        for i, line in enumerate(response.text.splitlines()):
            if pattern in line:
                next_lines = response.text.splitlines()[i+1:i+2]
                if next_lines:
                    match = re.search(r'href="([^"]+)"', next_lines[0])
                    if match:
                        links[name] = match.group(1)
                break

    return links
