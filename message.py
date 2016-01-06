from encryption import Encrypter as enc

class message:
    def __init__(self, command, data):
        self.command = command
        self.data = data

    def getMessage(self):
        message = ""
        message += enc.encrypt(self.command)
        message += "\n"
        message += enc.encrypt(str(self.data.count("\n")+1))
        message += "\n"
        for line in self.data.split("\n"):
            message += enc.encrypt(line)
            message += "\n"
        return message

    @staticmethod
    def readMessage(instream):
        command = instream.readline().strip()
        command = enc.decrypt(command)
        lines = int(enc.decrypt(instream.readline().strip()))
        data = ""
        for line in range(lines):
            data+=enc.decrypt(instream.readline().strip())+"\n"
        return message(command, data)

    def __str__(self):
        return self.getMessage()
