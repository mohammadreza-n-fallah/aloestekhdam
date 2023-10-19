from datetime import datetime
from unidecode import unidecode

def ConvertSlug(text):
    try:
        # Transliterate the text using unidecode
        transliterated_text = unidecode(text)
        
        # Replace spaces with dashes, remove other special characters, and create the slug
        slug = '-'.join(transliterated_text.split())
        slug = slug.lower()

        # Append a timestamp to make the slug unique
        slug += f"-{datetime.now().year}-{datetime.now().month}-{datetime.now().day}-{datetime.now().microsecond}"

        return slug
    except Exception as e:
        print(f"Error in ConvertSlug: {str(e)}")
        return None
