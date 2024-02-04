#
#
#  This file contains the Requests + BS4 shorts;
#  Avoid DRY code, its not a good practice!!!
#  Make Python3 better place for code!
#
#  Start here!
#
#
import cfscrape
import requests
from bs4 import BeautifulSoup
#
from .default_headers import DEFAULT_HEADERS
import xml.etree.ElementTree as ET

# Global Session -> avoid multiple requests
# ... and all classes can use it in one script
session = requests.Session()


class GetStaticSoup:
    '''
    ... This class return soup object from static page!
    '''

    def __new__(cls, link, custom_headers=None):

        headers = DEFAULT_HEADERS.copy()

        #  if user have custom headers,
        #  update the headers
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # return soup object from static page
        return BeautifulSoup(response.content, 'lxml')


class GetHtmlSoup:
    '''
    ... method if server return html response,
    after post requests.
    '''

    def __new__(cls, html_response):
        return BeautifulSoup(html_response, 'lxml')


class GetRequestJson:
    '''
    ... This class return JSON object from get requests!
    '''

    def __new__(cls, link, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Dacă utilizatorul are headere personalizate, actualizează headerele
        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # Parse response to JSON and return ditct oject
        try:
            json_response = response.json()
            return json_response
        except ValueError as e:
            print(f"Errors. No JSON! Details: {e}")
            return None


class PostRequestsJson:
    '''
    ... This class return JSON object from post requests!
    '''

    def __new__(cls, url, headers=None, data_raw=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if headers:
            headers.update(headers)

        response = session.post(url, headers=headers, data=data_raw)

        # Parse response to JSON and return ditct oject
        try:
            json_response = response.json()
            return json_response
        except ValueError as e:
            print(f"Errors. No JSON! Details: {e}")
            return None
class HackCloudFlare:
    '''
    ... this method can help you avoid CloudFlare protection.
    Is not a hack, but useful tool.
    '''

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if headers is requiered
        if custom_headers:
            headers.update(custom_headers)

        scraper = cfscrape.create_scraper()

        return BeautifulSoup(scraper.get(url).content, 'lxml')
    
class GetXMLObject:
    '''
    this class will return data from XML stored in a list
    '''
    
    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if custom headers
        if custom_headers:
            headers.update(custom_headers)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return ET.fromstring(response.text)