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

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        translatorRegion = os.getenv('TRANSLATOR_REGION')
        translatorKey = os.getenv('TRANSLATOR_KEY')

        # Create client using endpoint and key
        credential = TranslatorCredential(translatorKey, translatorRegion)
        client = TextTranslationClient(credential)


        ## Choose target language
        languagesResponse = client.get_languages(scope="translation")
        ## Print supported languages
        print("{} languages supported.".format(len(languagesResponse.translation)))
        print("(See https://learn.microsoft.com/azure/ai-services/translator/language-support#translation)")
        print("Enter a target language code for translation (for example, 'en'):")
        targetLanguage = "xx"
        supportedLanguage = False
        ## Check if language is supported
        while supportedLanguage == False:
            ## Get target language from user
            targetLanguage = input()
            ## Check if language is supported
            if  targetLanguage in languagesResponse.translation.keys():
                ## Set supportedLanguage to True to exit loop
                supportedLanguage = True
            else:
                print("{} is not a supported language.".format(targetLanguage))

        # Translate text
        inputText = ""
        ## Loop until user enters 'quit'
        while inputText.lower() != "quit":
            ## Get text to translate from user
            inputText = input("Enter text to translate ('quit' to exit):")
            if inputText != "quit":
                ## Translate text
                input_text_elements = [InputTextItem(text=inputText)]
                translationResponse = client.translate(content=input_text_elements, to=[targetLanguage])
                translation = translationResponse[0] if translationResponse else None
                if translation:
                    sourceLanguage = translation.detected_language
                    for translated_text in translation.translations:
                        print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")


    except Exception as ex:
        print(ex)
        


if __name__ == "__main__":
    main()