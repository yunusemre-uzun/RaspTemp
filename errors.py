class DatabaseException(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self): 
        if self.error_code == 1:
            return "Cloud database conncetion error. Check internet connection."
        if self.error_code == 2:
            return "Cloud database write error. {}".format(self.error_message) 