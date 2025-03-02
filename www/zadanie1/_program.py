from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md
from googlesearch import search

url = "https://visit.podlaskie.eu/turystyka/podlaskie-parki-krajobrazowe/"
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.content, "html.parser")


dane_podstron = {}

# Wyciągnij wszystkie tagi <h2> wraz z ich treściami i paragrafami pod nimi
with open("headings_and_paragraphs.md", "w", encoding="utf-8") as file:
    h2_tags = soup.find_all('h2')
    for tag in h2_tags:
        nazwa_parku = tag.get_text(strip=True)
        dane_podstron[nazwa_parku] = []
        file.write(f"## {tag.get_text(strip=True)}\n\n")
        # Znajdź wszystkie paragrafy pod danym nagłówkiem <h2>
        for sibling in tag.find_next_siblings():
            if sibling.name == "h2":
                break
            elif sibling.name == 'p':
                file.write(f"{sibling.get_text(strip=True)}\n\n")
            elif sibling.name != 'figure':
                dane_podstron[nazwa_parku].append(sibling.get_text(strip=True))
        # Szukamy linku do strony o parku:
        for url_parku in search(f"{nazwa_parku}", stop=1):
            print(f"Znaleziono link do strony o {nazwa_parku}: {url_parku}")
            file.write(f"[Więcej informacji: ](<{url_parku}>)\n\n")

# Dla każdego parku krajobrazowego zapisz dane do pliku:
for nazwa_parku, dane in dane_podstron.items():
    with open(f"{nazwa_parku}.md", "w", encoding="utf-8") as file:
        file.write(f"# {nazwa_parku.replace('_', ' ').title()}\n\n")
        for dana in dane:
            file.write(f"{dana}\n\n")

print("Tagi <h2> i ich paragrafy zostały zapisane do pliku headings_and_paragraphs.md")

# Convert the modified HTML to Markdown
markdown_content = md(str(soup))

# Save the Markdown content to a file
with open("index.md", "w", encoding="utf-8") as file:
    file.write(markdown_content)

print("Zawartość strony została zmodyfikowana i zapisana do pliku index.md")