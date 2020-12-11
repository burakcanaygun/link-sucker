from Sucker import link_sucker
from CsvCleaner import clean_data_generator

user_search_input = None
user_last_page = None
user_input = None

while user_input != "q":
    print("Hello there! \n1-Enter a search input \n2-Enter a page number\n3-Fire up!\n4-If you want to quit just hit q"
          "enter")
    user_input = input("Pick a number:")
    if user_input == "1":
        user_search_input = input("Enter your search input:")
    elif user_input == "2":
        user_last_page = input("Enter your page number:")
    elif user_input == "3":
        link_sucker(user_search_input, user_last_page)
        clean_data_generator(user_search_input)
