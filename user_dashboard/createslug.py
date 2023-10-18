from googletrans import Translator
from datetime import datetime

def ConvertSlug(text):
    translator = Translator()
    
    translated = translator.translate(text, src='fa', dest='en')
    slug = f"{translated.text.replace(' ', '-', -1)}-{datetime.now().year}-{datetime.now().month}-{datetime.now().day}-{datetime.now().microsecond}".lower()
    return slug

