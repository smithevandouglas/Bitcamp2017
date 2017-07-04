import urllib.request as request
import bs4 as bs

request_the_verge = request.Request("http://www.theverge.com/science")
sauce_the_verge = request.urlopen(request_the_verge).read().decode('utf-8')
soup = bs.BeautifulSoup(sauce_the_verge, 'html.parser')


def get_article_urls(soup_object):
    list_of_urls = soup.find_all('a')
    list_of_a_tag_hrefs = []
    final_list_of_urls = []
    for item in list_of_urls:
        list_of_a_tag_hrefs.append(item.get('href'))
    for element in list_of_a_tag_hrefs:
        if element[:27] == 'http://www.theverge.com/201':
            if element in final_list_of_urls:
                pass
            else:
                final_list_of_urls.append(element)
        else:
            pass

    return final_list_of_urls


def get_article_title(article_url):
    request_article = request.Request(article_url)
    sauce_article = request.urlopen(request_article).read().decode('utf-8')
    soup_article = bs.BeautifulSoup(sauce_article, 'html.parser')
    article_title = soup_article.find('title').string
    article_title_string = ''
    char = 0
    while article_title[char] != '-':
        article_title_string = article_title_string + article_title[char]

    return article_title_string[:-1]


def get_comment_counts(list_object):
    tuple_list = []
    for item in list_object:
        request_article = request.Request(item)
        sauce_article = request.urlopen(request_article).read().decode('utf-8')
        chickennoodle = bs.BeautifulSoup(sauce_article, 'html.parser')
        comment_count = chickennoodle.find_all('span', data-ui="comment-data").string
        tuple_holder = (item, get_article_title(item), int(comment_count))
        tuple_list.append(tuple_holder)

    return tuple_list
