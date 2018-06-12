from stellar_base.keypair import Keypair
from stellar_base.horizon import horizon_testnet
from stellar_base.operation import Payment
from stellar_base.builder import Builder
import sys
import requests

if  len(sys.argv) < 3:
  print("usage : "+sys.argv[0]+" <tokenName> <quantity>")
  sys.exit(0)

# Maximum length for asset name is 12 character
if len(sys.argv[1]) > 12: 
  print("The name of your asset must have between 1 and 12 caracters")
  sys.exit(0)
 
for car in sys.argv[1]:
  if car.upper() not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and car not in "0123456789":
    print("The name of your asset must be composed of (max 12) Alphanumerics caracters only")
    sys.exit(0)
    
# Quantity must be a positive number
if not sys.argv[2].isdigit():
    print("Please provide a correct quantity as second argument")
    sys.exit(0)

# We need to accounts, one for the issuer, the other for the distributer
kp_issuer = Keypair.random()
kp_distrib = Keypair.random()

# Then we need to fund them with testnet's Lumens
bot_url = "https://friendbot.stellar.org"
requests.get(bot_url, params={'addr': kp_issuer.address().decode()})
requests.get(bot_url, params={'addr': kp_distrib.address().decode()})

# And we create a trust line between the distributor and the issuer
# In order to do that, we build a transaction. I'll use the Builder class, for simplicity.
builder = Builder(secret=kp_distrib.seed().decode())
builder.append_trust_op(kp_issuer.address().decode(), sys.argv[1], sys.argv[2], kp_distrib.address().decode())
builder.sign()
bulder.submit()

# We finally send these tokens from issuer to distributer
builder = Builder(secret=kp_issuer.seed().decode())
builder.add_payment_op(kp_distrib.address().decode(), sys.argv[2], sys.argv[1], kp_issuer.address().decode())
builder.sign()
bulder.submit()

# To make sure there will not be anymore creation of this token, we make it unavailable by setting the permission of the master key to 0, and the minimum permission for any operation to 1
builder = Builder(secret=kp_distrib.seed().decode())
builder.add_set_options_op(master_weight=0, low_treshold=1, med_treshold=1, high_treshold=1)
builder.sign()
bulder.submit()

print("Succesfully created "+sys.argv[2]+" "+sys.argv[1]+" tokens. You can access them via the following account :")
print("Address : "+kp_distrib.address().decode())
print("Key : "+kp_distrib.seed().decode())
