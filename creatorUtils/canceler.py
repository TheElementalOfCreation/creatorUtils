class Canceler(object):
    def __init__(self, fake = False):
        self.__can = False
        self.__fake = fake

    def cancel(self):
        if not self.__fake:
            self.__can = True

    def get(self):
        return self.__can

    def reset(self):
        self.__can = False

FAKE = Canceler(True)
