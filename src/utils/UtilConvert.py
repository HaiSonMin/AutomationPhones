from collections import Counter
import os, requests, pytz, pytesseract
from datetime import datetime
from PIL import Image
from io import BytesIO
from appium.webdriver.webdriver import WebDriver
import numpy as np

pytesseract.pytesseract.tesseract_cmd = (
    "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)


def convert_img_text(
    driver: WebDriver, dir_name, image_name, x_start, y_start, x_end, y_end
) -> str:
    # Take a screenshot using the driver
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))

    # Crop the screenshot to the specified area
    cropped_image = screenshot.crop((x_start, y_start, x_end, y_end))

    # Define the directory path for saving the image
    directory_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "images", dir_name
    )
    os.makedirs(directory_path, exist_ok=True)

    # Join path
    image_path = os.path.join(directory_path, f"{image_name}.png")

    # # Save the cropped image
    cropped_image.save(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image_path)

    print("text:::", text)

    return text


def convert_img_color_codes(
    driver: WebDriver,
    image_name,
    x_start,
    y_start,
    x_end,
    y_end,
    dir_name="colors_code",
):
    # Take a screenshot using the driver
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))

    # Crop the screenshot to the specified area
    cropped_image = screenshot.crop((x_start, y_start, x_end, y_end))

    # Get the directory of the current file
    current_file_directory = os.path.dirname(os.path.abspath(__file__))

    # Move back one directory level
    parent_directory = os.path.dirname(current_file_directory)

    # Define the directory path using the parent directory
    directory_path = os.path.join(parent_directory, "images", dir_name)

    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Join path
    image_path = os.path.join(directory_path, f"{image_name}.png")

    # Save the cropped image
    cropped_image.save(image_path)

    # Load the image
    image = Image.open(image_path)
    image = image.convert("RGB")  # Ensure the image is in RGB format

    # Convert image to numpy array
    image_array = np.array(image)

    # Flatten the array and count the occurrences of each color
    flat_sub_image_array = image_array.reshape(-1, image_array.shape[2])
    color_counts = Counter(map(tuple, flat_sub_image_array))

    most_common_color_arr = color_counts.most_common(1)

    # Get the most common color
    most_common_color = most_common_color_arr[len(most_common_color_arr) - 1][0]

    # Convert the most common color to hexadecimal
    hex_color = get_hex_color(*most_common_color)

    return hex_color


def get_hex_color(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def convert_limit(limit: str = "10"):
    return int(limit)


def convert_list_music_to_arr(strListMusic: str):
    # ['Beautiful People', 'Ed Sheeran featuring Khalid', 'Good as Hell', 'Lizzo']
    parts = [part.strip() for part in strListMusic.split("-")]
    return [part for part in parts if part]


def convert_list_music_to_arr(strListMusic: str):
    # ['Beautiful People', 'Ed Sheeran featuring Khalid', 'Good as Hell', 'Lizzo']
    parts = [part.strip() for part in strListMusic.split("-")]
    return [part for part in parts if part]


def convert_skip(limit: str = "10", page: str = "1"):
    return (int(page) - 1) * int(limit)


def convert_str_to_arr(strVal: str, character_split: str = ",") -> list[str]:
    if strVal.strip() == "":
        return []
    listItems = [item.strip() for item in strVal.split(character_split)]
    listItems = [item for item in listItems if item.strip() != ""]
    return listItems


def convert_arr_to_str(arrVal: list[str], character_join: str = ", ") -> str:
    return character_join.join(arrVal)


def convert_remove_item_empty_arr(arr: list[any]) -> list[any]:
    return [item for item in arr if item != "" and item != None]


def convert_remove_item_empty_dict(arr: dict) -> dict:
    return {key: value for key, value in arr.items() if value not in [None, "", [], {}]}


def convert_to_lowercase_arr(strings: list[str]):
    return [s.lower() for s in strings]


def lower_case_first_character(valString: str):
    return f"{valString[0].lower()}{valString[1:]}"


def convert_to_time_us(vn_time: datetime):
    # Define the Vietnam time zone
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")

    # Localize the given Vietnam time to its time zone
    localized_vn_time = vn_tz.localize(vn_time)

    # Define the USA time zones you want to convert to
    usa_time_zone = "America/Chicago"

    # Convert and print the time in each USA time zone
    usa_tz = pytz.timezone(usa_time_zone)
    usa_time = localized_vn_time.astimezone(usa_tz)

    return usa_time.strftime("%Y-%m-%d %H:%M:%S")
