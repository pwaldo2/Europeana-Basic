# -*- coding: utf-8 -*-

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
        args = {'wskey': api_key, 
                'query': query, 
                'start': '1', 
                'rows': '12', 
                'profile': 'standard'}
                
        return requests.get(self.search_url, params=args).json()

    def advanced_search(self, query, keywords=None, media_type=None, language=None, year=None, use=None):
        """
        Adding in some advanced query functionality
        
        TO DO:
        Use is not working correctly
        Document list of options
        """
        args = {'wskey': self.api_key, 
                'query': query,
                'qf': [],
                'start': '1', 
                'rows': '24', 
                'profile': 'standard'}
                
        if keywords and type(keywords) == list:
            for key in keywords:
                args['qf'].append(key)
        
        if keywords and type(keywords) != list:
            print 'Keywords must be a list type'
            raise AttributeError
                
        if media_type:
            args['qf'].append('TYPE:%s' % (media_type))
        
        if language:
            args['qf'].append('LANGUAGE:%s' % (language))
            
        if year:
            args['qf'].append('YEAR:%s' % (year))
        
        if use:
            args['qf'].append('REUSABILITY:permission')
            
        return requests.get(self.search_url, params=args).json()
        
    def mona_lisa(self):
        """
        Get back 12 results for the Mona Lisa:
        API: http://europeana.eu/api/v2/search.json?wskey=SECRET&query=Mona+Lisa&start=1&rows=12&profile=standard+portal+facets+breadcrumb+minimal+params
        Web: http://europeana.eu/portal/search.html?query=Mona+Lisa&rows=12
        """
        return self.simple_search('Mona Lisa')
        
    def test_advanced(self):
        """
        Test advanced search.
        API 1:http://europeana.eu/api/v2/search.json?wskey=SECRET&query=Brussels&qf=TYPE:SOUND&rows=24&profile=standard+portal+facets+breadcrumb+minimal+params
        Web 1: http://europeana.eu/portal/search.html?query=Brussels&qf=City&qf=TYPE:SOUND&rows=24
        
        API 2: http://europeana.eu/api/v2/search.json?wskey=SECRET&query=Brussels&qf=TYPE:SOUND&qf=LANGUAGE:fr&qf=YEAR:2009&rows=24&profile=standard+portal+facets+breadcrumb+minimal+params
        Web 2: http://europeana.eu/portal/search.html?query=Brussels&qf=TYPE:SOUND&qf=LANGUAGE:fr&qf=YEAR:2009&rows=24
        """
        
        print self.advanced_search(query='Brussels', keywords=['City'], media_type='SOUND')
        print self.advanced_search(query='Brussels', media_type='SOUND', language='fr', year='2009')


if __name__ == '__main__':
    
    EU = Europeana(API_KEY)
    #mona_lisa = EU.mona_lisa()
    print EU.test_advanced()

    #print "Found %d items for Mona Lisa\n" % (mona_lisa["itemsCount"])
    #
    #for i in mona_lisa["items"]:
    #    print "Title: ", i["title"][0]
    #    print "Link: ", i["link"]
    #    try:
    #        print "Image: ", i["edmPreview"][0]
    #    except KeyError:
    #        print "Image: None"
    #    print '\n'
