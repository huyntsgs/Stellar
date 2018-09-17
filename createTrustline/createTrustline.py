#coding: utf-8
from stellar_base.builder import Builder
import sys

if len(sys.argv) > 3:
	builder = Builder(secret=sys.argv[1])
	builder.append_trust_op(sys.argv[2], sys.argv[3])
	builder.sign()
	print(builder.submit())
else:
	print(sys.argv[0]+" privkey address_of_issuer asset_code")
