#!/usr/bin/python3
#As it currently exists, this script needs to be run with python3 but could be modified to work with 3.0.1
#Definitely works on 3.0.1

import urllib.request
import re
import sys

class FakeFireFox(urllib.request.FancyURLopener):
    '''Pretend to be firefox so that Wikipedia will allow access'''
    version='Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def wpget(lang, title):
    '''Download a Wikipedia page'''
    return FakeFireFox().open('http://{lang}.wikipedia.org/w/index.php?title=Special%3ASearch&search={title}&go=Go'.format(title=encode_percent(title.encode()).decode().replace(' ','_'), lang=lang)).read()

def decode_percent(s):
    '''Turn URL-style %xx to proper Unicode'''
    return eval(re.sub('%(..)',r'\x\1',repr(s)))

def encode_percent(s):
    '''From Unicode to URL-style %xx'''
    return eval(re.sub(r'\\x(..)',r'%\1',repr(s)))

def rawtrans(page):
    '''Return a list of tuples (lang, title)'''
    return re.findall(br'<li class="interwiki-([^"]+)"><a href="http://\1.wikipedia.org/wiki/([^"]+)">',
                      page)

def transdict(raw):
    '''Turn output of rawtrans(page) into a lang:title dictionary'''
    return {i[0].decode():decode_percent(i[1]).decode().replace('_',' ') for i in raw}

def noargs():
    '''Run interactively'''
    d=transdict(rawtrans(wpget(input('Language code: '),input('Page title: '))))
    if d:
        print('Available language codes:')
        for key in sorted(d.keys()):
            print(key)
        print(d[input('Enter language code: ')])
    else:
        print('No translations')

def twoargs(inlang, title):
    '''List available language codes and let the user choose'''
    d=transdict(rawtrans(wpget(inlang,title)))
    if d:
        print('Available language codes:')
        for key in sorted(d.keys()):
            print(key)
        print(d[input('Enter language code: ')])
    else:
        print('No translations')

def threeargs(inlang, title, outlang):
    '''Non-interactive'''
    print(transdict(rawtrans(wpget(inlang,title)))[outlang])

# A note for the confused:
# sys.argv contains the entire command line, i.e. sys.argv[0] should be 'wptrans.py'
# (so len(sys.argv) is the number of arguments *plus one*.
if __name__=='__main__':
    if len(sys.argv)==4:
        threeargs(sys.argv[1],sys.argv[2],sys.argv[3])
    elif len(sys.argv)==3:
        twoargs(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==1:
        while True:
            noargs()
            if not input('Press enter to quit, anything else and then enter to continue\n'):
                break
    else:
        print('Wrong number of arguments')
