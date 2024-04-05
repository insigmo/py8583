from py8583.errors import SpecError
from py8583.enums import DT, LT

Descriptions = {}
ContentTypes = {}


class IsoSpec:
    _ValidContentTypes = ('a', 'n', 's', 'an', 'as', 'ns', 'ans', 'b', 'z')

    Descriptions = {}
    ContentTypes = {}
    DataTypes = {}

    def __init__(self):
        self.set_descriptions()
        self.set_content_types()
        self.set_data_types()

    def set_descriptions(self):
        pass

    def set_content_types(self):
        pass

    def set_data_types(self):
        pass

    def description(self, field, description=None):
        if description is None:
            return self.Descriptions[field]
        else:
            self.Descriptions[field] = description

    def data_type(self, field, data_type=None):
        if data_type is None:
            return self.DataTypes[field]['Data']
        else:
            if data_type not in DT:
                raise SpecError("Cannot set data type '{0}' for F{1}: Invalid data type".format(data_type, field))
            if field not in self.DataTypes.keys():
                self.DataTypes[field] = {}
            self.DataTypes[field]['Data'] = data_type

    def content_type(self, field, content_type=None):
        if content_type is not None:
            if content_type not in self._ValidContentTypes:
                raise SpecError(
                    "Cannot set Content type '{0}' for F{1}: Invalid content type".format(content_type, field))
            self.ContentTypes[field]['content_type'] = content_type
        else:
            return self.ContentTypes[field]['content_type']

    def max_length(self, field, max_length=None):
        if max_length is None:
            return self.ContentTypes[field]['MaxLen']
        else:
            self.ContentTypes[field]['MaxLen'] = max_length

    def length_type(self, field, length_type=None):
        if length_type is None:
            return self.ContentTypes[field]['len_type']
        else:
            if length_type not in LT:
                raise SpecError("Cannot set Length type '{0}' for F{1}: Invalid length type".format(length_type, field))
            self.ContentTypes[field]['len_type'] = length_type

    def length_data_type(self, field, length_data_type=None):
        if length_data_type is None:
            return self.DataTypes[field]['Length']
        else:
            if length_data_type not in DT:
                raise SpecError("Cannot set data type '{0}' for F{1}: Invalid data type".format(length_data_type, field)
                                )
            if field not in self.DataTypes.keys():
                self.DataTypes[field] = {}
            self.DataTypes[field]['Length'] = length_data_type


class IsoSpec1987(IsoSpec):
    def set_descriptions(self):
        self.Descriptions = Descriptions['1987']

    def set_content_types(self):
        self.ContentTypes = ContentTypes['1987']


class IsoSpec1987ASCII(IsoSpec1987):
    def set_data_types(self):
        self.data_type('mti', DT.ASCII)
        self.data_type(1, DT.ASCII)  # bitmap

        for field in self.ContentTypes.keys():
            self.data_type(field, DT.ASCII)

            if self.length_type(field) != LT.FIXED:
                self.length_data_type(field, DT.ASCII)


class BICISO(IsoSpec1987ASCII):
    def set_content_types(self):
        super(BICISO, self).set_content_types()

        # Variations between official ISO and BIC ISO
        self.ContentTypes[41]['MaxLen'] = 16
        self.ContentTypes[44]['MaxLen'] = 27


class IsoSpec1987BCD(IsoSpec1987):
    def set_content_types(self):
        super().set_content_types()
        # Most popular BCD implementations use the reserved/private fields
        # as binary, so we have to set them as such in contrast to the ISO spec
        for field in self.ContentTypes.keys():
            if self.max_length(field) == 999:
                self.content_type(field, 'b')

    def set_data_types(self):
        self.data_type('mti', DT.BCD)
        self.data_type(1, DT.BIN)  # bitmap

        for field in self.ContentTypes.keys():

            content_type = self.content_type(field)

            if 'a' in content_type or 's' in content_type:
                self.data_type(field, DT.ASCII)
            elif content_type == 'b':
                self.data_type(field, DT.BIN)
            else:
                self.data_type(field, DT.BCD)

            if self.length_type(field) != LT.FIXED:
                self.length_data_type(field, DT.BCD)


class IsoSpec1993(IsoSpec):
    def set_descriptions(self):
        self.Descriptions = Descriptions['1993']

    def set_content_types(self):
        self.ContentTypes = ContentTypes['1993']


class IsoSpec1993ASCII(IsoSpec1993):
    def set_data_types(self):
        self.data_type('mti', DT.ASCII)
        self.data_type(1, DT.ASCII)  # bitmap

        for field in self.ContentTypes.keys():
            self.data_type(field, DT.ASCII)
            if self.length_type(field) != LT.FIXED:
                self.length_data_type(field, DT.ASCII)


Descriptions['1987'] = {
    1: 'bitmap',
    2: 'primary account number (PAN)',
    3: 'Processing code',
    4: 'Amount, transaction',
    5: 'Amount, settlement',
    6: 'Amount, cardholder billing',
    7: 'Transmission date & time',
    8: 'Amount, cardholder billing fee',
    9: 'Conversion rate, settlement',
    10: 'Conversion rate, cardholder billing',
    11: 'System trace audit number',
    12: 'Time, local transaction (hhmmss)',
    13: 'Date, local transaction (MMDD)',
    14: 'Date, expiration',
    15: 'Date, settlement',
    16: 'Date, conversion',
    17: 'Date, capture',
    18: 'Merchant type',
    19: 'Acquiring institution country code',
    20: 'PAN extended, country code',
    21: 'Forwarding institution. country code',
    22: 'Point of service entry mode',
    23: 'Application PAN sequence number',
    24: 'Network International identifier (NII)',
    25: 'Point of service condition code',
    26: 'Point of service capture code',
    27: 'Authorizing identification response length',
    28: 'Amount, transaction fee',
    29: 'Amount, settlement fee',
    30: 'Amount, transaction processing fee',
    31: 'Amount, settlement processing fee',
    32: 'Acquiring institution identification code',
    33: 'Forwarding institution identification code',
    34: 'primary account number, extended',
    35: 'Track 2 data',
    36: 'Track 3 data',
    37: 'Retrieval reference number',
    38: 'Authorization identification response',
    39: 'Response code',
    40: 'Service restriction code',
    41: 'Card acceptor terminal identification',
    42: 'Card acceptor identification code',
    43: 'Card acceptor name/location',
    44: 'Additional response data',
    45: 'Track 1 data',
    46: 'Additional data - ISO',
    47: 'Additional data - national',
    48: 'Additional data - private',
    49: 'Currency code, transaction',
    50: 'Currency code, settlement',
    51: 'Currency code, cardholder billing',
    52: 'Personal identification number data',
    53: 'Security related control information',
    54: 'Additional amounts',
    55: 'Reserved ISO',
    56: 'Reserved ISO',
    57: 'Reserved national',
    58: 'Reserved national',
    59: 'Reserved national',
    60: 'Reserved national',
    61: 'Reserved private',
    62: 'Reserved private',
    63: 'Reserved private',
    64: 'Message authentication code (MAC)',
    65: 'bitmap, extended',
    66: 'Settlement code',
    67: 'Extended payment code',
    68: 'Receiving institution country code',
    69: 'Settlement institution country code',
    70: 'Network management information code',
    71: 'Message number',
    72: 'Message number, last',
    73: 'Date, action (YYMMDD)',
    74: 'Credits, number',
    75: 'Credits, reversal number',
    76: 'Debits, number',
    77: 'Debits, reversal number',
    78: 'Transfer number',
    79: 'Transfer, reversal number',
    80: 'Inquiries number',
    81: 'Authorizations, number',
    82: 'Credits, processing fee amount',
    83: 'Credits, transaction fee amount',
    84: 'Debits, processing fee amount',
    85: 'Debits, transaction fee amount',
    86: 'Credits, amount',
    87: 'Credits, reversal amount',
    88: 'Debits, amount',
    89: 'Debits, reversal amount',
    90: 'Original data elements',
    91: 'File update code',
    92: 'File security code',
    93: 'Response indicator',
    94: 'Service indicator',
    95: 'Replacement amounts',
    96: 'Message security code',
    97: 'Amount, net settlement',
    98: 'Payee',
    99: 'Settlement institution identification code',
    100: 'Receiving institution identification code',
    101: 'File name',
    102: 'Account identification 1',
    103: 'Account identification 2',
    104: 'Transaction description',
    105: 'Reserved for ISO use',
    106: 'Reserved for ISO use',
    107: 'Reserved for ISO use',
    108: 'Reserved for ISO use',
    109: 'Reserved for ISO use',
    110: 'Reserved for ISO use',
    111: 'Reserved for ISO use',
    112: 'Reserved for national use',
    113: 'Reserved for national use',
    114: 'Reserved for national use',
    115: 'Reserved for national use',
    116: 'Reserved for national use',
    117: 'Reserved for national use',
    118: 'Reserved for national use',
    119: 'Reserved for national use',
    120: 'Reserved for private use',
    121: 'Reserved for private use',
    122: 'Reserved for private use',
    123: 'Reserved for private use',
    124: 'Reserved for private use',
    125: 'Reserved for private use',
    126: 'Reserved for private use',
    127: 'Reserved for private use',
    128: 'Message authentication code'
}

ContentTypes['1987'] = {
    1: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    2: {'content_type': 'n', 'MaxLen': 19, 'len_type': LT.LLVAR},
    3: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    4: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    5: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    6: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    7: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    8: {'content_type': 'n', 'MaxLen': 8, 'len_type': LT.FIXED},
    9: {'content_type': 'n', 'MaxLen': 8, 'len_type': LT.FIXED},
    10: {'content_type': 'n', 'MaxLen': 8, 'len_type': LT.FIXED},
    11: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    12: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    13: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    14: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    15: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    16: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    17: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    18: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    19: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    20: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    21: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    22: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    23: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    24: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    25: {'content_type': 'n', 'MaxLen': 2, 'len_type': LT.FIXED},
    26: {'content_type': 'n', 'MaxLen': 2, 'len_type': LT.FIXED},
    27: {'content_type': 'n', 'MaxLen': 1, 'len_type': LT.FIXED},
    28: {'content_type': 'an', 'MaxLen': 9, 'len_type': LT.FIXED},
    29: {'content_type': 'an', 'MaxLen': 9, 'len_type': LT.FIXED},
    30: {'content_type': 'an', 'MaxLen': 9, 'len_type': LT.FIXED},
    31: {'content_type': 'an', 'MaxLen': 9, 'len_type': LT.FIXED},
    32: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    33: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    34: {'content_type': 'ns', 'MaxLen': 28, 'len_type': LT.LLVAR},
    35: {'content_type': 'z', 'MaxLen': 37, 'len_type': LT.LLVAR},
    36: {'content_type': 'n', 'MaxLen': 104, 'len_type': LT.LLLVAR},
    37: {'content_type': 'an', 'MaxLen': 12, 'len_type': LT.FIXED},
    38: {'content_type': 'an', 'MaxLen': 6, 'len_type': LT.FIXED},
    39: {'content_type': 'an', 'MaxLen': 2, 'len_type': LT.FIXED},
    40: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    41: {'content_type': 'ans', 'MaxLen': 8, 'len_type': LT.FIXED},
    42: {'content_type': 'ans', 'MaxLen': 15, 'len_type': LT.FIXED},
    43: {'content_type': 'ans', 'MaxLen': 40, 'len_type': LT.FIXED},
    44: {'content_type': 'an', 'MaxLen': 25, 'len_type': LT.LLVAR},
    45: {'content_type': 'an', 'MaxLen': 76, 'len_type': LT.LLVAR},
    46: {'content_type': 'an', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    47: {'content_type': 'an', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    48: {'content_type': 'an', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    49: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    50: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    51: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    52: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    53: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    54: {'content_type': 'an', 'MaxLen': 120, 'len_type': LT.LLLVAR},
    55: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    56: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    57: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    58: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    59: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    60: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    61: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    62: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    63: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    64: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    65: {'content_type': 'b', 'MaxLen': 1, 'len_type': LT.FIXED},
    66: {'content_type': 'n', 'MaxLen': 1, 'len_type': LT.FIXED},
    67: {'content_type': 'n', 'MaxLen': 2, 'len_type': LT.FIXED},
    68: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    69: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    70: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    71: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    72: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    73: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    74: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    75: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    76: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    77: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    78: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    79: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    80: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    81: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    82: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    83: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    84: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    85: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    86: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    87: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    88: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    89: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    90: {'content_type': 'n', 'MaxLen': 42, 'len_type': LT.FIXED},
    91: {'content_type': 'an', 'MaxLen': 1, 'len_type': LT.FIXED},
    92: {'content_type': 'an', 'MaxLen': 2, 'len_type': LT.FIXED},
    93: {'content_type': 'an', 'MaxLen': 5, 'len_type': LT.FIXED},
    94: {'content_type': 'an', 'MaxLen': 7, 'len_type': LT.FIXED},
    95: {'content_type': 'an', 'MaxLen': 42, 'len_type': LT.FIXED},
    96: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    97: {'content_type': 'an', 'MaxLen': 17, 'len_type': LT.FIXED},
    98: {'content_type': 'ans', 'MaxLen': 25, 'len_type': LT.FIXED},
    99: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    100: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    101: {'content_type': 'ans', 'MaxLen': 17, 'len_type': LT.LLVAR},
    102: {'content_type': 'ans', 'MaxLen': 28, 'len_type': LT.LLVAR},
    103: {'content_type': 'ans', 'MaxLen': 28, 'len_type': LT.LLVAR},
    104: {'content_type': 'ans', 'MaxLen': 100, 'len_type': LT.LLLVAR},
    105: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    106: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    107: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    108: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    109: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    110: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    111: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    112: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    113: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    114: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    115: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    116: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    117: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    118: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    119: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    120: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    121: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    122: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    123: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    124: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    125: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    126: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    127: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    128: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED}
}

Descriptions['1993'] = {
    1: 'bitmap',
    2: 'primary account number (PAN)',
    3: 'Processing code',
    4: 'Amount, transaction',
    5: 'Amount, reconciliation',
    6: 'Amount, cardholder billing',
    7: 'Date and time, transmission',
    8: 'Amount, cardholder billing fee',
    9: 'Conversion rate, reconciliation',
    10: 'Conversion rate, cardholder billing',
    11: 'System trace audit number',
    12: 'Date and time, local transaction',
    13: 'Date, effective',
    14: 'Date, expiration',
    15: 'Date, settlement',
    16: 'Date, conversion',
    17: 'Date, capture',
    18: 'Merchant type',
    19: 'Country code, acquiring institution',
    20: 'Country code, primary account numbe',
    21: 'Country code, forwarding institution',
    22: 'Point of service data code',
    23: 'Card sequence number',
    24: 'function code',
    25: 'Message reason code ',
    26: 'Card acceptor business code ',
    27: 'Approval code length ',
    28: 'Date, reconciliation ',
    29: 'Reconciliation indicator',
    30: 'Amounts, original',
    31: 'Acquirer reference data',
    32: 'Acquiring institution identification code',
    33: 'Forwarding institution identification code',
    34: 'primary account number, extended',
    35: 'Track 2 data',
    36: 'Track 3 data',
    37: 'Retrieval reference number',
    38: 'Approval code',
    39: 'Action code',
    40: 'Service code',
    41: 'Card acceptor terminal identification',
    42: 'Card acceptor identification code',
    43: 'Card acceptor name/location',
    44: 'Additional response data',
    45: 'Track 1 data',
    46: 'Amounts, fees',
    47: 'Additional data - national',
    48: 'Additional data - private',
    49: 'Currency code, transaction',
    50: 'Currency code, reconciliation',
    51: 'Currency code, cardholder billing',
    52: 'Personal identification number data',
    53: 'Security related control information',
    54: 'Amounts, additional',
    55: 'Integrated circuit card system related data',
    56: 'Original data elements',
    57: 'Authorization life cycle code',
    58: 'Authorizing agent institution identification code',
    59: 'Transport data',
    60: 'Reserved for national use',
    61: 'Reserved for national use',
    62: 'Reserved for private use',
    63: 'Reserved for private use',
    64: 'Message authentication code field',
    65: 'Reserved for IS0 use',
    66: 'Amounts, original fees',
    67: 'Extended payment data',
    68: 'Country code, receiving institution ',
    69: 'Country code, settlement institution',
    70: 'Country code, authorizing agent institution',
    71: 'Message number',
    72: 'Data record ',
    73: 'Date, action',
    74: 'Credits, number',
    75: 'Credits, reversal number',
    76: 'Debits, number',
    77: 'Debits, reversal number',
    78: 'Transfer, number',
    79: 'Transfer, reversal number',
    80: 'Inquiries, number',
    81: 'Authorizations, number',
    82: 'Inquiries, reversal number',
    83: 'Payments, number',
    84: 'Payments, reversal number',
    85: 'Fee collections, number ',
    86: 'Credits, amount',
    87: 'Credits, reversal amount',
    88: 'Debits, amount',
    89: 'Debits, reversal amount',
    90: 'Authorizations, reversal number',
    91: 'Country code, transaction destination institution ',
    92: 'Country code, transaction originator institution ',
    93: 'Transaction destination institution identification code',
    94: 'Transaction originator institution identification code ',
    95: 'Card issuer reference data',
    96: 'Key management data',
    97: 'Amount, net reconciliation',
    98: 'Payee',
    99: 'Settlement institution identitifaction code',
    100: 'Receiving institution identification code',
    101: 'File name',
    102: 'Account identification 1',
    103: 'Account identification 2',
    104: 'Transaction description',
    105: 'Credits, chargeback amount',
    106: 'Debits, chargeback amount',
    107: 'Credits, chargeback number',
    108: 'Debits, chargeback number',
    109: 'Credits, fee amounts',
    110: 'Debits, fee amounts',
    111: 'Reserved for ISO use',
    112: 'Reserved for ISO use',
    113: 'Reserved for ISO use',
    114: 'Reserved for ISO use',
    115: 'Reserved for ISO use',
    116: 'Reserved for national use',
    117: 'Reserved for national use',
    118: 'Reserved for national use',
    119: 'Reserved for national use',
    120: 'Reserved for national use',
    121: 'Reserved for national use',
    122: 'Reserved for national us',
    123: 'Reserved for private use',
    124: 'Reserved for private use',
    125: 'Reserved for private use',
    126: 'Reserved for private use',
    127: 'Reserved for private use',
    128: 'Message authentication code field',
}

ContentTypes['1993'] = {
    1: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    2: {'content_type': 'n', 'MaxLen': 19, 'len_type': LT.LLVAR},
    3: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    4: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    5: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    6: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    7: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    8: {'content_type': 'n', 'MaxLen': 8, 'len_type': LT.FIXED},
    9: {'content_type': 'n', 'MaxLen': 8, 'len_type': LT.FIXED},
    10: {'content_type': 'n', 'MaxLen': 8, 'len_type': LT.FIXED},
    11: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    12: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    13: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    14: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    15: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    16: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    17: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    18: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    19: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    20: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    21: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    22: {'content_type': 'an', 'MaxLen': 12, 'len_type': LT.FIXED},
    23: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    24: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    25: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    26: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    27: {'content_type': 'n', 'MaxLen': 1, 'len_type': LT.FIXED},
    28: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    29: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    30: {'content_type': 'n', 'MaxLen': 24, 'len_type': LT.FIXED},
    31: {'content_type': 'an', 'MaxLen': 31, 'len_type': LT.LLVAR},
    32: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    33: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    34: {'content_type': 'ns', 'MaxLen': 28, 'len_type': LT.LLVAR},
    35: {'content_type': 'z', 'MaxLen': 37, 'len_type': LT.LLVAR},
    36: {'content_type': 'z', 'MaxLen': 104, 'len_type': LT.LLLVAR},
    37: {'content_type': 'an', 'MaxLen': 12, 'len_type': LT.FIXED},
    38: {'content_type': 'an', 'MaxLen': 6, 'len_type': LT.FIXED},
    39: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    40: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    41: {'content_type': 'ans', 'MaxLen': 8, 'len_type': LT.FIXED},
    42: {'content_type': 'ans', 'MaxLen': 15, 'len_type': LT.FIXED},
    43: {'content_type': 'ans', 'MaxLen': 99, 'len_type': LT.LLVAR},
    44: {'content_type': 'ans', 'MaxLen': 99, 'len_type': LT.LLVAR},
    45: {'content_type': 'ans', 'MaxLen': 76, 'len_type': LT.LLVAR},
    46: {'content_type': 'ans', 'MaxLen': 204, 'len_type': LT.LLLVAR},
    47: {'content_type': 'an', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    48: {'content_type': 'an', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    49: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    50: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    51: {'content_type': 'an', 'MaxLen': 3, 'len_type': LT.FIXED},
    52: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    53: {'content_type': 'b', 'MaxLen': 48, 'len_type': LT.FIXED},
    54: {'content_type': 'ans', 'MaxLen': 120, 'len_type': LT.LLLVAR},
    55: {'content_type': 'b', 'MaxLen': 255, 'len_type': LT.LLLVAR},
    56: {'content_type': 'n', 'MaxLen': 35, 'len_type': LT.LLLVAR},
    57: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.LLLVAR},
    58: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.FIXED},
    59: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    60: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    61: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    62: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    63: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    64: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    65: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    66: {'content_type': 'n', 'MaxLen': 1, 'len_type': LT.FIXED},
    67: {'content_type': 'n', 'MaxLen': 2, 'len_type': LT.FIXED},
    68: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    69: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    70: {'content_type': 'n', 'MaxLen': 3, 'len_type': LT.FIXED},
    71: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    72: {'content_type': 'n', 'MaxLen': 4, 'len_type': LT.FIXED},
    73: {'content_type': 'n', 'MaxLen': 6, 'len_type': LT.FIXED},
    74: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    75: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    76: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    77: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    78: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    79: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    80: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    81: {'content_type': 'n', 'MaxLen': 10, 'len_type': LT.FIXED},
    82: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    83: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    84: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    85: {'content_type': 'n', 'MaxLen': 12, 'len_type': LT.FIXED},
    86: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    87: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    88: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    89: {'content_type': 'n', 'MaxLen': 16, 'len_type': LT.FIXED},
    90: {'content_type': 'n', 'MaxLen': 42, 'len_type': LT.FIXED},
    91: {'content_type': 'an', 'MaxLen': 1, 'len_type': LT.FIXED},
    92: {'content_type': 'an', 'MaxLen': 2, 'len_type': LT.FIXED},
    93: {'content_type': 'an', 'MaxLen': 5, 'len_type': LT.FIXED},
    94: {'content_type': 'an', 'MaxLen': 7, 'len_type': LT.FIXED},
    95: {'content_type': 'an', 'MaxLen': 42, 'len_type': LT.FIXED},
    96: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED},
    97: {'content_type': 'an', 'MaxLen': 17, 'len_type': LT.FIXED},
    98: {'content_type': 'ans', 'MaxLen': 25, 'len_type': LT.FIXED},
    99: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    100: {'content_type': 'n', 'MaxLen': 11, 'len_type': LT.LLVAR},
    101: {'content_type': 'ans', 'MaxLen': 17, 'len_type': LT.LLVAR},
    102: {'content_type': 'ans', 'MaxLen': 28, 'len_type': LT.LLVAR},
    103: {'content_type': 'ans', 'MaxLen': 28, 'len_type': LT.LLVAR},
    104: {'content_type': 'ans', 'MaxLen': 100, 'len_type': LT.LLLVAR},
    105: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    106: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    107: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    108: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    109: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    110: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    111: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    112: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    113: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    114: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    115: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    116: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    117: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    118: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    119: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    120: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    121: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    122: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    123: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    124: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    125: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    126: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    127: {'content_type': 'ans', 'MaxLen': 999, 'len_type': LT.LLLVAR},
    128: {'content_type': 'b', 'MaxLen': 8, 'len_type': LT.FIXED}
}
