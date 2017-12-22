import json
from urllib.request import getproxies

import requests
from bs4 import BeautifulSoup

def make_soup(url):  # pragma: no cover
    """Make soup, that is basically parsing the html document."""
    response = requests.get(
        url,
        headers={'User-agent': 'UIP'},
        # gets system proxy (if it is currently using one)
        proxies=getproxies())

    html = response.content
    return BeautifulSoup(html, "html.parser")


def make_json(url):  # pragma: no cover
    """Make a dictionary out of a json file."""
    response = requests.get(
        url,
        headers={'User-agent': 'UIP'},
        # gets system proxy (if it is currently using one)
        proxies=getproxies())

    json_file = response.text
    data = json.loads(json_file)
    return data

def unsplash_scraper(no_of_images=5):
    """Retrieve images from unsplash.

    Returns a list of tuples containing filename and url of the image.
    """
    url = "https://unsplash.com/new"
    soup = make_soup(url)
    '''Selects desired bs4 tags, soup.select is a recursive function,
       it searches for classes/tags within classes/tags'''
    a_tags = soup.select('.y5w1y .hduMF .tPMQE a')
    image_links = []
    if not a_tags:
        print('No matching image found')
        return []

    for a_tag in a_tags:
        image_url = a_tag['href']
        image_links.append(image_url)
        if len(image_links) < no_of_images:
            break
    return image_links


def reddit_scraper(subreddits=[], no_of_images=5):
    """Retrieve images from reddit.

    Returns a list of tuples containing filename and url of the image.
    """
    # reddit requires .json format for the URL
    image_links = []
    for subreddit in subreddits:
        url = "www.reddit.com/r/"+subreddit + '/.json'
        page = make_json(url)
        children = []
        try:
            # structure of reddit API
            children = page['data']['children']
        except (IndexError, KeyError) as e:
            print("You seem to be having some issues with your internet."
                  "Please contact us at our github repo 'NIT-dgp/UIP'"
                  "If you feel it isn't the case with your internet.", e)
            continue
        for child in children:
            images = []
            try:
                images = child['data']['preview']['images']
            except KeyError:
                pass
            for image in images:
                if(len(image_links) < no_of_images):
                    image_url = image['source']['url']
                    image_links.append(image_url)
                else:
                    break
    return image_links


def desktoppr_scraper(no_of_images=5):
    """Retrieve images from desktoppr.

    Returns a list of tuples containing filename and url of the image.
    """
    url = "https://api.desktoppr.co/1/wallpapers"
    responses = []
    image_links = []
    index = 1
    while len(responses) < no_of_images:
        page_url = url + ('?page=%d' % index)
        data = make_json(page_url)
        responses.extend(data['response'])
        index += 1
    responses = responses[:no_of_images]
    for result in responses:
        image_url = result['image']['url']
        filename = image_url.split('/')[-1]
        image_links.append(image_url)

    return image_links
