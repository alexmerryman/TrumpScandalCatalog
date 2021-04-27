import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import uuid
import sys
sys.setrecursionlimit(10000)


def get_page(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    return soup


def scrape_legend(soup):
    legend = soup.find("p", style="padding-left:4em;")
    legend_dict = {'img_src': []}

    for i in legend.find_all("img"):
        legend_dict['img_src'].append(i.get("src"))

    legend_dict['category'] = legend.get_text().split('\n')

    scrape_timestamp = datetime.datetime.utcnow()
    legend_dict['scrape_timestamp'] = scrape_timestamp

    legend_df = pd.DataFrame.from_dict(data=legend_dict)

    datestamp = datetime.datetime.today().strftime("%Y-%m-%d")
    legend_df.to_csv(f"legend_scraped_{datestamp}.csv", index=False)

    return legend_df


def scrape_catalogue_list(soup):

    catalogue_scraped = []

    def concat_entry_parts(accept_tags, init_entry_part, init_entry_part_tag):
        entry_part = init_entry_part
        entry_part_tag = init_entry_part_tag

        entry_parts_list = []

        while (entry_part_tag in accept_tags) and (entry_part.next_sibling is not None):  # get all next siblings with acceptable tags
            # skip the date entry part
            if entry_part_tag == 'b':
                pass
            else:
                entry_parts_list.append(entry_part)

            # move on to next sibling
            entry_part = entry_part.next_sibling
            print("NEXT SIBLING:", entry_part)
            print("NEXT SIBLING TAG:", entry_part.name)
            if entry_part.next_sibling is None:
                pass
            else:
                entry_part_tag = entry_part.name

        return entry_parts_list

    # TODO: wrap in try/excepts
    catalogue_list = soup.find("div", class_="article-body").find("ol")
    all_entries_html = str(catalogue_list.find_all("li", recursive=True)[0])
    all_entries_html_list = all_entries_html.split("<br/>")
    all_entries_html_list = list(set(all_entries_html_list) - set("\n"))

    for li in all_entries_html_list:
        li = li.replace(r"\n", "")
        li_soup = BeautifulSoup(li, 'html.parser')
        entry_date = li_soup.find("b")
        entry_bullets = li_soup.find_all("img")

        try:
            entry_text = li_soup.find("li").get_text()
        except Exception as e:
            entry_text = f"Error - unable to extract text ({e})"

        try:
            entry_links = li_soup.find("li").find_all("a")
            entry_links_list = [a["href"] for a in entry_links]
        except Exception as e:
            entry_links_list = ['No links scraped.']

        try:
            entry_date_text = entry_date.get_text()
        except Exception as e:
            entry_date_text = f"Error - unable to extract date as ext ({e})"

        # accept_tags = ["a", "b", "i", "span", None]
        # init_entry_part = entry_date
        # init_entry_part_tag = init_entry_part.name
        # entry_parts_list = concat_entry_parts(accept_tags, init_entry_part, init_entry_part_tag)

        print("=============================================================================================")
        print(li)
        print("ENTRY TEXT:", entry_text)
        print("DATE:", entry_date)
        print("BULLETS:", entry_bullets)
        print("ENTRY LINKS:", entry_links_list)
        # print(entry_parts_list)

        entry_uuid = uuid.uuid4()
        entry_bullet_src = [s["src"] for s in entry_bullets]

        scrape_timestamp = datetime.datetime.utcnow()

        entry_dict = {"entry_uuid": entry_uuid,
                      "legend_bullet_src": entry_bullet_src,
                      "entry_date": entry_date_text,
                      "entry_text": entry_text,
                      "entry_links": entry_links_list,
                      "scrape_timestamp": scrape_timestamp,
                      }

        catalogue_scraped.append(entry_dict)


    return catalogue_scraped


url = "https://www.mcsweeneys.net/articles/the-complete-listing-so-far-atrocities-1-963"
soup = get_page(url)

legend_df = scrape_legend(soup)

catalogue_scraped = scrape_catalogue_list(soup)
catalogue_df = pd.DataFrame(catalogue_scraped)
print(catalogue_df.head())

datestamp = datetime.datetime.today().strftime("%Y-%m-%d")
catalogue_df.to_csv(f"catalogue_scraped_{datestamp}.csv", index=False)

