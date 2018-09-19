#coding:utf-8 

from stellar_base.keypair import Keypair
from stellar_base.horizon import horizon_testnet
from stellar_base.operation import Payment
from stellar_base.builder import Builder
import sys
import requests
from hashlib import sha256, new

# From https://github.com/darosior/bitcoin-utils/blob/master/utils.py
def hash128(bytes):
    """

    Args:
        bytes (bytes): the data to hash.
	bin (bool): if set to True, returns bytes.

    Returns:
        str/bytes: the hash of the data passed as first parameter.
    """
    rip = new('ripemd')
    rip.update(sha256(bytes).digest())
    return rip.hexdigest()[:28]

class School:
    def __init__(self, key=None):
        if key is None:
            self.kp = Keypair.random()
        else:
            try:
                self.kp = Keypair.from_seed(key)
            except:
                print("You passed a wrong private key as third argument")
                raise

    def award_degree(self, address, student_name, birthdate, year):
        """

        :param student_name: in format prenamesurname with only one prename
        :param year: 4-digits number
        :return: Horizon return of the tx
        """
        memo = hash128((student_name+birthdate+year).encode())
        builder = Builder(secret=self.kp.seed().decode())
        builder.add_text_memo(memo)
        builder.append_payment_op(address, 0.0000001)
        builder.sign()
        return builder.submit()

