import base64
import mmh3
import re

from datetime import datetime
from bitarray import bitarray
from typing import Optional, List

COMBINATIONS = [
    ('ssn', 'first_name', 'last_name'),
    ('ssn', 'last_name', 'date_of_birth'),
    ('ssn', 'last_name', 'phone_number'),
    ('ssn', 'last_name', 'email_address'),
    ('ssn', 'date_of_birth', 'phone_number'),
    ('ssn', 'date_of_birth', 'email_address'),
    ('last4ssn', 'last_name', 'date_of_birth'),
    ('last4ssn', 'last_name', 'phone_number'),
    ('last4ssn', 'last_name', 'email_address'),
    ('last_name', 'date_of_birth', 'phone_number'),
    ('last_name', 'date_of_birth', 'email_address'),
    ('date_of_birth', 'phone_number', 'email_address'),
]

BIT_ARRAY_SIZE = 60
HAMMING_WEIGHT = 30
NINE_DIGIT_SSN_REGEX_PATTERN = \
    r'^(?!219099999|078051120)(?!666|000|9\d{2})\d{3}(?!00)\d{2}(?!0{4})\d{4}$'
EMAIL_REGEX = r'\+[^)]*@'
GMAIL_REGEX = r'(?:\.|\+.*)(?=.*?@gmail\.com)'


def _sanitize_ssn(ssn: Optional[str]) -> Optional[str]:
    """ Returns the ssn as a string of 9 digits if it is valid, otherwise None """

    if isinstance(ssn, str):
        # Remove any non-digit character.
        ssn = re.sub(r'\D', '', ssn)

        # If the SSN is 9 digits, and it is a valid SSN, return it.
        if len(ssn) == 9 and bool(re.match(NINE_DIGIT_SSN_REGEX_PATTERN, ssn)):
            return ssn

    return None


class FintechFraudDAOHashing:

    def __init__(self, first_name: Optional[str] = None,
                 last_name: Optional[str] = None,
                 date_of_birth: Optional[datetime] = None,
                 phone_number: Optional[str] = None,
                 email_address: Optional[str] = None,
                 ssn: Optional[str] = None,
                 last4ssn: Optional[str] = None,
                 country: Optional[str] = 'US') -> None:

        # We want to do this because if we receive SSN, we no longer need last4ssn for two reasons
        # 1. If SSN is somehow invalid then last4ssn should also be invalid
        # 2. If SSN is valid then last4ssn is redundant. We can use SSN to generate last4ssn
        if ssn is not None:
            last4ssn = None

        self.first_name = first_name and first_name.lower().strip()
        self.last_name = last_name and last_name.lower().strip()
        self.date_of_birth = date_of_birth and date_of_birth.strftime('%Y-%m-%d')
        self.ssn = _sanitize_ssn(ssn)
        self.last4ssn = last4ssn

        self.phone_number = phone_number and re.sub(r'\D', '', phone_number)
        if self.phone_number:
            # If phone number is 10 digits and a US number, add the 1 keeping it in
            # international format without the +. This can be built upon later if
            # entities from other countries are added.
            if len(self.phone_number) == 10 and country == 'US':
                self.phone_number = '1' + self.phone_number

        self.email_address = email_address and email_address.lower().strip()
        if self.email_address:
            self.email_address = re.sub(GMAIL_REGEX, '', self.email_address)
            self.email_address = re.sub(EMAIL_REGEX, '@', self.email_address)

        if self.last4ssn:
            # Remove any non-digit character.
            self.last4ssn = re.sub(r'\D', '', self.last4ssn)

            if len(self.last4ssn) != 4 or self.last4ssn == '0000':
                self.last4ssn = None

        # If we have a full SSN, then use this for the last4
        if self.ssn:
            self.last4ssn = self.ssn[-4:]

    @staticmethod
    def _generate_hash(value: str) -> str:
        bf = bitarray(BIT_ARRAY_SIZE)
        bf.setall(0)
        for seed in range(HAMMING_WEIGHT):
            result = mmh3.hash(value, seed) % BIT_ARRAY_SIZE
            bf[result] = 1
        return base64.b64encode(bf.tobytes()).decode('utf8')

    def generate_hashes(self) -> List[str]:
        result = []
        for c in COMBINATIONS:
            if all(self.__getattribute__(v) for v in c):
                result.append(self._generate_hash(''.join([self.__getattribute__(v) for v in c])))
        return result
