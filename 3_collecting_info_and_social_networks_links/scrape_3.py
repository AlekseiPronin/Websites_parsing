import requests
import lxml
from bs4 import BeautifulSoup
import json

headers = {
    'accept': '*/*',
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Mobile Safari/537.36'
}


persons_url_list = []


for i in range(0, 740, 20):
    url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}'
    print(url)

    # sending request
    q = requests.get(url, headers=headers)
    result = q.content

    soup = BeautifulSoup(result, 'lxml')

    # collecting persons' data
    persons = soup.find_all(class_='bt-open-in-overlay')

    for person in persons:
        person_page_url = person.get('href')
        persons_url_list.append(person_page_url)

# saving persons' links into file
with open('persons_url_list.txt', 'a', encoding="utf-8-sig") as file:
    for line in persons_url_list:
        file.write(f'{line}\n')



with open('persons_url_list.txt', encoding="utf-8-sig") as file:

    # making a list of links and stripping just in case
    lines = [line.strip() for line in file.readlines()]

    # creating dict to store persons' data
    data_dict = []
    # counter for the final data saving into json
    count = 0

    for line in lines:
        q = requests.get(line)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')

        # getting person's name and party
        person = soup.find(class_='bt-biografie-name').find('h3').text
        person_name_party = person.strip().split(',')
        person_name = person_name_party[0]
        person_party = person_name_party[1].strip()


        # collecting social networks
        social_networks = soup.find_all(class_='bt-link-extern')

        social_networks_urls = []
        for item in social_networks:
            social_networks_urls.append(item.get('href'))

        
        # gathering data together into dict

        data = {
            'person_name': person_name,
            'party_name': person_party,
            'social_networks': social_networks_urls
        }

        count += 1
        print(f'#{count}: {line} is done.')

        data_dict.append(data)

        with open('data.json', 'w', encoding="utf-8-sig") as json_file:
            json.dump(data_dict, json_file, indent=4)