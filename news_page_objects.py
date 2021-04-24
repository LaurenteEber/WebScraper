import bs4
import requests

from common import config

class NewsPage:
    
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]    #news_sites es la primera llave del diccionario
        self._queries = self._config['queries']
        self._html = None
        
        self._visit(url)        

    def _select(self, query_string):
        return self._html.select(query_string)
        
    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status() #mÃƒÂ©todo que arroja error si la solicitud no fue concluida correctamente 
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')

class HomePage(NewsPage):      #Se estÃ¡ diciendo que HomePage extiende NewsPage
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

        
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)
        return set(link['href'] for link in link_list) #utilizamos set para eliminar elementos repetidos
            
        
class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
            
# Definiendo la manera como accederemos a la noticia y a su cuerpo

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''
    
    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''