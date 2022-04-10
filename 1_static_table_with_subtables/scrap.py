import random
import requests
from bs4 import BeautifulSoup
import json
import csv
from time import sleep

# # 1st step: defining url, headers
# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    "accept":'*/*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Mobile Safari/537.36'
}
# # Sending request
# req = requests.get(url, headers=headers)

# # Checking that we picked up the website code
# src = req.text
# # print(src)

# # Saving the code into index.html file
# with open('index.html', 'w', encoding="utf-8-sig") as file:
#     file.write(src)

# # Step 2
# # Reading index file
# with open('index.html', encoding="utf-8-sig") as file:
#     src = file.read()

# # Checking class of the web links and parsing the webpage with find_all
# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')

# # Creating empty dict for storing categories' names and hrefs
# all_categories_dict = {}
# for item in all_products_hrefs:
#     # print(item)
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_text] = item_href

# # Saving dict into json file
# with open('all_categories_dict.json', 'w', encoding="utf-8-sig") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


# step 3
# loading json file into variable "all_categories"
with open("all_categories_dict.json", encoding="utf-8-sig") as file:
    all_categories = json.load(file)

# Counting total iterations
iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():
    # replacing symbols with underscore
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    # going to requests on the webpage
    req = requests.get(url=category_href, headers=headers)
    # saving it to virable
    src = req.text

    # writing down category files
    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8-sig") as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding="utf-8-sig") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # Checking if there are tables insige product categories
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # Collecting table headers
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    # saving data into file
    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # Collecting products' data
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []
    for item in products_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        # saving it to tuple to store it later in json file
        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        # writing data into files
        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    # saving data to json        
    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8-sig") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    # Adding counter
    count += 1
    print(f"# Iteration {count}. {category_name} has been written")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Work is done")
        break

    print(f"Remaining iterations: {iteration_count}")
    sleep(random.randrange(2, 4))



    