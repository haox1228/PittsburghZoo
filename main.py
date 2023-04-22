from CsvProcess import cleanData, matchAnimal
import pandas as pd


def main():
    # Load and clean the data
    animal_type = pd.read_csv('/Users/mahaoxuan/Downloads/archive (1)/class.csv')
    zoo = pd.read_csv('/Users/mahaoxuan/Downloads/archive (1)/zoo.csv')
    df = cleanData(animal_type, zoo)

    # List of animal options
    animal_options = ['Canadian Lynx', 'Giant Panda', 'Komodo Dragon', 'Tiger']

    while True:
        # User prompt
        print("\nWhich animal do you want to know? (Press 0 to exit)")
        for i, option in enumerate(animal_options, 1):
            print(f"{i}. {option}")

        # Get user input
        choice = int(input("> "))

        # Exit when user inputs 0
        if choice == 0:
            break

        # Ensure valid input
        if 1 <= choice <= len(animal_options):
            search_string = animal_options[choice - 1]
            result = matchAnimal(df, search_string)
            print(result)
        else:
            print("Invalid input.")



if __name__ == '__main__':
    main()
