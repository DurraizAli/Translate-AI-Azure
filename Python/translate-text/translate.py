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
        


        ## Choose target language



        # Translate text



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()