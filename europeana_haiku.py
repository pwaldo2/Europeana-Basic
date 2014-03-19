# -*- coding: utf-8 -*-

from europeana_api import Europeana

import curses
from curses.ascii import isdigit
import nltk
from nltk.corpus import cmudict
import random
import re

#To get an API key, go here: http://europeana.eu/portal/api/registration.html
API_KEY = "pRTrsaZTD"

class EuropeanaHaikuGenerator(Europeana):
    """
    Accepts keywords to query Europeana and creats a Haiku.  Inspired by the surreal titles that appear sometimes.

    N.B. Remember to download cmudict first: nltk.download('cmudict')
    """

    def __init__(self, api_key):
        Europeana.__init__(self, api_key)
        self.cmu_dict = cmudict.dict()    
        
    def splitPunctuation(self, sentence):
        """
        Remove punctuation from the sentence
        """
        
        exclude = """!"#$%&()*+,;<=>?@[]^`{|}~./"""
        regex = re.compile('[%s]' % re.escape(exclude))
        clean = ''.join(regex.split(sentence))
        clean = clean.replace('\n', '')
        clean = clean.replace('\r\n', '')
        clean = clean.replace('\t', '')
        
        return clean
        
    def hasFiveSyllables(self, sentence):
        syllable_count = 0
        clean_sentence = self.splitPunctuation(sentence)
        for word in clean_sentence.split(' '):
            if word != None or word != u'':
                try:
                    syllable_count += self.nsyl(word)[0]
                except KeyError:  #Usually a foreign language word...or may have quotations in the title
                    return False
        
        return syllable_count == 5
        
    def hasSevenSyllables(self, sentence):
        syllable_count = 0
        clean_sentence = self.splitPunctuation(sentence)
        for word in clean_sentence.split(' '):
            if word != None or word != u'':
                try:
                    syllable_count += self.nsyl(word)[0]
                except KeyError:  #Usually a foreign language word...or may have quotations in the title
                    return False
                    
        return syllable_count == 7
        
    def getFirstFive(self, sentence):
        """
        If we don't have a pure five syllable sentence then we will grab the first seven and hope for the best!
        """
        bad_endings = ['a']
        syllable_count = 0
        clean_sentence = self.splitPunctuation(sentence)
        catch = []
        for word in clean_sentence.split(' '):
            if word != None or word != u'':
                try:
                    syllable_count += self.nsyl(word)[0]
                    catch.append(word)
                except KeyError:  #Usually a foreign language word...or may have quotations in the title
                    return False
                
                if syllable_count == 5 and catch[-1] not in bad_endings:
                    return ' '.join(catch)
                    
        return None
            
        
    def getFirstSeven(self, sentence):
        """
        If we don't have a pure seven syllable sentence then we will grab the first seven and hope for the best!
        """
        
    def makeHaiku(self, fives, sevens):
        """
        Generate some random haikus from a list of titles
        """
        
        if fives == []:
            print 'No Five Syllables Found!'
            return None
            
        if sevens == []:
            print 'No Seven Syllables Found!'
            return none
            
        poems = []
        end_range = len(fives)-1
        for line in sevens:
            line_1 = fives[random.randint(0, end_range)]
            line_2 = line
            line_3 = fives[random.randint(0, end_range)]
            
            while line_1 == line_3:  #Avoiding duplication
                line_3 = fives[random.randint(0, end_range)]
                print 'Trying...', line_3

            entry = line_1, line_2, line_3
            if entry not in poems:
                poems.append(entry)
        
        return poems
        
        
    def nsyl(self, word):
        """
        From http://www.onebloke.com/2011/06/counting-syllables-accurately-in-python-on-google-app-engine/
        
        It works by looking up the pronunciation of the word in the Carnegie Mellon University’s pronunciation dictionary 
        that is part of the Python-based Natural Language Toolkit (NLTK). This returns one or more pronunciations for the
        word. Then the clever bit is that the routine counts the stressed vowels in the word. The raw entry from the cmudict
        file for the word SYLLABLE is shown below.

        SYLLABLE 1 S IH1 L AH0 B AH0 L
        
        """
        return [len(list(y for y in x if isdigit(y[-1]))) for x in self.cmu_dict[word.lower()]]
        
    def test_haiku(self):
        """
        Searching for Laughter produces some great results!
        """
        
        fives = []
        sevens = []
        results = self.advanced_search(query='what:Laughter', keywords=None, media_type=None, language='en', year=None, use=None)
        
        for r in results["items"]:
            if self.hasFiveSyllables(r["title"][0]):
                fives.append(r["title"][0])
            elif self.hasSevenSyllables(r["title"][0]):
                sevens.append(r["title"][0])

        if fives == []:
            for r in results["items"]:
                f = self.getFirstFive(r["title"][0])
                if f:
                    fives.append(f)

        print self.makeHaiku(fives, sevens)
            
        
if __name__ == '__main__':

    EU = EuropeanaHaikuGenerator(API_KEY)
    EU.test_haiku()