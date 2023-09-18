from selenium import webdriver
import requests
import base64


def convert_to_base64(image_url):
    """
    Converts an image from a given URL into a base64-encoded string.

    :param image_url: The URL of the image to convert.
    :return: Base64-encoded image as a string.
    """
    response = requests.get(image_url)
    image_bytes = response.content

    # Encode the image bytes as base64
    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')

    return base64_encoded


def get_solution(base64_image):
    """
    Requests a solution from Capsolver for a given base64 image.

    :param base64_image: Base64-encoded image as a string.
    :return: The solution obtained from Capsolver.
    """
    payload = {
        "clientKey": "YOUR_API_KEY",  # Replace with your API key
        "task": {
            "type": "ImageToTextTask",
            "body": base64_image  # Base64 encoded image
        }
    }
    endpoint = "https://api.capsolver.com/createTask"
    response = requests.post(url=endpoint, json=payload)

    solution = response['solution']['text']
    return solution


# Initialize a Chrome WebDriver instance
driver = webdriver.Chrome()

# Get the URL of the captcha image. 
image_url = driver.find_element("captcha-image").get_attribute("href")

# Find the input box where text needs to be written
text_input_box = driver.find_element("input")

# Write the text solution into the text box
text_input_box.send_keys(get_solution(image_url))
