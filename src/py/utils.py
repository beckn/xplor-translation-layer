## Utils file 
## Contains all the reusable functions 

import logging
import time
from datetime import datetime
import argostranslate.package
import argostranslate.translate
import pandas as pd
from functools import lru_cache, wraps
import warnings
warnings.filterwarnings("ignore")


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

















