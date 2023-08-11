from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateFileMaxSizeInMb:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.__megabytes_to_bytes():
            raise ValidationError(self.__get_exception_message())

    def __megabytes_to_bytes(self):
        return self.max_size * 1024 * 1024


    def __get_exception_message(self):
        return f"Max file size is {self.max_size:.02f} MB."
