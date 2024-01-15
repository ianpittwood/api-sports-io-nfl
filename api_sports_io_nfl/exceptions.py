import inspect
import sys
import traceback


class ApiError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message=None, response=None):
        self.message = message
        if self.message is None:
            self.message = "An unknown API error occurred."
        self.response = response
        current_frame = inspect.currentframe()
        self.line_number = current_frame.f_lineno
        self.file_name = current_frame.f_back

    def __str__(self):
        return f"{self.message} ({self.file_name}:{self.line_number})"


class Api401Error(ApiError):
    """Raised when API returns 401 error"""

    def __init__(self, message=None, response=None):
        self.message = message
        if self.message is None:
            self.message = "API returned a 401 error. Check your API key and usage limits."
        super().__init__(self.message)
        if self.response is not None:
            self.response_errors = self.response.json().get("errors", None)

    def __str__(self):
        s = super().__str__()
        if self.response_errors is not None:
            s += f"\nResponse Errors: {self.response_errors}"
        return s


class Api404Error(ApiError):
    """Raised when API returns 404 error"""

    def __init__(self, message=None, response=None):
        self.message = message
        if self.message is None:
            self.message = "API returned a 404 error. Check your parameters."
        super().__init__(self.message)
        if self.response is not None:
            self.response_errors = self.response.json().get("errors", None)

    def __str__(self):
        s = super().__str__()
        if self.response_errors is not None:
            s += f"\nResponse Errors: {self.response_errors}"
        return s


class Api429Error(ApiError):
    """Raised when API returns 429 error"""

    def __init__(self, message=None, response=None):
        self.message = message
        if self.message is None:
            self.message = "API returned a 429 error."
        super().__init__(self.message)
        if self.response is not None:
            self.response_errors = self.response.json().get("errors", None)

    def __str__(self):
        s = super().__str__()
        if self.response_errors is not None:
            s += f"\nResponse Errors: {self.response_errors}"
        return s


class Api500Error(ApiError):
    """Raised when API returns 500 error"""

    def __init__(self, message=None, response=None):
        self.message = message
        if self.message is None:
            self.message = "API returned a 500 server error."
        super().__init__(self.message)
        if self.response is not None:
            self.response_errors = self.response.json().get("errors", None)

    def __str__(self):
        s = super().__str__()
        if self.response_errors is not None:
            s += f"\nResponse Errors: {self.response_errors}"
        return s


EXCEPTION_MAP = {
    401: Api401Error,
    404: Api404Error,
    429: Api429Error,
    500: Api500Error,
}
