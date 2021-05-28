from logging import getLogger

def override(f):
    return f


class EventHandler:

    def __init__(self):
        self.handlers = []
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