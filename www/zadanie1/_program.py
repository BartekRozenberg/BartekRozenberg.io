## run command: python3 www/zadanie1/_program.py

from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md
from duckduckgo_search import DDGS
import time
import wikipediaapi

mysite = "https://bartekrozenberg.github.io/BartekRozenberg.io/www/zadanie1"
pharaohs_page = "www/zadanie1/index.md"

responsive_css = """
html, body {{ height: 100%; margin: 0; }}
body {{ background: url({bg}) no-repeat center center fixed; background-size: cover; font-family: Arial, sans-serif; color: #FFFFFF; }}
.content {{ padding: 20px; min-height: 100vh; background-color: rgba(0, 0, 0, 0.55); }}
h1 {{ font-size: 2.5rem; }}
p {{ font-size: 1.13rem; }}
a {{ color:rgb(230, 223, 173); }}
/* Tablet devices */
@media (max-width: 768px) {{
  .content {{ padding: 15px; }}
  h1 {{ font-size: 2rem; }}
  p {{ font-size: 1rem; }}
}}
/* Mobile devices */
@media (max-width: 480px) {{
  .content {{ padding: 10px; }}
  h1 {{ font-size: 1.5rem; }}
  p {{ font-size: 0.9rem; }}
}}
""".strip()

# Data for scraping from wikipedia:
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)


# Getting the image for the background used in king pages:
with DDGS() as ddgs:
    image_results = ddgs.images("valley of kings mountain", max_results=1)

king_background = image_results[0].get("image", "")
background_king_source = image_results[0].get("image") if image_results and len(image_results) > 0 else ""

def create_king_page(king_name):
    king_page_name = king_name.replace(" ", "_")
    king_page = f"www/zadanie1/pharaohs/{king_page_name}.md"

    time.sleep(10) # Not to get 202 ratelimit error.
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
    
    king_page_content = f"""
    <html>
    <head>
      <meta charset="UTF-8">
      <title>{king_name}</title>
      <style>
        {responsive_css.format(bg=king_background)}
      </style>
    </head>
    <body>
      <div class="content">
        <h1>{king_name}</h1>
    """
    
    page_ending = f"""
        </div>
      </body>
    </html>
    """
    
    king_page_wiki = wiki_wiki.page(king_name)
    if king_page_wiki.exists():
        print(king_page_wiki.fullurl)
        description = king_page_wiki.summary
        king_page_content += f'<p>{description}\n</p>'
        king_page_content += f'<img src="{image_url}" alt="{king_name}" style="width: 100%; max-width: 400px;">'
        king_page_content += f'<p><em>Source of information: <a href="{king_page_wiki.fullurl}" target="_blank">{king_page_wiki.fullurl}</a></em></p>'
        king_page_content += f'<p><em>Image source: <a href="{image_source}" target="_blank">{image_source}</a></em></p>'
        king_page_content += f'<p><em>Background image source: <a href="{background_king_source}" target="_blank">{background_king_source}</a></em></p>'
        king_page_content += page_ending
        
        with open(king_page, "w") as file:
            file.write(king_page_content.strip())
    else:
        print(f"No results found for {king_name}")


### Creating the main page with the list of pharaohs: ###

# Getting the image for the background:
time.sleep(10)
with DDGS() as ddgs:
    image_results = ddgs.images("karnak egypt 4k wallpapers statues", max_results=1)

background_url = image_results[0].get("image", "")
background_source = image_results[0].get("image") if image_results and len(image_results) > 0 else ""

print("Background url: ", background_url)
print("Background source: ", background_source)

url = "https://pharaoh.se/ancient-egypt/dynasty/18/"
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.content, "html.parser")
# There is general information about the 18th dynasty:
paragraphs = soup.find_all("p", limit=4)


page_beginning = f"""
<html>
  <head>
    <meta charset="UTF-8">
    <title>The Eighteenth Dynasty of Ancient Egypt</title>
    <style>
      {responsive_css.format(bg=background_url)}
    </style>
  </head>
  <body>
    <div class="content">
      <h1>The Eighteenth Dynasty of Ancient Egypt</h1>
      <h2>The New Kingdom</h2>
      <p>{paragraphs[0].text}</p>
      <h2>Time of prosperity</h2>
      <p>{paragraphs[1].text}</p>
      <h2>Achievements</h2>
      <p>{paragraphs[2].text}</p>
"""

king_list_to_file = f"""
      <h2>The list of Pharaohs</h2>
      <p>{paragraphs[3].text}</p>
        <u1>
"""

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
    king_list_to_file += f'        <li><a href="pharaohs/{page_name}">{king[1]}</a></li>\n'
    create_king_page(king[1])

page_end = f"""
        </u1>
      <br>
      <p><em>Source of information: <a href="{url}" target="_blank">{url}</a></em></p>
      <p><em>Background image source:
         <a href="{background_source}" target="_blank">{background_source}</a>
      </em></p>
    </div>
  </body>
</html>
"""

complete_page = (page_beginning + king_list_to_file + page_end).strip()

with(open(pharaohs_page, "w")) as file:
    file.write(complete_page)
