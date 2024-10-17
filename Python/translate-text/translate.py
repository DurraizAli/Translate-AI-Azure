from dotenv import load_dotenv
import os

 # import namespaces
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem



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



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()