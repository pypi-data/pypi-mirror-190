class Newsito():
    def __init__(self, message=None):
        self.message = message
        if self.message is None:
            print("Don't you want to say anything?")
        else:
            print(self.message)
