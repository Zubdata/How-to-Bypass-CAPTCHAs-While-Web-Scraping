"""
This module demonstrates a method for solving math-based CAPTCHAs encountered during web scraping.
To achieve this, you should use the 'image_captcha.py' module to extract text from captcha images.

"""

from selenium import webdriver

# Initialize a Chrome WebDriver instance
driver = webdriver.Chrome()

# Let's assume the text extracted from the image captcha is as follows:
captcha_text = "2+3=?"

# Remove the question mark and equals sign from the text
captcha_text = captcha_text.replace("?", "")
captcha_text = captcha_text.replace("=", "")

# Now 'captcha_text' holds the expression '2+3'

# Evaluate the expression using JavaScript
solution = driver.execute_script(f"return eval('{captcha_text}')")

# You can now use 'solution' to populate solution input box
