# coding: utf-8

import urllib.request as request
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import operator
import bs4 as bs

ps = PorterStemmer()

request_washington_post = request.Request('https://www.washingtonpost.com/')
sauce_washington_post = request.urlopen(request_washington_post).read().decode('utf-8')
tokenized = word_tokenize(sauce_washington_post)

no_no_list = ['//www.washingtonpost.com/terms-of-service/2011/11/18'
              '/gIQAldiYiN_story.html',
              '//www.washingtonpost.com/privacy-policy/2011/11/18/'
              'gIQASIiaiN_story.html',
              '//www.washingtonpost.com/rss-terms-of-service/2012/01/16/'
              'gIQAadFYAQ_story.html',
              '//www.washingtonpost.com/'
              'how-can-i-opt-out-of-online-advertising-cookies/2011/11/18/'
              'gIQABECbiN_story.html']


# FOR WASHINGTON POST
def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i) < 128)


# FOR WASHINGTON POST
def translate_comment_count_to_int(integer_string):
    base_num = ''
    real_num = 0
    if 'K' in integer_string:
        for char in integer_string:
            if char != 'K':
                base_num = base_num + char
            else:
                real_num = float(base_num)
                real_num *= 1000
    elif '+' in integer_string:
        for char in integer_string:
            if char != '+':
                base_num = base_num + char
        real_num = int(float(base_num))

    return real_num


# FOR WASHINGTON POST
def get_article_urls(source_code_token):
    url = ''
    list_of_urls = []
    https_tag = False
    colon_tag = False
    for item in source_code_token:
        if item == 'https' and not colon_tag:
            https_tag = True
        elif item == ':' and https_tag:
            colon_tag = True
        elif https_tag and colon_tag and item != '\'\'':
            url = url + item
        elif item == '\'\'':
            list_of_urls.append(url)
            url = ''
            https_tag = False
            colon_tag = False

    real_list = []
    for thing in list_of_urls:
        if 'story.html' in thing and thing not in no_no_list:
            real_list.append(thing)

    real_list = ['https:' + entry for entry in real_list]

    return real_list


# FOR WASHINGTON POST
def get_comment_counts(list_input):
    list_of_triples = []
    for headline in list_input:
        request_article = request.Request(headline)
        sauce = request.urlopen(request_article).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        title = soup.find('h1', itemprop="headline")
        comment_count = soup.find('span', "echo-counter")
        triple = (headline, str(remove_non_ascii_1(title.text)),
                translate_comment_count_to_int(str(comment_count.text)))
        if triple in list_of_triples:
            pass
        else:
            list_of_triples.append(triple)

    return list_of_triples


# FOR WASHINGTON POST
def produce_final_dictionary():
    list_of_urls = get_article_urls(tokenized)
    return get_comment_counts(list_of_urls[:20])

print(produce_final_dictionary())
