#coding:utf-8 

from stellar_base.keypair import Keypair
from stellar_base.builder import Builder
from hashlib import sha256, new

# From https://github.com/darosior/bitcoin-utils/blob/master/utils.py
def hash128(bytes):
    """Returns the first 28 bytes of the hash (ripmd of sha256) of the data

    :param bytes: The data to be hashed (likely the student's informations)
    :return: The first 28 bytes of the hash (ripmd of sha256) of the data
    """
    rip = new('ripemd')
    rip.update(sha256(bytes).digest())
    return rip.hexdigest()[:28]

class School:
    """
    Represents the school on the website
    """
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
        """Sends a transaction with a hash of the student's informations as text memo.

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

