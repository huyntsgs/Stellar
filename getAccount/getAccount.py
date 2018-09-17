#encode: utf-8
from stellar_base.keypair import Keypair
import requests, time, sys


bot_url = "https://horizon-testnet.stellar.org/friendbot"
if len(sys.argv) == 1:
	kp = Keypair.random()
	print(requests.get(bot_url, params={'addr': kp.address().decode()}).text)
	print(kp.address().decode())
	print(kp.seed().decode())
else:
	while True:
		print(requests.get(bot_url, params={'addr': sys.argv[1]}).text)
		time.sleep(5)
		
