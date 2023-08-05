import os

from django.conf import settings
from django.http import HttpResponse
from datetime import date, datetime

class Log():
    @classmethod
    def __set_log_file(self, folder_name='logs'):
        d = date.today().strftime("%d")
        m = date.today().strftime("%m")
        Y = date.today().strftime("%Y")
        folder = settings.BASE_DIR / folder_name / Y / m / d
        os.makedirs(os.path.dirname(folder), exist_ok=True)
        file = str(folder) + '.log'
        if not os.path.exists(file):
            open(file, 'w')
        return file

    @classmethod
    def __get_log_file(self):
        folder_name = 'logs'
        if hasattr(settings, 'LOG_FOLDER_NAME'):
            folder_name = settings.LOG_FOLDER_NAME
        return self.__set_log_file(folder_name=folder_name)

    @classmethod
    def __write(self, text='', args=[], log_type=None):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.basename(__file__)

        log_file = self.__get_log_file()
        with open(log_file, 'a') as out_file:
            text = '{datetime}: {request_type} {path}/{filename} - {text} {args}{delimiter}'.format(
                datetime=str(datetime.now()), request_type=log_type, path=path,
                filename=filename, text=text, args=args,
                delimiter=os.linesep)
            out_file.write(text)
        return HttpResponse(text)

    @classmethod
    def request(self, text='', args=[]):
        return Log.__write(text=text, args=args, log_type="REQUEST")

    @classmethod
    def response(self, text='', args=[]):
        return Log.__write(text=text, args=args, log_type="RESPONSE")
