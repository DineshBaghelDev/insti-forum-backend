from email_validator import validate_email, EmailNotValidError

def check_user_input(email):
    """Returns (is_valid, error_message)"""
    try:
        validate_email(email, check_deliverability=False)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)
