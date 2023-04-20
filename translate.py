import html
import requests
import xml.etree.ElementTree as ET
import os
import time

start_time = time.time()

# Set your subscription key and endpoint for the Azure Cognitive Services API
subscription_key = os.environ.get('AZURE_TRANSLATION_KEY')
endpoint = "https://api.cognitive.microsofttranslator.com/translate"

# Set the language codes for the source and target languages
source_language = 'en'
target_language = 'pt-pt'

# Parse the XML file and retrieve the values inside the <source> tags
tree = ET.parse('pt_PT-ui.xml')
root = tree.getroot()
sources = [source.text for source in root.findall('.//source')]
# Create a list to store the translated values
translations = []

# Loop through the source values and retrieve translations from the Azure Cognitive Services API
for source in sources:
    # Construct the request URL
    params = {
        "api-version": "3.0",
        "from": "en",
        "to": "pt"
    }

    # Set the request headers and body
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Region": "westeurope"}
    body = [{'text': source}]

    # Send the request to the Azure Cognitive Services API and retrieve the response
    response = requests.post(endpoint, headers=headers,
                             params=params, json=body)
    response.raise_for_status()

    # Retrieve the translated value from the response
    translation = html.unescape(response.json()[0]['translations'][0]['text'])
    translations.append(translation)
    print(translation)

num_translations = len(root.findall('.//translation'))
if len(translations) < num_translations:
    # add empty strings to the translations list if there aren't enough translations
    translations.extend([''] * (num_translations - len(translations)))

for i, translation in enumerate(root.findall('.//translation')):
    translation.text = translations[i]\


# Save the modified XML file
tree.write('pt_PT_translated.xml')
print("--- Translation took %s seconds ---" % (time.time() - start_time))
