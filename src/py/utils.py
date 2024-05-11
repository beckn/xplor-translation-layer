## Utils file 
## Contains all the reusable functions 

import logging
import requests
import time
from datetime import datetime
import argostranslate.package
import argostranslate.translate
import pandas as pd
from functools import lru_cache, wraps
from config import *
import warnings
warnings.filterwarnings("ignore")

#############################################################################################################

userID = bhashini_userID
ulcaApiKey = bhashini_ulcaApiKey


#############################################################################################################
#############################################################################################################
#                                   UTILS FOR General Purpose                                               #
#############################################################################################################
#############################################################################################################



# Configure logging
logging.basicConfig(filename='../app.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_function_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)

        end_time = time.time()
        execution_time = end_time - start_time
        
        # Log the demarcation 
        logging.info(f"--------------------------------------------------------------------")
        # Log the function's input (arguments and keyword arguments) & function's output
        logging.info(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs} and function returned:  {result} ")    
        
        # Log the execution time
        logging.info(f"{func.__name__} execution time: {execution_time:.4f} seconds")

        return result
    return wrapper

# Example usage of the decorator
#@log_function_data
#def sample_function(a, b):
#    """Example function that adds two numbers."""
#    return a + b

# Call the decorated function
#result = sample_function(5, 7)


#############################################################################################################
#############################################################################################################
#                                   UTILS FOR TRANSLATION MODULE                                            #
#############################################################################################################
#############################################################################################################


argos_languages = {
"Arabic": "ar",
"Chinese": "zh",
"English": "en",
"French": "fr",
"German": "de",
#"Hindi": "hi",
"Italian": "it",
"Japanese": "ja",
"Polish": "pl",
"Portuguese": "pt",
"Turkish": "tr",
"Russian": "ru",
"Spanish": "es"
}

bhashini_languages = {
    "English": "en",
    "Hindi": "hi",
    "Gom": "gom",
    "Kannada": "kn",
    "Dogri": "doi",
    "Bodo": "brx",
    "Urdu": "ur",
    "Tamil": "ta",
    "Kashmiri": "ks",
    "Assamese": "as",
    "Bengali": "bn",
    "Marathi": "mr",
    "Sindhi": "sd",
    "Maithili": "mai",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Manipuri": "mni",
    "Telugu": "te",
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Santali": "sat",
    "Gujarati": "gu",
    "Odia": "or"
  }


#############################################################################################################

def get_language_code(input_language):
    """
    Retrieves the ISO language code for a given language name or code. This function supports
    languages listed in two dictionaries, handling variations in capitalization and recognizing
    both full names and short codes. If the language is not recognized, it returns a notification
    that the language is not supported.
    Args:
    input_language (str): The name of the language or its ISO code which could be in any case
                          (e.g., 'English', 'en', 'ENGLISH', 'En').
    Returns:
    str: The ISO code for the language if found (e.g., 'en' for English); otherwise,
         a string indicating that the language is not supported.
    Example usage:
    >>> get_language_code("English")
    'en'
    >>> get_language_code("en")
    'en'
    >>> get_language_code("HINDI")
    'hi'
    >>> get_language_code("german")
    'de'
    >>> get_language_code("xyz")
    'Language not supported.'
    """
    # Combine both language dictionaries
    combined_languages = {
        **argos_languages,
        **bhashini_languages
    }
    # Normalize the keys to handle different cases and create a reverse map for codes
    normalized_languages = {}
    for full_name, code in combined_languages.items():
        # Normalize full language names
        normalized_languages[full_name.lower()] = code
        # Map code to itself for reverse lookup
        normalized_languages[code.lower()] = code
    # Convert the input to lowercase for case-insensitive comparison
    input_language_normalized = input_language.lower()
    # Look up the input language in the normalized dictionary
    if input_language_normalized in normalized_languages:
        return normalized_languages[input_language_normalized]
    else:
        return "Language not supported."

#############################################################################################################

def select_translation_service(from_code, to_code):
    """
    Determines which translation service to use based on the provided source and target language codes.
    Args:
    from_code (str): The ISO code of the source language.
    to_code (str): The ISO code of the target language.
    Returns:
    str: A string indicating the translation service to use ("argos", "bhashini", or "combination").
    # Example usage
    print(select_translation_service("fr", "de"))  # Output: argos
    print(select_translation_service("hi", "gom"))  # Output: bhashini
    print(select_translation_service("ja", "ml"))  # Output: combination
    print(select_translation_service("ru", "sv"))  # Output: Unsupported language combination
    """
    # Language codes for Argos and Bhashini
    argos_codes = {"ar", "zh", "en", "fr", "de", "it", "ja", "pl", "pt", "tr", "ru", "es"}
    bhashini_codes = {"en", "hi", "gom", "kn", "doi", "brx", "ur", "ta", "ks", "as", "bn", "mr", "sd", "mai", "pa", "ml", "mni", "te", "sa", "ne", "sat", "gu", "or"}
    # Convert codes to lowercase to ensure case insensitivity
    from_code = from_code.lower()
    to_code = to_code.lower()
    # Determine the appropriate service
    if from_code in argos_codes and to_code in argos_codes:
        return "argos"
    elif from_code in bhashini_codes and to_code in bhashini_codes:
        return "bhashini"
    elif from_code in argos_codes and to_code in bhashini_codes:
        return "a_b"
    elif from_code in bhashini_codes and to_code in argos_codes:
        return "b_a"
    else:
        return "Unsupported language combination"



#############################################################################################################


@lru_cache(maxsize=128)
def install_translation_package(from_code : str = "en", to_code : str = None ) -> bool:
    """
    Attempts to install a translation package for Argos Translate, given a source
    and target language code, if it's not already cached as attempted. This function
    updates the package index, checks the available packages, and installs the required
    package if it has not been attempted previously.
    
    Parameters:
    - from_code (str): The ISO 639-1 language code of the source language. Defaults to 'en'.
    - to_code (str): The ISO 639-1 language code of the target language.
    
    Returns:
    - bool: True if the installation attempt was made (regardless of success), False otherwise.
    
    Utilizes an LRU (Least Recently Used) cache to remember installation attempts, preventing
    redundant installations for the same language pairs.
    """

    if not to_code:
        return False  # No target language code provided

    # Generate a unique identifier for the language pair
    package_id = f"{from_code}-{to_code}"

    # Update the Argos Translate package index
    argostranslate.package.update_package_index()
    
    # Get the list of available translation packages
    available_packages = argostranslate.package.get_available_packages()
    
    # Find the package that matches the specified from and to languages
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        ), None
    )

    # Attempt to install the package if found
    if package_to_install:
        print(f"Attempting to install package: {package_id}")
        argostranslate.package.install_from_path(package_to_install.download())
        return True
    else:
        print(f"No package found for translating from '{from_code}' to '{to_code}'.")
        return False  # Package not found or installation not attempted

# Example usage
#success = install_translation_package(from_code="en", to_code="hi")
#print(f"Installation attempted: {success}")
#############################################################################################################


@lru_cache(maxsize=128)  # Cache the most recent 128 unique translation requests
def translate_text(text: str, from_code: str = "en", to_code: str = "pt") -> str:
    """
    Translates the given text from the source language to the target language using
    Argos Translate, with caching to avoid retranslating the same text.
    
    Parameters:
    - text (str): The text to be translated.
    - from_code (str): The ISO 639-1 language code of the source language. Defaults to 'en'.
    - to_code (str): The ISO 639-1 language code of the target language. Defaults to 'pt'.
    
    Returns:
    - str: The translated text.
    
    Utilizes an LRU (Least Recently Used) cache to store the results of recent translations
    and quickly retrieve them for repeated requests, reducing the need for redundant translations.
    """

    # Load installed languages
    installed_languages = argostranslate.translate.get_installed_languages()

    # Select source and target languages
    from_lang = next((lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next((lang for lang in installed_languages if lang.code == to_code), None)

    if not from_lang or not to_lang:
        return "Language code not found or language not installed."

    # Get the translation model for the desired language pair
    translate = from_lang.get_translation(to_lang)

    # Translate text
    translated_text = translate.translate(text)

    return translated_text

# Example usage
#translated_text = translate_text("Hello, world!")
#print(translated_text)


#############################################################################################################


@lru_cache(maxsize=128)  # Cache the most recent 128 unique translation requests
def bhashini_translate(text: str, from_code: str = "en", to_code: str = "te", user_id: str = userID, api_key: str = ulcaApiKey ) -> dict:
    """Translates text from source language to target language using the Bhashini API.
    Args:
        text (str): The text to translate.
        from_code (str): Source language code. Default is 'en' (English).
        to_code (str): Target language code. Default is 'te' (Telugu).
        user_id (str): User ID for the API.
        api_key (str): API key for authentication.
    Returns:
        dict: A dictionary with the status code, message, and translated text or error info.
    """
    url = 'https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline'
    headers = {
        "Content-Type": "application/json",
        "userID": user_id,
        "ulcaApiKey": api_key
    }
#####    
    payload = {
        "pipelineTasks": [{"taskType": "translation", "config": {"language": {"sourceLanguage": from_code, "targetLanguage": to_code}}}],
        "pipelineRequestConfig": {"pipelineId" : "64392f96daac500b55c543cd"}
    }
##### 
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return {"status_code": response.status_code, "message": "Error in translation request", "translated_content": None}
#####
    response_data = response.json()
    service_id = response_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]
    callback_url = response_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
    headers2 = {
        "Content-Type": "application/json",
        response_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]: response_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]
    }
#####
    compute_payload = {
        "pipelineTasks": [{"taskType": "translation", "config": {"language": {"sourceLanguage": from_code, "targetLanguage": to_code}, "serviceId": service_id}}],
        "inputData": {"input": [{"source": text}], "audio": [{"audioContent": None}]}
    }
#####
    compute_response = requests.post(callback_url, json=compute_payload, headers=headers2)
    if compute_response.status_code != 200:
        return "Error in translation"
#####
    compute_response_data = compute_response.json()
    translated_content = compute_response_data["pipelineResponse"][0]["output"][0]["target"]
#####
    return translated_content
