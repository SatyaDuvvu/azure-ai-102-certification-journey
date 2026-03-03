from dotenv import load_dotenv
import os

# Import namespaces
# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)


        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            """ text = ["Good Hotel and staff The Royal Hotel, London, UK 3/2/2018",
                    "Clean rooms, good service, great location near Buckingham Palace and Westminster Abbey", 
                    "and so on. We thoroughly enjoyed our stay. The courtyard is very peaceful and we went to ",
                    "a restaurant which is part of the same group and is Indian ( West coast so plenty of fish) ",
                    "with a Michelin Star. We had the taster menu which was fabulous.The rooms were very well ",
                    "appointed with a kitchen, lounge, bedroom and enormous bathroom. Thoroughly recommended."] """
            
            # Get language
            print("=" * 60)
            
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))

            print("=" * 60)
            # Get sentiment
            detectedSentiment = ai_client.analyze_sentiment(documents=[text])[0]
            print('\nSentiment: {}'.format(detectedSentiment.sentiment))


            print("=" * 60)
            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases)>0:
                for phrase in phrases:
                    print(phrase)

            print("=" * 60)
            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities)>0:
                for entity in entities:
                    print(f"entity text :{entity.text}, entity category: {entity.category}")

            print("=" * 60)
            # Get linked entities

            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities)>0:
                for entity in entities:
                    print(f"linked entity name :{entity.name}, linked entity category: {entity.url}")



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()