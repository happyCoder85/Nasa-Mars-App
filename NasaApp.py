from requests import get
import json
from PIL import Image
from io import BytesIO
from menu import Menu

# Apps menus page titles
main_menu = Menu(title="Welcome to the Mars Rover Image App - Please select a rover:")

# Gets all the rovers as json
API_KEY = "mM4uZVkrlLH0obbBfKrTh4OneozBK5RTWWzDycsl"
url_rovers = f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={API_KEY}"
all_rovers = get(url_rovers).json()    

def display_image(url):
    """Displays the photo found at url."""
    image_response = get(url) 
    image = Image.open(BytesIO(image_response.content))
    image.show()
    image.close()

def generate_image_selection(list_of_photos, page_number, photo_stop_count, date):
    """List 10 photo items based on photo_stop_count variable"""

    photo_menu = Menu(title= f"You are seeing pictures {photo_stop_count - 9} - {photo_stop_count} out of {len(list_of_photos['photos'])} on page {page_number}. Please make a selection:")
    photo_menu_options = []
        
    for image in list_of_photos['photos'][photo_stop_count - 10:photo_stop_count:1]:
        photo_menu_options.append((image['img_src'], display_image, {"url": image['img_src']}))
    
    page_number += 1
    photo_stop_count += 10

    if photo_stop_count - 10 < len(list_of_photos['photos']):
        photo_menu_options.append(("Next page", generate_image_selection, {"list_of_photos": list_of_photos, "page_number": page_number, "photo_stop_count": photo_stop_count, "date": date}))

    if page_number - 1 > 1:
        photo_menu_options.append(("Previous page", Menu.CLOSE))

    if page_number - 1 == 1:
        photo_menu_options.append(("Main menu", Menu.CLOSE))

    photo_menu.set_options(photo_menu_options)
    photo_menu.open()

def choose_rover(choice):
    """Based off selection in previous menu will generate the first page of photos"""
    date = input('Please enter a date in the following format: YYYY-MM-DD (if you chose Curiosity, try 2015-06-03 or 2020-01-01) -> ')
    url_images = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{choice}/photos?earth_date={date}&api_key={API_KEY}'
    list_of_photos = get(url_images).json()
    
    page_number = 1

    generate_image_selection(list_of_photos, page_number, 10, date)
        
# Loops through rovers found in all_rovers and adds them to the main menu options
main_menu_options = []
for rover in all_rovers['rovers']:
    main_menu_options.append((rover['name'], choose_rover, {"choice": rover['name']}))
    
main_menu_options.append(("Exit", Menu.CLOSE))
main_menu.set_options(main_menu_options)
main_menu.open()