message_add_devices = {
    1: 'Dodano nowe urzadzenie', 
    2: 'Nie udało sie dodać urzadzenia'
}

message_server_connection = {
    1: 'Połączono z serwerem',
    2: 'Nie połączono z serwerem '
}


class Messages:
    def message_device(self,number):
        return message_add_devices[number]

    def message_serwer(self,number):
        return message_server_connection[number]

    class ClientException(Exception):
    
        def __init__(self, code, message=None, details=None,
                 request_id=None):
            self.code = code
            self.message = message or getattr(self.__class__, 'message', None)
            self.details = details
            self.request_id = request_id

    def __str__(self):
        formatted_string = "%s" % self.message
        if self.code >= 100:
            formatted_string += f" (HTTP {self.code})"  
        return formatted_string


    class BadRequest(ClientException):
        http_status = 400
        message = "Bad request"


    class Unauthorized(ClientException):
        http_status = 401
        message = "Unauthorized"

    class Forbidden(ClientException):
        http_status = 403
        message = "Forbidden"


    class NotFound(ClientException):
        http_status = 404
        message = "Not found"


    class NotAcceptable(ClientException):
        http_status = 406
        message = "Not Acceptable"


    class OverLimit(ClientException):
        http_status = 413
        message = "Over limit"
