## File for the Translation Service
import json
from typing import Union

import sys
sys.path.append('.')
from utils import *


@log_function_data
def translate_input(input_data: Union[str, dict], from_ln: str, to_ln: str) -> Union[str, dict]:
    """
    Translates the given input text from the source language to the target language.
    The input can be in plain text or JSON (as a dictionary).
    This function checks if the required translation package is installed, installs it if not,
    and then proceeds with the translation.

    Parameters:
    - input_data (str, dict): The text to be translated, or a JSON/dictionary containing the text.
    - from_ln (str): The ISO 639-1 language code of the source language.
    - to_ln (str): The ISO 639-1 language code of the target language.

    Returns:
    - Union[str, dict]: The translated text, in the same format as the input.
    """

    # Check and install the translation package if necessary
    if not install_translation_package(from_ln, to_ln):
        return "Required translation package could not be installed."

    def translate_item(text):
        return translate_text(text, from_ln, to_ln)

    # Handle different types of input
    if isinstance(input_data, str):
        return translate_item(input_data)
    elif isinstance(input_data, dict):
        # Assume the dict is in JSON format and translate each value
        return {key: translate_item(value) for key, value in input_data.items()}
    else:
        return "Unsupported input type."

# Example usage
# For plain text
# translated_text = translate_input("Hello, world!", "en", "es")
# print(translated_text)

# For JSON/dict
# translated_json = translate_input({"greeting": "Hello, world!", "farewell": "Goodbye, world!"}, "en", "es")
# print(translated_json)
