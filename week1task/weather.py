import requests
import time


API_KEY = '46d45f6d92cde5463f35cb43811b353e'  # Replace with your OpenWeatherMap API key
FAVORITES_FILE = 'favorites.txt'

# Function to fetch weather data by city name
def get_weather_by_city(city):
    BASE_URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error fetching weather data for {city}: {response.status_code}')
        return None

# Function to manage favorite cities
def manage_favorites(action, city):
    favorites = load_favorites()
    if action == 'add':
        if city not in favorites:
            favorites.append(city)
            print(f'{city} added to favorites.')
        else:
            print(f'{city} is already in favorites.')
    elif action == 'remove':
        if city in favorites:
            favorites.remove(city)
            print(f'{city} removed from favorites.')
        else:
            print(f'{city} is not in favorites.')
    elif action == 'list':
        print('Favorite cities:')
        for idx, favorite in enumerate(favorites, start=1):
            print(f'{idx}. {favorite}')
    save_favorites(favorites)

# Function to load favorite cities from file
def load_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as file:
            favorites = [line.strip() for line in file.readlines()]
            return favorites
    except FileNotFoundError:
        return []

# Function to save favorite cities to file
def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as file:
        for favorite in favorites:
            file.write(favorite + '\n')

# Main function
def main():
    print("Weather Checking Application")
    print("============================")
    while True:
        print('\nOptions:')
        print('1. Check weather by city')
        print('2. Add city to favorites')
        print('3. Remove city from favorites')
        print('4. List favorite cities')
        print('5. Exit')

        choice = input('Enter your choice: ')

        if choice == '1':
            city = input('Enter city name: ')
            weather_data = get_weather_by_city(city)
            if weather_data:
                print(f'Weather in {city}: {weather_data["weather"][0]["description"]}')
                print(f'Temperature: {weather_data["main"]["temp"]}°C')
                print(f'Humidity: {weather_data["main"]["humidity"]}%')
            else:
                print(f'Failed to fetch weather data for {city}.')

        elif choice == '2':
            city = input('Enter city name: ')
            manage_favorites('add', city)

        elif choice == '3':
            city = input('Enter city name: ')
            manage_favorites('remove', city)

        elif choice == '4':
            manage_favorites('list', '')

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print('Invalid choice. Please try again.')

        time.sleep(15)  # Auto-refresh every 15 seconds

if __name__ == '__main__':
    main()