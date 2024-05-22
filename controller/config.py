import datetime

get_datetime = datetime.datetime.now()
formated_datetime = get_datetime.strftime('%Y-%M-%d_%H-%M-%S')
string_datetime = str(formated_datetime)

WS_MAIN_LOG_NAME = f'WS_Log_{string_datetime}.txt'

APPDATA = None
OUTPUT = None