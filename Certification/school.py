#coding:utf-8 

from stellar_base.keypair import Keypair
from stellar_base.horizon import horizon_testnet
from stellar_base.operation import Payment
from stellar_base.builder import Builder
import sys
import requests

class School:
    def __init__(name, token_name, key=None):
        self.name = name
        self.tk_name = token_name
        if key is None:
            self.kp = Keypair.random()
        else:
            try:
                self.kp = Keypair.from_seed(key.encode())
            except:
                print("You passed a wrong private key as third argument")
                raise
                
    def award_degree(address, name, date, id):
        memo = name+date+id
        builder = Builder(secret=self.kp.seed().decode())
        builder.add_text_memo(memo.encode('utf-8'))
        builder.append_payment_op(address, 1, self.token_name, kp_issuer.address().decode())
        builder.sign()
        builder.submit()
