

import re  # Import the regular expression module for email validation

def validate_input(input_value, length=None, is_email=False, expected_type=None, is_password=False):
    """
    Validate input based on specified conditions.

    Parameters:
        input_value (any): The input value to be validated.
        length (int): The maximum length allowed for the input (optional).
        is_email (bool): Whether the input should be a valid email address (optional).
        expected_type (type): The expected data type of the input (optional).

    Returns:
        bool: True if input passes all validation conditions, False otherwise.
        str: Error message if validation fails.
    """
    # Check for length validation
    if length is not None and len(str(input_value)) > length:
        return False, f"Input length exceeds {length} characters."

    # Check for email validation
    if is_email:
        valid_email = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not re.match(valid_email, str(input_value)):
            return False, "Invalid email address."
    #check for password validation
    if is_password:
        
        valid_spec_password = "!£$%^&**@"
        
        
        if True not in [c.isdigit() for c in input_value]: 
            return False, "Must contain numbers."
        elif True not in [c in input_value for c in valid_spec_password ]:
            return False, "Must contain special characters."
        elif not len(input_value) >=8:
            return False, "Must be at least 8 chars long."
    # Check for type validation
    if expected_type is not None and isinstance(input_value, expected_type):
        return False, f"Input must be of type {expected_type}."

    return True, None  # Input passes all validation conditions



        
