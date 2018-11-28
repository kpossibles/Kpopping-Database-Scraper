import requests
import csv
from bs4 import BeautifulSoup

url = "https://kpopping.com/profiles/the-idols"
page = requests.get(url)

#pass the HTML to Beautifulsoup.
soup = BeautifulSoup(page.content,'html.parser')

#get the HTML of the table called site Table where all the links are displayed
main_table = soup.find("div", attrs={'class': 'widget shadowed pink-bordered'})
idols = main_table.find_all('a', href=True)

#from each link extract the text of link and the link itself
#List to store a dict of the data we extracted
idol_links = []
for link in idols:
    url = "https://kpopping.com" + link['href']
    idol_links.append(url)

# Create a file to write to, add headers row
f = csv.writer(open('z-artist-names.csv', 'w', encoding="utf-8"))
f.writerow(['Stage Name', 'Real Name', 'Group', 'Instagram', 'Profile Pic', 'Kpoppin Profile'])

idol_data = []
for url in idol_links:
    page1 = requests.get(url)
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    main_table1 = soup1.find(
        "div", attrs={'class': 'col encyclopedia-sidebar-picture'})
    data = soup1.find(
        "div", attrs={'class': 'data'})
    stage_name = data.find('h1').text.strip()
    name = data.find('h2').text.strip()
    group = data.find("td", text="Group(s)")
    if group != None:
        group = group.find_next_sibling("td").text
    else:
        group = ""
    profilepic = "https://kpopping.com" + main_table1.find('img')['src']
    instagram = soup1.find(
        "a", attrs={'class': 'fab fa-instagram act'})
    if instagram != None: 
        instagram = instagram['href']
    else:
        instagram = ""
    
    record = {
        'stage_name': stage_name,
        'real_name': name,
        'group': group,
        'instagram': instagram,
        'profilepic': profilepic,
        'url': url
    }
    idol_data.append(record)
    f.writerow([stage_name, name, group, instagram, profilepic, url])
    print('.', end='', flush=True)

#print(idol_data)
