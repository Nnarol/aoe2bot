import string
import requests
from bs4 import BeautifulSoup
import re
from collections import namedtuple

#Technology data is stored per table for each technology category,
#such as economy, infantry, ship, building, etc.
#These HTML tables follow a CSV format, including a header:
#each table contains the same header row with the same data item names,
#followed by one row of data for each technology in the table.

Tech = namedtuple("Tech", ["Technology", "Cost", "Effect", "Research_Time"])
table_indices = {"Economy": 2, "Buildings": 1, "Monastery": 3, "Infantry": 4, "Ranged": 5, "Cavalry": 6, "Ship": 7, "Miscellaneous": 8}
desired_data = ("Technology", "Cost", "Effect", "Research_Time")

#reading fandom webpage using beautiful soup

soup = BeautifulSoup(requests.get('https://ageofempires.fandom.com/wiki/Technology_(Age_of_Empires_II)').content, 'lxml')

#finding required tables, using website and it's code

techs = []

for category_name, table_index in table_indices.items():
    tech_table = soup.find_all("table")[table_index]

    rows = tech_table.find_all('tr')
    header_row = rows[0]

    normalized_header = [table_data.text for table_data in header_row.find_all('td')]
    normalized_header = [field.strip().replace(" ", "_") for field in normalized_header]

    field_indices_in_row = {}
    for field in desired_data:
        field_indices_in_row[field] = normalized_header.index(field)
        if field_indices_in_row[field] == -1:
            raise(
                ValueError(f'No field named "{field}" or similar found for tech category "{category_name}"!'))

    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)

    tech_rows = rows[1:]
    for row in tech_rows:
        tech_data = [td.text for td in row.find_all('td')]
        filtered_tech_data = {
            field: tech_data[index].translate(translator)
            for field, index in field_indices_in_row.items()
        }

        #Cleaning tech name strings
        filtered_tech_data["Technology"] = filtered_tech_data["Technology"].replace(u'\xa0', ' ')
        filtered_tech_data["Technology"] = filtered_tech_data["Technology"].lower()
        filtered_tech_data["Technology"] = re.sub(r"^\s+", "", filtered_tech_data["Technology"], flags=re.UNICODE)
        techs.append(Tech(**filtered_tech_data))

#Map all technology names to their human-readable descriptions.
#Tech names are in lower-case.
tech_all = {
    tech.Technology: f"Effect: {tech.Effect}; Cost: {tech.Cost}; Time to Research: {tech.Research_Time}"
    for tech in techs
}
print(tech_all)
