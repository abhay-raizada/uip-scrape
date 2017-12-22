import unittest

from bs4 import BeautifulSoup

from lib import scrape
from lib import plugins


class ScrapeTest(unittest.TestCase):

    def setUp(self):
        self.json = {'data': {'children': [{'data': {'preview': {
                          'images': [{'source':
                                      {'url':
                                       'url.com/some_url.png?21'}}]}}}]}}
        self.html = ('<html><head></head><body><div class="y5w1y">'
                     '<div class="hduMF"><div class="_31wG7 _3YIV2">'
                     'Some text</div><div class="_114MZ"> Some text'
                     '</div><div class="_287Ma tPMQE"><a href="url.com'
                     '/photos/some_url/download?force=true"></a></div>'
                     '</div></div></body></html>')

    def test_get_image_links_list(self):
        old_reddit = plugins.reddit_scraper
        old_unsplash = plugins.unsplash_scraper
        old_desktoppr = plugins.desktoppr_scraper
        plugins.unsplash_scraper = lambda **x: [1,2]
        plugins.reddit_scraper = lambda **x: [7,8]
        plugins.desktoppr_scraper = lambda **x: [3,4]

        self.assertEqual(
          scrape.get_image_links_list(
              ['reddit'], subbreddits='r/something'),
          [ 7, 8])
        self.assertEqual(
          scrape.get_image_links_list(
              ['unsplash']),[1, 2])
        self.assertEqual(
          scrape.get_image_links_list(
              ['desktoppr']),
              [3,    4])

        plugins.reddit_scraper = old_reddit
        plugins.unsplash_scraper = old_unsplash
        plugins.desktoppr_scraper = old_desktoppr

    def test_reddit_image_links(self):
        plugins.make_json = lambda x: {
            'data': {'children': [{'data': {'preview': {
                'images': [{'source':
                            {'url':
                             'url.com/some_url.png?21'}}]}}}]}}
        self.assertEqual(
          plugins.reddit_scraper(subreddits = ['r/some']),
            ['url.com/some_url.png?21'])

        # No preview, sometimes children's list has no key Preview
        self.json['data']['children'].append({})
        self.assertEqual(
          plugins.reddit_scraper(subreddits = ['r/some']),
            ['url.com/some_url.png?21'])

        # No preview images
        json_1 = self.json
        json_1['data']['children'] = [{}]
        plugins.make_json = lambda x: json_1
        self.assertEqual(plugins.reddit_scraper(subreddits = ['r/some']), [])

        # Bad Json, mostly in case of bad internet
        json_1 = self.json
        json_1['data'] = {}
        plugins.make_json = lambda x: json_1
        self.assertEqual(plugins.reddit_scraper(subreddits = ['r/some']), [])

    def test_unsplash_image_links(self):
        old_make_soup = plugins.make_soup
        plugins.make_soup = lambda x: BeautifulSoup(self.html, "html.parser")
        self.assertEqual(
          plugins.unsplash_scraper(),
          ['url.com/photos/some_url/download?force=true'])

        # Bad html file, mostly in case of bad internet
        html = '<html></html>'
        plugins.make_soup = lambda x: BeautifulSoup(html, "html.parser")
        self.assertEqual(plugins.unsplash_scraper(), [])
        plugins.make_soup = old_make_soup

    def test_desktoppr_image_links(self):
        plugins.make_json = lambda x: {
            'response': [{
                    'image': {
                        'url': 'example.com/example.jpg'
                    }
            }]
        }

        self.assertEqual(
          plugins.desktoppr_scraper(no_of_images=1),
          ['example.com/example.jpg'])
