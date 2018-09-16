from stellar_base.keypair import Keypair
from stellar_base.horizon import horizon_testnet
from stellar_base.operation import Payment
from stellar_base.builder import Builder
import sys
import requests

key = "SAUGXMIK4FFET7KGYPGBVUIZOGHPCSZGMW73EGKHK4QKZGLZIANLV4XB"
kp = Keypair.from_seed(key)


