from enum import IntEnum


# Data Type enumeration
class DT(IntEnum):
    BCD = 1
    ASCII = 2
    BIN = 3


# Length Type enumeration
class LT(IntEnum):
    FIXED = 0
    LVAR = 1
    LLVAR = 2
    LLLVAR = 3


class MsgVersion(IntEnum):
    ISO1987 = 0
    ISO1993 = 1
    ISO2003 = 2
    National = 8
    Private = 9


class MsgClass(IntEnum):
    Authorization = 1
    Financial = 2
    FileAction = 3
    Reversal = 4
    Reconciliation = 5
    Administrative = 6
    FeeCollection = 7
    NetworkManagement = 8
    Reserved = 9


class MsgFunction(IntEnum):
    Request = 0
    RequestResponse = 1
    Advice = 2
    AdviceResponse = 3
    Notification = 4
    NotificationAck = 5
    Instruction = 6
    InstructionAck = 7


class MsgOrigin(IntEnum):
    Acquirer = 0
    AcquirerRepeat = 1
    Issuer = 2
    IssuerRepeat = 3
    Other = 4
    OtherRepeat = 5
