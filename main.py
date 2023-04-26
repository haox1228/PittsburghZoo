#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:51:12 2023
@author: Nick, Samson, Masu (Team: Cold Brew)
"""
import pandas as pd
from CsvProcess import cleanData, matchAnimal, show_stats
from webcrawler import crawler
from APICall import call_api, wording

def main():
    '''
    The main routine of the program, have include all the use cases in the proposal
    '''
    # Load and clean the data
    animal_type = pd.read_csv('class.csv')
    zoo = pd.read_csv('zoo.csv')
    df = cleanData(animal_type, zoo)

    animal_dict = crawler()
    # List of animal options
    # animal_options = ['Canadian Lynx', 'Giant Panda', 'Komodo Dragon', 'Tiger']
    animal_areas = list(animal_dict.keys())

    while True:
        # first layer of ui
        print("\nHello there, this is the PGH Zoo Virtual Tour guide, how can i help you?")
        print("1. View statistical data of the PGH zoo")
        print("2. Know the animals in the PGH zoo")
        print("0. Exit")

        choice = int(input("> "))

        if choice == 0:
            break
        # if user choose 1, then generate graph
        if choice == 1:
            # filter out the csv data with only animals in the pgh zoo
            matched_animals = []
            for area, animals in animal_dict.items():
                for animal in animals:
                    matched_animal, _ = matchAnimal(df, animal,False)
                    if matched_animal:
                        matched_animals.append(matched_animal)

            matched_animals = list(set(matched_animals))
            filtered_df = df[df['animal_name'].isin(matched_animals)]
            #show the graphs
            show_stats(filtered_df)
        elif choice == 2:
            # User prompt
            print("\nWhich area do you want to know? (Press 0 to exit)")
            for i, option in enumerate(animal_areas, 1):
                print(f"{i}. {option}")

            # Get user input for animal area
            choice = int(input("> "))

            # Exit when user inputs 0
            if choice == 0:
                break

            # Ensure valid input
            if 1 <= choice <= len(animal_areas):
                print('\nWhich animal do you want to know? (Press 0 to exit)')
                animal_options = list(animal_dict.get(animal_areas[choice-1]))
                for i, option in enumerate(animal_options, 1):
                    print(f"{i}. {option}")

                # Get user input for specific animal
                choice = int(input("> "))

                # Exit when user inputs 0
                if choice == 0:
                    break

                search_string = animal_options[choice - 1]
                matched_animal, result = matchAnimal(df, search_string)
                print(result)

                # in case of not existing in csv but can find from API such as panda
                # extract a last word from animal name (can cover mostly)
                if matched_animal == '':
                    matched_animal = search_string.split()[-1]

                animals_apiinfo = call_api(matched_animal)

                if len(animals_apiinfo) > 0:
                    print('I can provide detailed information for the below species. (select one of enter 0 to exit)')

                    animal_options = [d.get('name') for d in animals_apiinfo]
                    for i, option in enumerate(animal_options, 1):
                        print(f"{i}. {option}")

                    # Get user input for specific animal
                    choice = int(input("> "))

                    # Exit when user inputs 0
                    if choice == 0:
                        break

                    # Choose one animal dict and wording information
                    target_animal_dict = animals_apiinfo[choice - 1]
                    explanation = wording(target_animal_dict)

                    # Print detailed animal info
                    print(explanation)

                else:
                    print("Sorry, I can't find this animal's information")
        else:
            print("Invalid input.")

if __name__ == '__main__':
    main()
