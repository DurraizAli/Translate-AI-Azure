from dotenv import load_dotenv
import os

 # import namespaces
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem


## load configuration
def load_configuration():
    """
    Loads environment variables for Azure translation service.
    Returns:
        translatorRegion (str): The configured Azure region.
        translatorKey (str): The configured Azure translation key.
    """
    load_dotenv()
    translatorRegion = os.getenv('TRANSLATOR_REGION')
    translatorKey = os.getenv('TRANSLATOR_KEY')
    if not translatorRegion or not translatorKey:
        raise ValueError("Please provide a valid Azure region and key in the .env file.")
    return translatorRegion, translatorKey

## create traslation client
def create_translation_client():
    """
    Creates a translation client using the Azure region and key.
    Returns:
        client (TextTranslationClient): The translation client.
    """
    translatorRegion, translatorKey = load_configuration()
    credential = TranslatorCredential(translatorKey, translatorRegion)
    client = TextTranslationClient(credential)
    return client

##get supported languages
def get_supported_languages():
    """
    Gets the supported languages for translation.
    Returns:
        languagesResponse (GetLanguagesResult): The supported languages.
    """
    client = create_translation_client()
    languagesResponse = client.get_languages(scope="translation")
    return languagesResponse

## select target language
def select_target_language(supported_languages):
    """
    Prompts the user to choose a target language from the supported languages.
    Args:
        supported_languages (list): A list of supported languages (code, name tuples).
    Returns:
        str: The chosen target language code.
    """
    print("Supported languages:")
    for code, name in supported_languages:
        print(f"- {code} ({name})")
    ## get target language
    while True:
        target_language = input("Enter a target language code (or 'q' to quit): ").lower()
        if target_language == 'q':
            exit()
        ## check if target language is supported
        if target_language in [code for code, _ in supported_languages]:
            return target_language
        else:
            print(f"{target_language} is not a supported language.")


def main():
    try:
        # Get supported languages
        languages = get_supported_languages()
        print("Supported languages: ")
        for language in languages:
            print("\t", language)
    except Exception as ex:
        print(ex)
        


if __name__ == "__main__":
    main()