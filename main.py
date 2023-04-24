from CsvProcess import cleanData, matchAnimal
import pandas as pd
from webcrawler import crawler

def main():
    # Load and clean the data
    animal_type = pd.read_csv('class.csv')
    zoo = pd.read_csv('zoo.csv')
    df = cleanData(animal_type, zoo)

    animal_dict = crawler()

    # List of animal options
    # animal_options = ['Canadian Lynx', 'Giant Panda', 'Komodo Dragon', 'Tiger']
    animal_areas = list(animal_dict.keys())

    while True:
        # User prompt
        print("\nWhich animal do you want to know? (Press 0 to exit)")
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
            result = matchAnimal(df, search_string)
            print(result)

        else:
            print("Invalid input.")



if __name__ == '__main__':
    main()
