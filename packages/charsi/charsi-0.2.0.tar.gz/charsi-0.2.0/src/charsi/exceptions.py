class _InstructionError(Exception):
    ...


class InstructionFormatError(_InstructionError):
    ...


class _InstructionInvokeError(Exception):
    ...


class InstructionConflictError(_InstructionInvokeError):
    ...


class InstructionUndefinedError(_InstructionInvokeError):
    ...
