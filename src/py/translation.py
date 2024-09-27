# File for the Translation Service
from utils import *
import json
from typing import Union, List
from fastapi import HTTPException

import sys
sys.path.append('.')

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
@log_function_data
def translate_input(input_data: Union[str, dict, List[Union[str,dict]]], from_ln: str, to_ln: str, excluded_keys: List[str] = None) -> Union[str, dict, List[Union[str, dict]]]:
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
    max_elements = 50
    # Resolve ISO codes for the languages
    from_code = get_language_code(from_ln)
    to_code = get_language_code(to_ln)
########################################################################################
    # Handle unsupported languages
    if from_code == "Language not supported" or to_code == "Language not supported":
        return f"One or both languages are not supported: {from_ln}, {to_ln}"
########################################################################################
    # Determine the translation service to use
    service = select_translation_service(from_code, to_code)
    if service == "unsupported language combination for translation":
        return "Unsupported language combination for translation"
#######################
    # Check and install the translation package if necessary
    if service == "argos":
        # Check and install the translation package if necessary
        if not install_translation_package(from_code, to_code):
            return "Required translation package could not be installed."
        def translate_item(text): return translate_text(text, from_code, to_code)
#######################
    elif service == "bhashini":
        def translate_item(text): return bhashini_translate(text, from_code, to_code)
#######################
    elif service == "a_b":
        if not install_translation_package(from_code, 'en'):
            return "Required translation package could not be installed."
        def translate_item(text): return bhashini_translate(translate_text(text, from_code, 'en'), 'en', to_code)
#######################
    elif service == "b_a":
        if not install_translation_package('en', to_code):
            return "Required translation package could not be installed."
        def translate_item(text): return translate_text(bhashini_translate(text, from_code, 'en'), 'en', to_code)
#######################
    else:
        return "Unsupported language combination for translation"
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
    if isinstance(input_data, str):
        input_data = input_data.lower()
        return translate_item(input_data)
#######################
    elif isinstance(input_data, dict):
        if excluded_keys is None:
            excluded_keys = []
        input_data = {key: value.lower() if isinstance(value, str) else str(value) for key, value in input_data.items()}
        input_data = {key.replace('\n', ' '): value.replace('\n', ' ') for key, value in input_data.items()}

        excluded_data = {key: value.lower() if isinstance(value,str) else str(value) for key, value in input_data.items() if key in excluded_keys}
        excluded_data = {key.replace('\n', ' '): value.replace('\n', ' ') for key, value in excluded_data.items()}

        translated_included_data = translate_item(input_data)
        return {**translated_included_data, **excluded_data}
#######################
    elif isinstance(input_data, list):
        if len(input_data) > max_elements:
            raise HTTPException(status_code=400, detail=f"Number of elements in the list exceeds the limit of {max_elements}.")
        processed_list = []
        for item in input_data:
            if isinstance(item, str):
                item = item.lower()
            elif isinstance(item, dict):
                if excluded_keys is None:
                    excluded_keys = []
                excluded_data = {key: value for key, value in item.items() if key in excluded_keys}
                item = {key: value.lower() if isinstance(value, str) else str(value) for key, value in item.items()}
                item = {key.replace('\n', ' '): value.replace('\n', ' ') for key, value in item.items()}
                translated_included_data = translate_item(item)
                modified_data = {**translated_included_data, **excluded_data}
            processed_list.append(modified_data)
        return processed_list
#######################
    else:
        return "Unsupported input type."
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################


# Example usage
# For plain text
# translated_text = translate_input("Hello, world!", "en", "es")
# print(translated_text)

# For JSON/dict
# translated_json = translate_input({"greeting": "Hello, world!", "farewell": "Goodbye, world!"}, "en", "es")
# print(translated_json)