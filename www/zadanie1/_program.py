from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md
from googlesearch import search

mysite = "https://bartekrozenberg.github.io/BartekRozenberg.io-main/www/zadanie1/pharaohs"
pharaohs_page = "www/zadanie1/index.md"

url = "https://pharaoh.se/ancient-egypt/dynasty/18/"
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.content, "html.parser")

def create_king_page(king_name):
    pass

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
        file.write(f"- [{king[0]}: {king[1]}]({mysite}/{king[1]})\n")
        create_king_page(king[1])