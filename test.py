import random
import string
from datetime import datetime
import json
print("Hello User!\n")

first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
birthday = input("Enter your birthday (dd/mm/yyyy):")

try:
    birth_date = datetime.strptime(birthday, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
except ValueError:
    print("Invalid birthday format. Please use dd/mm/yyyy.")
    age = 0 

print(f" {first_name} {last_name}, welcome to the Motion Detector! Let's start\n")

# Password Generator
def generate_password(capitals, smalls, numbers, specials):
    password = []
    password.extend(random.choices(string.ascii_uppercase, k=capitals))
    password.extend(random.choices(string.ascii_lowercase, k=smalls))
    password.extend(random.choices(string.digits, k=numbers))
    password.extend(random.choices(string.punctuation, k=specials))
    random.shuffle(password)
    return ''.join(password)

# Username Generator
def generate_username(first_name, last_name):
    random_number = random.randint(100, 999)
    return f"{first_name.lower()}{last_name.lower()[:3]}{random_number}"

# Temperature Calculator
def convert_temperature(value, unit_from, unit_to):
    if unit_from == "C" and unit_to == "F":
        return value * 9/5 + 32
    elif unit_from == "C" and unit_to == "K":
        return value + 273.15
    elif unit_from == "F" and unit_to == "C":
        return (value - 32) * 5/9
    elif unit_from == "F" and unit_to == "K":
        return (value - 32) * 5/9 + 273.15
    elif unit_from == "K" and unit_to == "C":
        return value - 273.15
    elif unit_from == "K" and unit_to == "F":
        return (value - 273.15) * 9/5 + 32
    return value

# User Rights Checker
def check_user_role(first_name, age):
    if first_name.lower() == "shariar":
        print(f"Welcome {first_name}, you have admin rights.")
    elif first_name.lower() == "mira":
        print(f"Welcome {first_name}, you have super-user rights.")
    elif age >= 18:
        print(f"Welcome {first_name}, you have viewer rights.")
    else:
        print(f"Greetings {first_name}, you are too young to operate this program.")

# Number Guessing Game
def number_guessing_game():
    scoreboard = []
    while True:
        random_number = random.randint(1, 100)
        attempts = 8
        print("\nGuess the number between 1 and 100!")
        
        for round_num in range(1, attempts + 1):
            guess = input(f"Round {round_num}: Enter your guess (or type 'quit' to exit): ")
            
            if guess.lower() == "quit":
                print("Thanks for playing!")
                print("Scoreboard:", scoreboard)
                return
            
            try:
                guess = int(guess)
            except ValueError:
                print("Please enter a valid number.")
                continue

            if guess == random_number:
                print("Congratulations! You guessed the number!")
                scoreboard.append("Win")
                break
            elif guess < random_number:
                print("Too low!")
            else:
                print("Too high!")
        else:
            print(f"Sorry, you've used all your attempts. The number was {random_number}.")
            scoreboard.append("Loss")

        print("Scoreboard:", scoreboard)
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            print("Scoreboard:", scoreboard)
            break

# Main Program Menu
def main():
    while True:
        print("\nMain Menu:")
        print("1. Password Generator")
        print("2. Username Generator")
        print("3. Temperature Calculator")
        print("4. User Rights Checker")
        print("5. Number Guessing Game")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            capitals = int(input("Enter the number of capital letters: "))
            smalls = int(input("Enter the number of small letters: "))
            numbers = int(input("Enter the number of numbers: "))
            specials = int(input("Enter the number of special characters: "))
            print(f"Generated password: {generate_password (capitals, smalls, numbers, specials)}")
        elif choice == "2":
            day, month, year = birthday.split("/")
            username = first_name[:3] + last_name[:3] + year + month + day
            print(f"Your username is:{username}")
        elif choice == "3":
            value = float(input("Enter the temperature value: "))
            unit_from = input("Enter the unit to convert from (C, F, K): ").upper()
            unit_to = input("Enter the unit to convert to (C, F, K): ").upper()
            if unit_from in ["C", "F", "K"] and unit_to in ["C", "F", "K"]:
                print(f"Converted Temperature: {convert_temperature(value, unit_from, unit_to)} {unit_to}")
            else:
                print("Invalid unit. Please enter C, F, or K.")
        elif choice == "4":
            check_user_role(first_name, age)
        elif choice == "5":
            number_guessing_game()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Function to fetch data from ThingSpeak API
def fetch_thingspeak_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("feeds", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from ThingSpeak: {e}")
        return []

# Function to convert UTC to local timezone
def convert_to_local_time(utc_time_str, timezone='Europe/Helsinki'):
    local_tz = pytz.timezone(timezone)
    try:
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        local_time = utc_time.astimezone(local_tz)
        return local_time.strftime("%d.%m.%Y, %H:%M")
    except ValueError as e:
        print(f"Error converting time: {e}")
        return utc_time_str
    
def save_data_to_json(user_info, data, file_name="sensor_data.json"):
    combined_data = {
        "user_info": user_info,
        "sensor_data": data
    }
    try:
        with open(file_name, "w") as file:
            json.dump(combined_data, file, indent=4)
        print(f"Data successfully saved to {file_name}.")
    except IOError as e:
        print(f"Error saving data to JSON: {e}")

 # ThingSpeak API details
    api_url = "https://api.thingspeak.com/channels/2780324/feeds.json?api_key=4OEBN726QPS8YWKF&results=10"

    # Fetch and process data from ThingSpeak
    print("\nFetching data from ThingSpeak...")
    feeds = fetch_thingspeak_data(api_url)

    # Process the data
    sensor_data = []
    for entry in feeds:
        converted_time = convert_to_local_time(entry["created_at"])
        sensor_data.append({
            "movement_value": entry.get("field1"),
            "temperature_value": entry.get("field2"),
            "timestamp": converted_time
        })

    # Save the information to a JSON file
    save_data_to_json(user_info, sensor_data)
# Run the program
main()
