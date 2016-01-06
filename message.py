class message:
    def __init__(self, command, data):
        self.command = command
        self.data = data

    def getMessage(self):
        message = ""
        message += self.command
        message += "\n"
        message += str(self.data.count("\n")+1)
        message += "\n"
        message += self.data
        return message

    @staticmethod
    def readMessage(instream):
        command = instream.readline().strip()
        lines = int(instream.readline().strip())
        data = ""
        for line in range(lines):
            data+=instream.readline()
        return message(command, data)

    def __str__(self):
        return self.getMessage()
