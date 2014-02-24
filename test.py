"""
February 23, 2014

Europeana Proof of Concept Example

by Patrick Waldo
"""
import json
import urllib2
import requests

#To get an API key, go here: http://europeana.eu/portal/api/registration.html
API_KEY = "SECRET"

class Europeana:
    def __init__(self, api_key):
        self.api_key = api_key
        
        #Search and Retreive Records
        self.search_url = 'http://www.europeana.eu/api/v2/search.json'
        self.record_url = 'http://www.europeana.eu/api/v2/record.json'
        self.suggestions_url = 'http://www.europeana.eu/api/v2/suggestions.json'
        self.opensearch_url = 'http://www.europeana.eu/api/v2/opensearch.rss'
        
        #MyEuropeana Actions
        self.profile_url = 'http://www.europeana.eu/api/v2/profile.json'
        self.saveditem_url = 'http://www.europeana.eu/api/v2/saveditem.json'
        self.tag_url = 'http://www.europeana.eu/api/v2/tag.json'
        self.savedsearch_url = 'http://www.europeana.eu/api/v2/savedsearch.json'
        
        
    def simple_search(self, query):
        """
        Sets up the basic URL parameters for the Europeana API.  Returns a JSON data structure.
        JSON Keys: [u'apikey', u'success', u'items', u'itemsCount', u'action', u'requestNumber', u'totalResults']
        """
        args = {'wskey': self.api_key, 
                'query': query, 
                'start': '1', 
                'rows': '12', 
                'profile': 'standard'}
                
        return requests.get(self.search_url, params=args).json()

              
    def mona_lisa(self):
        """
        Get back 12 results for the Mona Lisa:
        API: http://europeana.eu/api//v2/search.json?wskey=pRTrsaZTD&query=Mona+Lisa&start=1&rows=12&profile=standard+portal+facets+breadcrumb+minimal+params
        Web: http://europeana.eu/portal/search.html?query=Mona+Lisa&rows=12
        """
        return self.simple_search('Mona Lisa')


if __name__ == '__main__':
    
    EU = Europeana(API_KEY)
    mona_lisa = EU.mona_lisa()

    print "Found %d items for Mona Lisa\n" % (mona_lisa["itemsCount"])
    
    for i in mona_lisa["items"]:
        print "Title: ", i["title"][0]
        print "Link: ", i["link"]
        try:
            print "Image: ", i["edmPreview"][0]
        except KeyError:
            print "Image: None"
        print '\n'
