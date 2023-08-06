import argparse
import base64
from cryptography.fernet import Fernet


class Helper:
    def __init__(self, argv: list = None):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--key",
            dest="key",
            required=True,
            help="encrypt key")

        parser.add_argument(
            "--text",
            dest="text",
            required=True,
            help="text to encrypt")
    
        self.__args, self.__opts = parser.parse_known_args(argv)


    def get_configuration_password(self):
        # the key, Fernet key must be 32 url-safe base64-encoded bytes.
        fernet = Fernet(base64.urlsafe_b64encode((f"{self.__args.key}.plusanystringtomakeitmorecomplextoguess")[:32].encode()))

        # the text encrypted
        t = fernet.encrypt(f"{self.__args.text}".encode())

        return t.decode()
