from googletrans import Translator
from datetime import datetime

def ConvertSlug(text):
    translator = Translator()
    
    try:
        translated = translator.translate(text, src='fa', dest='en')
        if translated is not None:
            slug = f"{translated.text.replace(' ', '-', -1)}-{datetime.now().year}-{datetime.now().month}-{datetime.now().day}-{datetime.now().microsecond}".lower()
            return slug
        else:
            print ('ok')
            return None
    except Exception as e:
        print(f"Error in ConvertSlug: {str(e)}")
        return None