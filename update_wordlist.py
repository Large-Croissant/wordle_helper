import requests
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta

URL = "https://www.stadafa.com/2021/09/every-worlde-word-so-far-updated-daily.html"

def get_and_parse(link: str, session: requests.Session) -> BeautifulSoup:
    page = session.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def main():
    s = requests.Session()
    parsed = get_and_parse(URL, s)
    print("Webpage parsed")
    body_sec = parsed.find("div", attrs={"id": "post-body-7839294531017604865"})
    print("<div> found")
    all_p = body_sec.find_all("p")
    print("All <p> found")
    words = []
    for p in all_p:
        p_text = p.get_text()
        try:
            possible = re.search(r"(?<=\d\.\s)(\w{5})", p_text).group()
            words.append(possible.lower())
        except:
            pass
    print("All <p> parsed")
    filename = f"./used_words.txt [up to {date.today() - timedelta(days=1)}]"
    with open(filename, "w") as file:
        for word in words:
            file.write(f"{word}\n")
    print(f"Words written to {filename}")

if __name__ == "__main__":
    main()