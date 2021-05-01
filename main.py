import argparse
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.INFO)
import re       #mรณdulo de expresiones regulares

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import news_page_objects as news
from common import config

logger = logging.getLogger(__name__)
# Primera expresión regular:
is_well_formed_link = re.compile(r'^https?://.+/.+$')
        # r indica a python que lo que sigue es un string
        # el ^ da el inicio de la palabra
        # el patron es "http", con 's' opcional
        # .+ significa que tenga por lo menos una letra
        # $ significa que termina el patron
        # Por ejemplo: https://exmaple.com/hell
# Segunda expresión regular:
is_root_path = re.compile(r'^/.+$')  # Ejemplo de match: /some-text

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    
    logging.info('Beginning scraper for {}'.format(host))
    homepage = news.HomePage(news_site_uid, host)
    
    articles = []
    for link in homepage.article_links:
        # print(link) en lugar de inprimir
        article = _fetch_article(news_site_uid, host, link) # nos permitirรก construir un link correcto a acceder
        
        if article:
            logger.info('Article feteched!!')
            articles.append(article)
            print(article.title)
    
    print(len(articles))
            
def _fetch_article(news_site_uid, host, link):
    logger.info('Start feching article at {}'.format(link))
    
    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except(HTTPError, MaxRetryError) as e:
        logger.warning('Error while fechting the article', exc_info=False)
    # HTTPError es cuando encuentra la páagina, el url no existe 
    # MaxRetryError cuando se entra en un loop infito de intentos de engresar a una web
    
    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None
    
    return article
    
    
def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{url}'.format(host=host, url=link)
    
        
         
    
if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Scrapper News sites')
    
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help = 'The news site that you want to scrape',
                        type = str,
                        choices = news_site_choices)
    #print(news_site_choices)                    
    args = parser.parse_args()
    #print(args.news_site)
    _news_scraper(args.news_site)