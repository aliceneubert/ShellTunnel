from Crypto.Cipher import AES
import base64

class Encrypter:
    @staticmethod
    def encrypt(text):
        if len(text)%16 != 0:
            return Encrypter.encrypt(text+" ")
        text = text.rjust(32)
        cipher = AES.new(Encrypter.getKey(), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(text))

    @staticmethod
    def decrypt(text):
        if len(text.strip()) == 0:
            return text
        text = text.strip()
        cipher = AES.new(Encrypter.getKey(), AES.MODE_ECB)
        return cipher.decrypt(base64.b64decode(text)).strip()

    @staticmethod
    def getKey():
        with open("key.txt", 'r') as keyfile:
            key = keyfile.read()
        return key

if __name__ == '__main__':
    text = "s  hello world aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print text
    encrypted = Encrypter.encrypt(text)
    print encrypted
    decrypted = Encrypter.decrypt(encrypted)
    print decrypted
