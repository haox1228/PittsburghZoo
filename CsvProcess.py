import pandas as pd
from fuzzywuzzy import process

animal_type = pd.read_csv('class.csv')
zoo = pd.read_csv('zoo.csv')


def cleanData(animal_type, zoo):
    animal_type = animal_type.drop(['Number_Of_Animal_Species_In_Class', 'Animal_Names'], axis=1)
    zoo = pd.merge(zoo, animal_type, left_on=('class_type'), right_on=('Class_Number'))
    zoo['animal_name'] = zoo['animal_name'].str.capitalize()
    zoo = zoo.drop(['class_type', 'Class_Number', 'catsize', 'milk', 'eggs'], axis=1)
    zoo = zoo.rename(columns={'Class_Type': 'type'})
    return zoo


def matchAnimal(df, search):
    animals = df['animal_name'].tolist()
    best_match = process.extractOne(search, animals)

    if best_match[1] >= 80:
        matched_animal = best_match[0]
        matched_row = df[df['animal_name'] == matched_animal].iloc[0]

        print(f"{search} seems a kind of '{matched_animal}'.")  # Added line


        group1 = [col for col in ['hair', 'feathers', 'toothed', 'backbone', 'fins', 'legs', 'tail'] if
                  matched_row[col] == 1]
        group2 = [col for col in ['airborne', 'aquatic'] if matched_row[col] == 1]
        group3 = [col for col in ['venomous', 'predator'] if matched_row[col] == 1]
        group4 = [col for col in ['domestic'] if matched_row[col] == 1]

        # Generate a sentence
        sentence = f"{matched_animal} is a "

        if group4:
            sentence += f"{' '.join(group4)} "

        if group2:
            sentence += f"{' '.join(group2)} "

        sentence += f"{matched_row['type'].lower()} with {', '.join(group1[:-1])}, and {group1[-1]}"

        if group3:
            sentence += f". It is {' and '.join(group3)}"

        sentence += f", that {'needs' if matched_row['breathes'] == 1 else 'needs not'} to breathe."

        return sentence
    else:
        return "No matching animal found, but try your luck at getting detail information feature"

