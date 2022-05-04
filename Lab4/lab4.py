from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://www.ukrinform.ua"
URL = f"{BASE_URL}/tag-povitrana-trivoga" 

page = get(URL)
soup = BeautifulSoup(page.content,  "html.parser")

with open("alert.txt", "w", encoding="UTF=8") as file:
    news_list = soup.find(class_="restList")
    for article in news_list.find_all("article"):
        section = article.find("section")
        time = section.find("time")
        data = time.get("datetime")
        time = time.find(text=True, recursive=False)

        a = section.find("a")
        news_link = BASE_URL + a.get("href")
        news_title = a.find(text=True, recursive=False)
        file.write(f"Дата та час: {data} - {time}\n Назва: {news_title}\n Посилання: {news_link}\n\n")
