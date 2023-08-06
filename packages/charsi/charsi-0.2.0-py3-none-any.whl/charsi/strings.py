from __future__ import annotations
import json
import re
from functools import reduce
from typing import TypedDict, TextIO, Optional
from enum import Enum


# pylint: disable=invalid-name
class StringLanguage(Enum):
    enUS = 'enUS'
    zhTW = 'zhTW'
    deDE = 'deDE'
    esES = 'esES'
    frFR = 'frFR'
    itIT = 'itIT'
    koKR = 'koKR'
    plPL = 'plPL'
    esMX = 'esMX'
    jaJP = 'jaJP'
    ptBR = 'ptBR'
    ruRU = 'ruRU'
    zhCN = 'zhCN'

    @staticmethod
    def get_values() -> list[str]:
        return [x.value for x in StringLanguage]


class GameString(TypedDict):
    id: str
    Key: str
    enUS: str
    zhTW: str
    deDE: str
    esES: str
    frFR: str
    itIT: str
    koKR: str
    plPL: str
    esMX: str
    jaJP: str
    ptBR: str
    ruRU: str
    zhCN: str


class StringTable:
    _strings: list[GameString]
    _index: dict

    def __init__(self):
        self._strings = []
        self._index = {}

    def load(self, fp: TextIO):
        self._strings = json.loads(fp.read())
        self._index = {self._strings[i]['Key']: i for i in range(0, len(self._strings))}

    def dump(self, fp: TextIO):
        json.dump(self._strings, fp, ensure_ascii=False, indent=4)

    def find(self, key: str) -> Optional[GameString]:
        if key not in self._index:
            return None

        return self._strings[self._index[key]]

    def findall(self, query: str) -> list[dict]:
        if query.find(',') > -1:
            return reduce(lambda v, sl: v + sl, [self.findall(q.strip()) for q in query.split(',')], [])

        m = re.match(r'^\s*([\w\s]+)\s*~\s*([\w\s]+)\s*$', query)

        if not m:
            s = self.find(query)

            if s is None:
                return []

            return [self.find(query)]

        if (m.group(1) not in self._index) or (m.group(2) not in self._index):
            raise IndexError(query)

        start_index = self._index[m.group(1)]
        end_index = self._index[m.group(2)] + 1

        if start_index > end_index:
            raise LookupError(query)

        return self._strings[start_index:end_index]
