#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:51:12 2023
@author: Nick, Samson, Masu (Team: Cold Brew)
"""
import re
import requests
from bs4 import BeautifulSoup

def crawler():
    """
    A web scraper that extracts animal information from the Pittsburgh Zoo website.

    Returns:
    animal_dict (dict): A dictionary containing animal areas as keys and their respective animal names as values.
    """
    pitts_zoo_url = 'https://www.pittsburghzoo.org/animals/'
    page = requests.get(pitts_zoo_url)

    # Parse the HTML content using BeautifulSoup, and Find the section containing animal information
    soup = BeautifulSoup(page.content, 'html.parser')
    animals_section = soup.find(id='et-boc').find(class_='et_pb_row et_pb_row_9')
    animals = animals_section.findAll(class_='et_pb_text_inner')

    # find the animal areas and animal names to store animal information
    animal_dict = {}
    for animal in animals:
        animal_info = animal.get_text().split('\n')
        animal_info = [re.sub(r'[^\x00-\x7F]+', "'", elem) for elem in animal_info if elem != '']
        animal_dict[animal_info[0]] = animal_info[1:]

    return animal_dict

# For debugging purpose
if __name__ == '__main__':
    animal_dict = crawler()
    print(animal_dict)
