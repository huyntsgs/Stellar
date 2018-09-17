#coding:utf-8 

from stellar_base.keypair import Keypair
from stellar_base.horizon import horizon_testnet
from stellar_base.operation import Payment
from stellar_base.builder import Builder
import sys
import requests
from hashlib import sha256

class School:
    def __init__(self, name, key=None):
        self.name = name
        if key is None:
            self.kp = Keypair.random()
        else:
            try:
                self.kp = Keypair.from_seed(key.encode())
            except:
                print("You passed a wrong private key as third argument")
                raise
                
    def award_degree(self, address, token_name, student_name, year):
        """

        :param token_name:
        :param student_name: in format prenamesurname with only one prename
        :param year: 4-digits number
        :return:
        """
        h = sha256((student_name+year).encode())
        memo = h.digest()
        builder = Builder(secret=self.kp.seed().decode())
        builder.add_hash_memo(memo)
        builder.append_payment_op(address, 1, token_name, kp_issuer.address().decode())
        builder.sign()
        builder.submit()
