from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md
from duckduckgo_search import DDGS
import time
import wikipediaapi

mysite = "https://bartekrozenberg.github.io/BartekRozenberg.io/www/zadanie1"
pharaohs_page = "www/zadanie1/index.md"

url = "https://pharaoh.se/ancient-egypt/dynasty/18/"
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.content, "html.parser")

# Data for scraping from wikipedia:
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

def create_king_page(king_name):
    king_page_name = king_name.replace(" ", "_")
    king_page = f"www/zadanie1/pharaohs/{king_page_name}.md"

    time.sleep(10)
    # There are two pathological cases:
    if(king_name == "Ay"):
        king_name = "Ay (pharaoh)"
    if(king_name == "Smenkhkara"):
        king_name = "Smenkhkare"
        
    with DDGS() as ddgs:
        image_results = ddgs.images("image of " + king_name, max_results=1)
    
    if image_results and len(image_results) > 0:
        image_url = image_results[0].get("image", "")
        image_source = image_results[0].get("image") if image_results else ""
    
    king_page_wiki = wiki_wiki.page(king_name)
    if king_page_wiki.exists():
        print(king_page_wiki.fullurl)
        description = king_page_wiki.summary
        
        with open(king_page, "w") as file:
            file.write(f"# {king_name}\n\n")
            file.write(description + "\n")
            file.write(f"\n![{king_name}]({image_url})\n")
            file.write(f"\n### Source: [{king_page_wiki.fullurl}]({king_page_wiki.fullurl})\n")
            file.write(f"\n### Image: [source]({image_source})\n")
    else:
        print(f"No results found for {king_name}")


### Creating the main page with the list of pharaohs: ###

# There is general information about the 18th dynasty:
paragraphs = soup.find_all("p", limit=4)

with(open(pharaohs_page, "w")) as file:
    file.write("# The Eighteenth Dynasty of Ancient Egypt\n\n")
    
    file.write("## The New Kingdom\n")
    file.write(paragraphs[0].text + "\n")
    
    file.write("## Time of prosperity\n")
    file.write(paragraphs[1].text + "\n")
    
    file.write("## Achievements\n")
    file.write(paragraphs[2].text + "\n")
    
    file.write("## The list of Pharaohs\n")
    file.write(paragraphs[3].text + "\n")

    # There is a list of pharaohs of the 18th dynasty:
    table = soup.find("table")
    rows = table.find_all("tr")
    kings_list = []
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        kings_list.append([ele for ele in cols if ele])

    for king in kings_list:
        if len(king) == 0:
            continue
        page_name = king[1].replace(" ", "_")
        file.write(f"- [{king[0]}: {king[1]}]({mysite}/pharaohs/{page_name})\n")
        create_king_page(king[1])

    file.write(f"\n### Source: [The Eighteenth Dynasty]({url})\n")