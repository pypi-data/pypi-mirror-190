from __future__ import annotations
from configparser import ConfigParser


class Config:
    _parser: ConfigParser
    filename: str

    default: Config

    @staticmethod
    def parse_key(key: str) -> list[str]:
        i = key.rfind('.')
        return [key[:i], key[i + 1:]]

    def __init__(self, filename):
        self.filename = filename

        self._parser = ConfigParser()

    def get(self, key: str) -> str:
        fields = Config.parse_key(key)
        return self._parser.get(fields[0], fields[1])

    def set(self, key: str, value: str):
        fields = Config.parse_key(key)

        if not self._parser.has_section(fields[0]):
            self._parser.add_section(fields[0])

        self._parser.set(fields[0], fields[1], value)

    def read(self):
        self._parser.read(self.filename)

    def write(self):
        with open(self.filename, 'w', encoding='utf-8') as fp:
            self._parser.write(fp)
