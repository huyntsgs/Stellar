from stellar_base.keypair import Keypair
import sys

if  len(sys.argv) < 2:
	print("usage : "+sys.argv[0]+" <pattern> (<end>)")
#If the pattern has to be at the end
elif len(sys.argv) == 3:
	pattern = sys.argv[1].upper()
	address = ""
	while pattern != address[-len(pattern):]:
		kp = Keypair.random()
		address = kp.address().decode()
		if pattern == address[-len(pattern):]:
			print("Your address : " + address)
			print("Your key : " + kp.seed().decode())
		else:
			print('.', end='', flush=True)
else:
	pattern = sys.argv[1].upper()
	address = ""
	while pattern not in address:
		kp = Keypair.random()
		address = kp.address().decode()
		if pattern in address:
			print("Your address : " + address)
			print("Your key : " + kp.seed().decode())
		else:
			print('.', end='', flush=True)
