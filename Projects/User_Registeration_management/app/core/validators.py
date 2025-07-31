import re
# using regax for password generating
password_regex = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
)

def is_valid_password(password: str) -> bool:
    valid = bool(password_regex.match(password))
    if not valid:
        print(f"[DEBUG] Password failed: {password}")
    return valid


def is_email_or_phone(value: str) -> bool:
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    phone_regex = r"^[6-9]\d{9}$"
    return re.match(email_regex, value) or re.match(phone_regex, value)
