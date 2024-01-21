#!/usr/bin/python3
from argparse import Action
from requests.utils import default_user_agent
from random import choice
import functools
from tqdm import tqdm

"""A module for all the miscellaneous pieces of code that are needed,
   but would make the main module look a bit clunky and cluttered. This
   includes a list of user agents to choose at random, a specialized 
   commandline argparse Action, and print decorator for formated output."""

user_agent_list = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)', 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7',
    'Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36', 'curl/7.35.0',
    'Wget/1.15 (linux-gnu)', 'Lynx/2.8.8pre.4 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.12.23')

class UserAgentAction(Action):
    def __call__(self, parser, namespace, values=None, option_string=None):
        if values == None:
            agent = RandomAgent()
        else:
            agent = values
        setattr(namespace, self.dest, agent)

def RandomAgent():
    return choice(user_agent_list)

status_codes = [200,204,301,302,307,401,403]

def pretty(func):
    '''Decorator function for output formating.'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        tqdm.write('=' * 65)
    return wrapper

def lister(exts):
    """Properly converts status codes or extenstions options
        into lists for latter use."""
    if isinstance(exts, str):
        exts = [i for i in exts.split(',')]
    elif isinstance(exts, list):
        pass
    else:
        if exts == None:
            return ['']
        else:
            raise ValueError(f"{exts} type {type(exts)} is not valid! Need string or list.")
    if any(map(lambda x: not x.isdigit(), exts)):
        if exts != ['']:
            exts = ['.'+i for i in exts]
            exts.insert(0,'')
    else:
        try:
            exts = [int(i) for i in exts]
        except ValueError:
            raise ValueError(f"Status code in {exts} is not a valid integer.")
    return exts