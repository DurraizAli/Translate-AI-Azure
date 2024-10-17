# Translate-AI-Azure
App in python to translate text using the Translator AI service from microsoft Azure

1. Create the Azure Translator service in the azure portal with the next settings:
    Subscription: Your Azure subscription
    Resource group: Choose or create a resource group
    Region: Choose any available region
    Name: Enter a unique name
    Pricing tier: Select F0 (free), or S (standard) if F is not available.
    Responsible AI Notice: Agree.

2. Create the .env file and add the next parameters:
    TRANSLATOR_KEY=your_translator_key
    TRANSLATOR_REGION=your_translator_region