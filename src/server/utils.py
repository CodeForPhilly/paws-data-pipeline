import re

def standardize_phone_number(phone):
    """Standardize phone number format.
    
    Args:
        phone (str): The phone number to standardize.
    
    Returns:
        str: The standardized phone number.
    """
    # Remove all non-numeric characters
    phone = re.sub(r'\D', '', phone)

    # if the phone number is less than 10 digits, it's invalid
    if len(phone) < 10:
        return None

    # If the phone number is exactly 10 digits, return as is
    if len(phone) == 10:
        return phone

    # if the phone number is greater than 10 digits, take the last 10 digits
    if len(phone) > 10:
        return f'{phone[-10:]}'

    # anything else we ignore
    return None
