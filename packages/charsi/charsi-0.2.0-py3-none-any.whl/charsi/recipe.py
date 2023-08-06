from __future__ import annotations
from typing import TextIO
from .strings import StringTable, StringLanguage
from .instruction import Instruction, InstructionInvoker
from .utils import filter_irrelevant


class Recipe:
    instructions: list[Instruction]

    def __init__(self):
        self.instructions = []

    def load(self, fp: TextIO):
        self.instructions = [Instruction.parse(line) for line in filter_irrelevant(fp.readlines())]

    def build(self, stbl: StringTable, invoker: InstructionInvoker = InstructionInvoker.default):
        langs = StringLanguage.get_values()

        for inst in self.instructions:
            for s in stbl.findall(inst.query):
                s.update({lang: invoker.invoke(inst, s[lang]) for lang in langs})
