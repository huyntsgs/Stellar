from stellar_base.keypair import Keypair
import sys

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
    
#quantity must be a positive number
if !sys.argv[2].isdigit():
    print("Please provide a correct quantity as second argument")
    sys.exit(0)
