#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:51:12 2023
The script that used to process the csv data
@author: Nick, Samson, Masu (Team: Cold Brew)
"""

import pandas as pd
from fuzzywuzzy import process

# read the csv
animal_type = pd.read_csv('class.csv')
zoo = pd.read_csv('zoo.csv')
import matplotlib.pyplot as plt


def show_stats(filtered_df):
    '''
    This method creates three graph for users to get basic infomation of the animals in the zoo
    :param filtered_df: the df that has been filtered with only animals exist in the pgh zoo
    :return: graphs and a sentence
    '''
    # pie chart for animal count by type
    animal_count = filtered_df['type'].value_counts()
    animal_count.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title("Animal Count by Type (Pie chart)")
    plt.ylabel("")
    plt.show()

    # bar chart for animal count by type
    animal_count.plot(kind='bar')
    plt.title("Animal Count by Type (Bar chart)")
    plt.xlabel("Animal Type")
    plt.ylabel("Count")
    plt.show()

    # box plot for animal count by legs and type
    fig, ax = plt.subplots()
    filtered_df.boxplot(column='legs', by='type', ax=ax)
    plt.title("Animal Count by Legs and Type (Box plot)")
    plt.suptitle("")
    plt.xlabel("Animal Type")
    plt.ylabel("Legs")
    plt.show()

    print('Your graph has been generated')


def cleanData(animal_type, zoo):
    '''
    This is the method that used to clean the csv data, it will join
    two csvs together and then drop a few columns
    :param animal_type: a csv
    :param zoo: another csv
    :return: a cleaned up csv
    '''
    animal_type = animal_type.drop(['Number_Of_Animal_Species_In_Class', 'Animal_Names'], axis=1)
    zoo = pd.merge(zoo, animal_type, left_on=('class_type'), right_on=('Class_Number'))
    zoo['animal_name'] = zoo['animal_name'].str.capitalize()
    zoo = zoo.drop(['class_type', 'Class_Number', 'catsize', 'milk', 'eggs'], axis=1)
    zoo = zoo.rename(columns={'Class_Type': 'type'})
    return zoo


def matchAnimal(df, search, print_sentences=True):
    '''
    This method will use the search name and the csv file, to search if the
    animal exists in the df, and used a fuzzy search since there won't always be an
    exact match. And then group out features to make a grammarly logical sentense
    to prompt to the user
    :param df: the csv
    :param search: the search string
    :return: return a matched animal from fuzzy search for making the api call
    and a string sentence to prompt to the user.
    '''
    animals = df['animal_name'].tolist()
    best_match = process.extractOne(search, animals)

    if best_match[1] >= 80:
        matched_animal = best_match[0]
        matched_row = df[df['animal_name'] == matched_animal].iloc[0]
        if print_sentences:
            print(f"{search} seems a kind of '{matched_animal}'.")  # Added line

        group1 = [col for col in ['hair', 'feathers', 'toothed', 'backbone', 'fins', 'legs', 'tail'] if
                  matched_row[col] == 1]
        group2 = [col for col in ['airborne', 'aquatic'] if matched_row[col] == 1]
        group3 = [col for col in ['venomous', 'predator'] if matched_row[col] == 1]
        group4 = [col for col in ['domestic'] if matched_row[col] == 1]

        # generate a sentence
        sentence = f"{matched_animal} is a "

        if group4:
            sentence += f"{' '.join(group4)} "

        if group2:
            sentence += f"{' '.join(group2)} "

        sentence += f"{matched_row['type'].lower()} with {', '.join(group1[:-1])}, and {group1[-1]}"

        if group3:
            sentence += f". It is {' and '.join(group3)}"

        sentence += f", that {'needs' if matched_row['breathes'] == 1 else 'needs not'} to breathe."

        return matched_animal, sentence
    else:
        return '', "No matching animal found, but try your luck at getting detail information feature"
