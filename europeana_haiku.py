import curses
from curses.ascii import isdigit
import nltk
from nltk.corpus import cmudict

class EuropeanaHaikuGenerator:
    """
    Accepts keywords to query Europeana and creats a Haiku.

    N.B. Remember to download cmudict first: nltk.download('cmudict')
    """

    def __init__(self):
        self.cmu_dict = cmudict.dict()    
