from cgitb import strong
from requests import get
from bs4 import BeautifulSoup
from sqlite3 import connect 

BASE_URL = "https://kubg.edu.ua/"  #Головна сторінка університету
URL = f"{BASE_URL}/структура/instytuty-ta-fakultety"   #Інститути та кафедри
URL_1 = f"{BASE_URL}/prouniversitet/vizytivka/rektorat/dyrektory"   #Директори та декани
URL_2 = f"{BASE_URL}/prouniversitet/vizytivka/rektorat/pomichnyk-rektora"   #Помічник Ректора
URL_3 = f"{BASE_URL}/prouniversitet/vizytivka/rektorat/prorektory"       #Проректори

connection = connect("program1.db")
cursor = connection.cursor()

page = get(URL)

soup = BeautifulSoup(page.content,  "html.parser")


with open("univ.txt", "w", encoding="UTF=8") as file:
    name_page = get(URL)
    name_soup = BeautifulSoup(name_page.content, "html.parser")
    name_list = name_soup.find(class_="tz_breadcrumb")
    h1 = name_list.find("h1")
    name_title = h1.find(text=True, recursive=False)
    file.write(f"{name_title}\n")
    print(name_title)
    fac_list = soup.find(class_="item-795 deeper parent")
    for li in fac_list.find_all("li"):
            a = li.find("a")
            link = a.get("href")
            fac_name = a.find(text=True, recursive=False)
            file.write(f"{fac_name} - {link}\n ")
            dep_link = BASE_URL+ a.get("href")
            faculty = {
            "name": fac_name,
            "url": link,
            "id": []
            }
           # print(fac_name)
           # print(link)

            for f in cursor.execute(
            "SELECT id FROM univers WHERE name=? AND url=?",
            [faculty["name"], faculty["url"]]
        ):
             faculty["id"] = f[0]

            if not faculty.get("id"):
             cursor.execute(
                "INSERT INTO univers (name, url) VALUES (?,?)",
                [faculty["name"], faculty["url"]]
            )
            connection.commit()
            for f in cursor.execute(
                "SELECT id FROM univers WHERE name=? AND url=?",
                [faculty["name"], faculty["url"]]
            ):
                faculty["id"] = f[0]


    staff_page_1 = get(URL_1)
    staff_soup_1 = BeautifulSoup(staff_page_1.content,"html.parser")
    staff_list_1 = staff_soup_1.find(class_="SPListing")
    h3 = staff_list_1.find("h3")
    staff_title_1 = h3.find(text=True, recursive=False)
    file.write(f"\n{staff_title_1}\n")
    print(staff_title_1)
    for div in staff_list_1.find_all("div",class_="spEntriesListTitle"):
        staff_1 = div.find("a",text=True, recursive=False).text
        file.write(f"{staff_1}\n ")
        
        
        # print(staff_1)
                
    id=-1
    for a in cursor.execute(
    "SELECT id FROM adm WHERE name=?",
                    [staff_1,]
                ):
                    id=a[0]

    if id == -1:
                    cursor.execute(
                        "INSERT INTO adm (name) VALUES (?,?)",
                        [staff_1]
                    )
                    connection.commit()

    staff_page_2 = get(URL_2)
    staff_soup_2 = BeautifulSoup(staff_page_2.content,"html.parser")
    staff_list_2 = staff_soup_2.find(class_="SPListing")
    for div in staff_list_2.find_all("div",class_="spEntriesListTitle"):
        staff_2 = div.find("a",text=True, recursive=False).text
        file.write(f"{staff_2}\n ")

        # print(staff_2)
        id=-1
        for a in cursor.execute(
                    "SELECT id FROM adm WHERE name=?",
                    [staff_2,]
                ):
                    id=a[0]

        if id == -1:
                    cursor.execute(
                        "INSERT INTO adm (name) VALUES (?,?)",
                        [staff_2]
                    )
                    connection.commit()


        staff_page_3 = get(URL_3)
        staff_soup_3 = BeautifulSoup(staff_page_3.content,"html.parser")
        staff_list_3 = staff_soup_3.find(class_="SPListing")

        for div in staff_list_3.find_all("div",class_="spEntriesListTitle"):
            staff_3 = div.find("a",text=True, recursive=False).text
            file.write(f"{staff_3}\n ")
        
        # print(staff_3)

        id=-1
        for a in cursor.execute(
                    "SELECT id FROM adm WHERE name=?",
                    [staff_3,]
                ):
                    id=a[0]

        if id == -1:
                    cursor.execute(
                        "INSERT INTO adm (name) VALUES (?,?)",
                        [staff_3]
                    )
                    connection.commit()

                
    connection.close()
