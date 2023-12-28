from django.core.cache import cache
from datetime import timedelta, datetime
from django.conf import settings
from random import randint
import random
from django.core.mail import send_mail
import requests

SMS_IR_API_KEY = None
SMS_LINE_NUMBER = None
OTP_EXPIRATION_MINUTES = 1
OTP_EXPIRATION_SECONDS = 60  # 1 minute has 60 seconds
sms = None


class OTPManager:

    def send_email_to_user(self, user_value, code):

        subject = 'الو استخدام | کد تایید'
        message = f"""
        Code: {code}
        کد تایید شما در الو استخدام میباشد 
         این کد را در اختیار کسی نزارید
         aloestekhdam.com
        """
        from_email = 'no-reply@aloestekhdam.com'
        recipient_list = []

        recipient_list.append(user_value)
        send_mail(subject, message, from_email, recipient_list)

    def send_sms_to_user(self, phone_number, code):
        if settings.DEBUG == False:
            data = {'bodyId': 146653, 'to': str(phone_number), 'args': [str(code)]}
            result = requests.post('https://console.melipayamak.com/api/send/shared/a7c2e5ae7d9a4d828fece432bedbe3f0',
                                   json=data)

        return "Code was sent"

    def generate_otp(self, user_data):
        otp = str(randint(1000, 9000))
        cache_key = f'otp_type:{user_data.get("value")}'
        expiration_time = datetime.now() + timedelta(minutes=OTP_EXPIRATION_MINUTES,
                                                     seconds=OTP_EXPIRATION_SECONDS)
        cache.set(cache_key, (otp, expiration_time), timeout=OTP_EXPIRATION_MINUTES * OTP_EXPIRATION_SECONDS)
        return otp, expiration_time

    def verify_otp(self, user_data, otp_code):
        cache_key = f'otp_type:{user_data.get("value")}'
        cached_data = cache.get(cache_key)
        if not cached_data:
            return False, None

        cached_otp, expiration_time = cached_data
        if cached_otp == str(otp_code):
            remaining_time = int((expiration_time - datetime.now()).total_seconds())
            cache.delete(cache_key)
            return True, remaining_time
        return False, None
