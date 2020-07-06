class ValueIsTooSmallError (Exception):
    def __init__(self, message):
        super(ValueIsTooSmallError, self).__init__(message)

class ValueIsTooLargeError (Exception):
    def __init__(self, message):
        super(ValueIsTooLargeError, self).__init__(message)