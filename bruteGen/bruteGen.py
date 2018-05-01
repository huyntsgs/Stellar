from stellar_base.horizon import horizon_livenet
from stellar_base.keypair import Keypair

horizon = horizon_livenet()

status = 404
while status == 404:
	kp = Keypair.random()
	address = kp.address().decode()
	account = horizon.account(address)
	status = account['status']
	if account['status'] != 404:
		balances = account['balances']
		for b in balances:
			if 'asset_code' in b:
				print(b['balance']+" "+b['asset_code'])
			else:
				print(b['balance']+" "+b['asset_type'])
		print(kp.seed().decode())
	else:
		print('404')
