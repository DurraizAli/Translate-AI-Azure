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

## Get user input for translation
def get_user_input():
    """Prompts the user for text to translate and options for profanity action and alignment.

    Returns:
        str: The text to translate.
        str: The chosen profanity action ("Marked", "NoAction", or "Deleted").
        bool: Whether to include alignment information in the translation.
    """
    while True:
        inputText = input("Enter text to translate ('quit' to exit):")
        if inputText.lower() == "quit":
            return inputText, None, None

        profanity_options = ["Marked", "Deleted", "NoAction"]
        print("Choose Profanity Action:")
        for i, option in enumerate(profanity_options):
            print(f"{i+1}. {option}")
        profanity_choice = int(input("Enter a number (1-3): ")) - 1
        if profanity_choice not in range(len(profanity_options)):
            print("Invalid choice. Please select a number between 1 and 3.")
            continue

        alignment_choice = input("Include alignment information (y/n)? ").lower()
        if alignment_choice not in ("y", "n"):
            print("Invalid choice. Please enter 'y' or 'n'.")
            continue

        return inputText, profanity_options[profanity_choice], alignment_choice == "y"

def translate_text(client, input_text, target_language, profanity_action, alignment):
    """Translates the given text.

    Args:
        client (TextTranslationClient): The translation client.
        input_text (str): The text to translate.
        target_language (str): The target language code.
        profanity_action (str): The profanity action to take.
        alignment (bool): Whether to include alignment information.
    """
    input_text_elements = [InputTextItem(text=input_text)]
    translationResponse = client.translate(
        content=input_text_elements,
        to=[target_language],
        include_alignment=alignment,
        include_sentence_length=True,
        profanity_action=profanity_action
    )
    translation = translationResponse[0] if translationResponse else None
    if translation:
        sourceLanguage = translation.detected_language
        for translated_text in translation.translations:
            print(f"'{input_text}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'\nAlignment: '{translated_text.alignment}' \nProfanity Action: {profanity_action}.")
            
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
        while True:
            # Get user input for translation
            inputText, profanityAction, alignment = get_user_input()
            if inputText.lower() == "quit":
                break

            # Translate text
            translate_text(client, inputText, targetLanguage, profanityAction, alignment)
    except Exception as ex:
            print(ex)

if __name__ == "__main__":
    main()