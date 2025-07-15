import calendar
from datetime import datetime, timedelta
from collections import defaultdict
import os
import sys

# Resolve paths relative to the executable or script location
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
SHOPPING_LIST_FILE = os.path.join(BASE_DIR, "shopping_list.txt")
RECIPE_FOLDER = os.path.join(BASE_DIR, "saved_recipes")

# Data stores
CALENDAR = {}  # Key: 'YYYY-MM-DD', Value: recipe dict
RECIPE_BOOK = []

CATEGORIES = {
    "dairy": ["milk", "cheese", "butter", "yogurt", "cream", "eggs"],
    "bread": ["bread", "bagel", "bun", "roll", "tortilla"],
    "meats": ["chicken", "beef", "pork", "bacon", "sausage", "ham", "turkey"],
    "vegetables": ["lettuce", "tomato", "onion", "carrot", "spinach", "broccoli", "pepper", "celery", "cucumber"],
    "baking": ["flour", "sugar", "baking powder", "baking soda", "vanilla", "yeast"]
}

# Ensure recipe folder exists
if not os.path.exists(RECIPE_FOLDER):
    os.makedirs(RECIPE_FOLDER)

def get_input(prompt):
    return input(prompt)

def display_main_menu():
    print("\nMain Menu:")
    print("1. View Calendar")
    print("2. Assign Recipe to a Day")
    print("3. View Saved Recipes")
    print("4. Generate Weekly Shopping List")
    print("5. View Specific Day")
    print("6. Exit")

def input_recipe():
    name = get_input("Enter recipe name: ")
    ingredients_input = get_input("Enter ingredients (comma-separated): ")
    ingredients = [i.strip().lower() for i in ingredients_input.split(',') if i.strip()]
    recipe = {'name': name, 'ingredients': ingredients}
    RECIPE_BOOK.append(recipe)

    # Save recipe to file
    safe_name = "_".join(name.lower().split()) + ".txt"
    recipe_path = os.path.join(RECIPE_FOLDER, safe_name)
    with open(recipe_path, "w") as file:
        file.write(f"Recipe: {name}\nIngredients:\n")
        for ingredient in ingredients:
            file.write(f"- {ingredient}\n")

    return recipe

def choose_saved_recipe():
    if not RECIPE_BOOK:
        print("No saved recipes available.")
        return None

    print("Saved Recipes:")
    for idx, recipe in enumerate(RECIPE_BOOK):
        print(f"{idx + 1}. {recipe['name']}")

    try:
        index = int(get_input("Enter the number of the recipe to select: ")) - 1
        return RECIPE_BOOK[index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None

def assign_recipe_to_day():
    selected_date = get_input("Enter the date (YYYY-MM-DD): ")
    try:
        datetime.strptime(selected_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    choice = get_input("Do you want to (1) Enter a new recipe or (2) Select a saved one? ")
    if choice == '1':
        recipe = input_recipe()
    elif choice == '2':
        recipe = choose_saved_recipe()
        if not recipe:
            return
    else:
        print("Invalid option.")
        return

    CALENDAR[selected_date] = recipe
    print(f"Recipe '{recipe['name']}' assigned to {selected_date}.")

def view_calendar():
    try:
        month = int(get_input("Enter month (1-12): "))
        year = int(get_input("Enter year (e.g., 2025): "))
    except ValueError:
        print("Invalid input.")
        return

    print(f"\nCalendar for {calendar.month_name[month]} {year}")
    week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    print(" ".join(week_days))
    cal = calendar.monthcalendar(year, month)

    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "    "
            else:
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                display_day = f"[{day:2d}]" if date_str in CALENDAR else f" {day:2d} "
                line += display_day + " "
        print(line.strip())
    print("\nLegend: [n] = Recipe scheduled")

def view_saved_recipes():
    if not RECIPE_BOOK:
        print("No saved recipes.")
        return
    for recipe in RECIPE_BOOK:
        print(f"- {recipe['name']}")

def view_specific_day():
    selected_date = get_input("Enter the date to view (YYYY-MM-DD): ")
    if selected_date in CALENDAR:
        recipe = CALENDAR[selected_date]
        print(f"\n{selected_date}: {recipe['name']}")
        print("Ingredients:")
        for item in recipe['ingredients']:
            print(f"- {item}")
    else:
        print("No recipe assigned for that day.")

def categorize_ingredient(item):
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in item:
                return category
    return "other"

def generate_shopping_list():
    start_date_input = get_input("Enter the start date for the week (YYYY-MM-DD): ")
    try:
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    ingredient_counts = defaultdict(int)
    for i in range(7):
        current_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        if current_date in CALENDAR:
            for item in CALENDAR[current_date]['ingredients']:
                ingredient_counts[item] += 1

    categorized = defaultdict(list)
    for item, count in ingredient_counts.items():
        category = categorize_ingredient(item)
        categorized[category].append((item, count))

    print("\nWeekly Shopping List:")
    with open(SHOPPING_LIST_FILE, "w") as file:
        for category in sorted(categorized.keys()):
            print(f"\n{category.capitalize()}:")
            file.write(f"\n{category.capitalize()}:\n")
            for item, count in categorized[category]:
                line = f"{item} x{count}"
                print(f"- {line}")
                file.write(f"- {line}\n")

    print(f"\nShopping list saved to {SHOPPING_LIST_FILE}.")

# Main loop
while True:
    display_main_menu()
    option = get_input("Choose an option: ")

    if option == '1':
        view_calendar()
    elif option == '2':
        assign_recipe_to_day()
    elif option == '3':
        view_saved_recipes()
    elif option == '4':
        generate_shopping_list()
    elif option == '5':
        view_specific_day()
    elif option == '6':
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")