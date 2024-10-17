from dotenv import load_dotenv
import os

from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem

# Get Configuration Settings
def load_configuration():
     load_dotenv()
     translatorRegion = os.getenv('TRANSLATOR_REGION')
     translatorKey = os.getenv('TRANSLATOR_KEY')
     return translatorRegion, translatorKey

## Create client
def create_client(translatorRegion, translatorKey):
    credential = TranslatorCredential(translatorKey, translatorRegion)
    client = TextTranslationClient(credential)
    return client

## show supported languages
def show_supported_languages(languagesResponse):
    count = 0
    for language_code, language_data in languagesResponse.translation.items():
        print(f"[{language_code}: {language_data['name']}]", end=" ")
        count += 1
        if count % 3 == 0:
            print()

## Get target language code for translation
def get_target_language(languagesResponse):
    print("Enter a target language code for translation (for example, 'en'):")
    targetLanguage = "xx"
    supportedLanguage = False
    while supportedLanguage == False:
        targetLanguage = input()
        if  targetLanguage in languagesResponse.translation.keys():
            supportedLanguage = True
        else:
            print("{} is not a supported language.".format(targetLanguage))
    return targetLanguage 

def main():
    try:
        # Load configuration settings
        translatorRegion, translatorKey = load_configuration()
        # Create client using endpoint and key
        client = create_client(translatorRegion, translatorKey)
        
        ## Choose target language
        languagesResponse = client.get_languages(scope="translation")
        
        ## Show supported languages
        show_supported_languages(languagesResponse)
        
        ## Get target language code for translation
        targetLanguage = get_target_language(languagesResponse)

        # Translate text
        inputText = ""
        ## Loop until user enters 'quit'
        while inputText.lower() != "quit":
            ## Get text to translate from user
            inputText = input("Enter text to translate ('quit' to exit):")
            profanityAction = "Marked"
            if inputText != "quit":
                ## Translate text
                input_text_elements = [InputTextItem(text=inputText)]
                translationResponse = client.translate(content=input_text_elements, to=[targetLanguage], include_alignment=True, include_sentence_length=True, profanity_action=profanityAction)
                translation = translationResponse[0] if translationResponse else None
                if translation:
                    sourceLanguage = translation.detected_language
                    for translated_text in translation.translations:
                        print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}' \nAlignment: '{translated_text.alignment}' \nProfanity Action: {profanityAction}.")
    except Exception as ex:
            print(ex)

if __name__ == "__main__":
    main()