import sys

def error_message_detail(error, error_detail: sys):
    """
    This function takes an error and its details and returns a formatted string with the error message.
    It extracts the file name and line number from the error details and includes them in the error message.
    The error message is formatted as:
    "Error occurred in script: [file_name] at line number: [line_number] error message: [error_message]"
    :param error: The error object that contains the error message.
    :param error_detail: The sys module that contains the error details.
    :return: A formatted string with the error message, file name, and line number.
    :rtype: str
    :raises: None
    Example:
    >>> error = ValueError("Invalid value")
    >>> error_detail = sys
    >>> error_message_detail(error, error_detail)    
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, line_number, str(error)
    )
    return error_message
    

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        """
        This function initializes the CustomException class with an error message and its details.
        It formats the error message using the error_message_detail function and sets it as the exception message.
        :param error_message: The error message to be displayed.
        :param error_detail: The sys module that contains the error details.
        :return: None
        :rtype: None
        :raises: None
        Example:
        >>> error_message = "Invalid value"
        >>> error_detail = sys
        >>> custom_exception = CustomException(error_message, error_detail)
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """
        This function returns the string representation of the CustomException class.
        It returns the error message set during initialization.
        :return: The error message as a string.
        :rtype: str
        :raises: None
        Example:
        >>> custom_exception = CustomException("Invalid value", sys)
        >>> str(custom_exception)
        "Error occurred in script: [file_name] at line number: [line_number] error message: [error_message]"
        """
        return self.error_message 
