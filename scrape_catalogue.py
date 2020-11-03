import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sys
sys.setrecursionlimit(10000)


url = "https://www.mcsweeneys.net/articles/the-complete-listing-so-far-atrocities-1-963"
def get_page(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    return soup


def scrape_legend(soup):
    legend = soup.find("p", style="padding-left:4em;")
    legend_dict = {'img_src': []}

    for i in legend.find_all("img"):
        legend_dict['img_src'].append(i.get("src"))

    legend_dict['txt'] = legend.get_text().split('\n')
    legend_df = pd.DataFrame.from_dict(data=legend_dict)

    datestamp = datetime.datetime.today().strftime("%Y-%m-%d")
    legend_df.to_csv(f"catalogue_legend_scraped_{datestamp}.csv", index=False)
    # TODO: Clean values in legend_dict['txt']

    return legend_df


soup = get_page(url)
legend_df = scrape_legend(soup)


def scrape_catalogue_list(soup):
    catalogue_dict = {'catalogue_src': [],
                      'entry_date': [],
                      'entry_html': []
                      }
    # catalogue_dict['txt'] = catalogue_list.find_all('li').get_text().split('\n')

    catalogue_list = soup.find("div", class_="article-body").find('ol')
    print(catalogue_list)

    for li in catalogue_list.find_all('li'):
        print(li.find("li"))
        while li.child.name == 'li':
            print('go one level deeper...')
            li = li.child
        print(li)

    #     print(li.prettify())
    #     for e in li.find_all("li"):
    #         catalogue_dict['catalogue_src'].append(e.get("src"))
    #
    #         entry_date = e.find("b")
    #         catalogue_dict['entry_date'].append(entry_date.get_text())
    #
    #         entry_html = entry_date.find_next_siblings("b")
    #         catalogue_dict['entry_html'].append(entry_html)
    #
    #         print(e)
    #         print(entry_date.get_text())
    #         print(entry_html)
    #         print('====================================================')
    #
    # catalogue_df = pd.DataFrame.from_dict(data=catalogue_dict)
    # print(catalogue_df)

    # print(soup.get_text())


scrape_catalogue_list(soup)
