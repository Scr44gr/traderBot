from logging import getLogger
from ast import literal_eval

def override(f):
    return f

def safe_number(number):
    str_value = str(number)

    if str_value.count('.'):
        value = str_value.replace('.', '')
        if value.isdigit():
            if isinstance(literal_eval(str_value), float):
                return float(str_value)
            elif isinstance(literal_eval(str_value), int):
                return int(str_value)
    
    return int(str_value)

class EventHandler:

    def __init__(self):
        self.handlers = {}
        self.__logger = getLogger('EventHandler')
    
    def call_event(self, name):
        if name in self.handlers:
            try:
                for handler in self.handlers[name]:
                    handler() 
            except:
                self.__logger.error('on call_event error', exc_info=1)
    
    def on(self, name):
        def register_event(handler):
            if name in self.handlers:
                self.handlers[name].append(handler)
            else:
                self.handlers[name] = [handler]
            return handler
        return register_event