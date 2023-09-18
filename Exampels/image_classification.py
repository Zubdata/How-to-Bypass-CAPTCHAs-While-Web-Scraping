"""
This module demonstrates the process of bypassing image classification captchas(i.e. Recaptcha) using the Capsolver API. For a comprehensive understanding of this process, please refer to the API documentation page at https://docs.capsolver.com/guide/recognition/ReCaptchaClassification.html

"""

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


def get_question(object_name):
    """
    Retrieves the question corresponding to an object name.

    :param object_name: The name of the object for which the question is needed.
    :return: The question associated with the object name.
    """
    object_mappings = {
        "taxis": "/m/0pg52",
        "bus": "/m/01bjv",
        "school bus": "/m/02yvhj",
        # ... (other object mappings) ...
    }

    for key, value in object_mappings.items():
        if object_name.lower() in key:
            return value


def get_solution(base64_image, object_name):
    """
    Requests a solution from Capsolver for a given base64 image and object name.

    :param base64_image: Base64-encoded image as a string.
    :param object_name: The name of the object in the image.
    :return: The solution obtained from Capsolver.
    """
    payload = {
        "clientKey": "YOUR_API_KEY",  # Replace with your API key
        "task": {
            "type": "ReCaptchaV2Classification",
            "image": base64_image,
            "question": get_question(object_name=object_name)
        }
    }
    endpoint = "https://api.capsolver.com/createTask"
    response = requests.post(url=endpoint, json=payload)

    solution = response['solution']['text']
    return solution

# Below is an example of solving a captcha using the obtained solution.


driver = webdriver.Chrome()
captcha_image = driver.find_element("img.captcha-image").get_attribute("href")
captcha_object = driver.find_element("h2.object").text

solution = get_solution(base64_image=convert_to_base64(
    image_url=captcha_image), object_name=captcha_object)

# Let's assume the solution is [0, 5, 3, 7]

# Now, we will retrieve all the captcha image boxes
all_boxes = driver.find_elements("div.img-box")

# We will check if the box index is present in the solution. Remember that box indices start from 0.
for index, box in enumerate(all_boxes):
    if index in solution:
        box.click()

# Finally, locate the verify button and click on it
verify_button = driver.find_element("button.verify")
verify_button.click()
