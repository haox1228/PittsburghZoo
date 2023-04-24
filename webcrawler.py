import re
import requests
from bs4 import BeautifulSoup


def crawler():
    pitts_zoo_url = 'https://www.pittsburghzoo.org/animals/'
    page = requests.get(pitts_zoo_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    animals_section = soup.find(id='et-boc').find(class_='et_pb_row et_pb_row_9')
    animals = animals_section.findAll(class_='et_pb_text_inner')

    animal_dict = {}
    for animal in animals:
        animal_info = animal.get_text().split('\n')
        animal_info = [re.sub(r'[^\x00-\x7F]+', "'", elem) for elem in animal_info if elem != '']
        animal_dict[animal_info[0]] = animal_info[1:]

    return animal_dict


if __name__ == '__main__':
    animal_dict = crawler()
    print(animal_dict)
