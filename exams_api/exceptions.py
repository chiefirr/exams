from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class ExamsAPIError(APIException):
    """
    Exams error class
    returns status code: 400
    """
    def __init__(self, msg):
        APIException.__init__(self, msg)
        self.status_code = HTTP_400_BAD_REQUEST
        self.message = msg
