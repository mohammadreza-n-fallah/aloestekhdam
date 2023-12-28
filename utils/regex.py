import re


def email_regex(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Use re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def phone_regex(phone):
    mobile_regex = "^(?:(?:(?:\\+?|00))|(0))?((?:90|91|92|93|99)[0-9]{8})$"
    if (re.search(mobile_regex, phone)):
        return True
    return False


def user_type_regex(user):
    status = False
    user_type = ""
    check_email = email_regex(email=user)
    check_phone = phone_regex(phone=user)
    if check_email:
        status = False
        user_type = "email"
    if check_phone:
        status = True
        user_type = "phone"

    return status, user_type
