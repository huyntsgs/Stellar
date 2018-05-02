import tkinter as tk
from tkinter import messagebox
import sys, os
from stellar_base.horizon import horizon_livenet
from stellar_base.keypair import Keypair

class Wallet:
	def __init__(self):
		#Usefull vars
		self.srcPath = os.path.dirname(os.path.realpath(__file__))
		self.imageFolder = self.srcPath + "/img/"
		#Initializing the window
		self.window = tk.Tk()
		self.window.title("Wallet")
		iconImg = tk.PhotoImage(file=self.imageFolder+"stellarIcon.gif")
		self.window.tk.call('wm', 'iconphoto', self.window._w, iconImg)
		#Infos about the user
		self.connected = False
		self.key = ""
		self.address = ""
		self.infos = {}
		self.nbOfAssets = 0
		#Stellar
		self.horizon = horizon_livenet()


	def connection(self):
		"""
		The user isn't connected yet so we provide him fields to log index, acting like a login page
		"""
		self.keyLabel = tk.Label(self.window, text="Your private key : ", justify=tk.RIGHT, bd=20)
		self.keyInput = tk.Entry(self.window, bd=5, width=56, exportselection=0)
		self.submit = tk.Button(self.window, text="Unlock wallet",  command=self.unlock, bd=5)

		self.keyLabel.grid(row=1, column=0, columnspan=2)
		self.keyInput.grid(row=1, column=2, columnspan=8)
		self.submit.grid(row=5, column=4, columnspan=2)


	def display(self):
		"""
		The user is connected, so we load and display his infos
		"""
		#Erasing the "login page"
		self.keyInput.destroy()
		self.keyLabel.destroy()
		self.submit.destroy()
		#Loading infos
		self.infos = self.horizon.account(self.address)
		if not "status" in self.infos:#meaning request failed with a 404
			#Displaying infos
			#The address
			self.addressLabel = tk.Label(self.window, text="Your address : "+self.address, padx=10, pady=10, bd=10)
			self.addressLabel.grid(row=1, column=0, columnspan=10)#row=0 is for the banner
			#The balances, that we position in a frame and loop into all assets the account has or has trustlined
			self.balancesFrame = tk.LabelFrame(self.window, text="Balances")
			self.balancesFrame.grid(row=2, column=0, columnspan=3)
			for i in self.infos['balances']:
				self.nbOfAssets += 1
				if i["asset_type"] == "native":
					balanceLabel = tk.Label(self.balancesFrame, text="XLM : "+i['balance'], padx=5, pady=5, bd=15)
					balanceLabel.pack()			
				else:
					balanceLabel = tk.Label(self.balancesFrame, text=i['asset_code']+" : "+i['balance'], padx=5, pady=5, bd=15)
					balanceLabel.pack()
			#Send
			self.sendFrame = tk.LabelFrame(self.window, text="Send money")
			self.sendFrame.grid(row=2, column=3, columnspan=7)
			self.receiverLabel = tk.Label(self.sendFrame, text="The receiver address")
			self.receiverLabel.grid(row=0, column=1, columnspan=5)
			self.receiverInput = tk.Entry(self.sendFrame, bd=3, width=56, exportselection=0)
			self.receiverInput.grid(row=1, column=0, columnspan=11)
			self.assetLabel = tk.Label(self.sendFrame, text="Asset to send : ", pady=10)
			self.assetLabel.grid(row=2, column=0)
			#We make a list of all assets in order to pass them to the drop-down
			assets = ["XLM"]
			for b in self.infos["balances"]:
				if b["asset_type"] != "native":
					assets.append(b["asset_code"])
			self.assetChosen = tk.StringVar(self.sendFrame)
			self.assetChosen.set(assets[0]) #Default value
			self.assetList = tk.OptionMenu(self.sendFrame, self.assetChosen, *assets)
			self.assetList.grid(row=2, column=1, columnspan=3)
			self.quantityLabel = tk.Label(self.sendFrame, text="Quantity : ", pady=10, padx=5)
			self.quantityLabel.grid(row=2, column=4, columnspan=3)
			self.quantitySpin = tk.Spinbox(self.sendFrame, from_=0, to=1000000000000000, width=10, wrap="true")
			self.quantitySpin.grid(row=2, column=7, columnspan=3)
			#Simulating an offset
			offset = tk.Label(self.sendFrame, text="", width=10, height=1)
			offset.grid(row=3, column=0, columnspan=10)
			self.sendSubmit = tk.Button(self.sendFrame, text="Send", bd=2, width=10, command=self.send)
			self.sendSubmit.grid(row=4, column=2, columnspan=2)

		else:
			self.connected = False
			self.address = ""
			self.connection()
			messagebox.showerror("Account not valid", "The key you provided refers to an account that hasn't been activated yet, please try again after having activated it. More infos at Stellar.org")
	
		
		
	def run(self):
		#The banner
		bannerImg = tk.PhotoImage(file=self.imageFolder + "banner.png")
		self.banner = tk.Label(self.window, image=bannerImg, bd=20)
		
		if not self.connected:
			self.connection()
		else:
			self.display()
			
		self.banner.grid(row=0, column=0, columnspan=10)
		self.window.mainloop()
			
	def send(self):
		"""
		The method to make a payment
		"""
		address = self.receiverInput.get()
		asset = self.assetChosen.get()
		quantity = self.quantitySpin.get()
		valid = True
		#Verify address
		addressInfos = self.horizon.account(address)
		if "status" in addressInfos:
			messagebox.showerror("Invalid address", "The address you provided doesn't refer to any account.")
			valid = False
		#Verifying the destination accepts this asset
		if valid:
			if asset == "XLM":
				valid = True
			else:
				for i in addressInfos["balances"]:
					if i["asset_code"] == asset:
						valid = True
						break
					else:
						valid = False
		#Verifying the quantity
		if valid:
			#Getting fresh infos
			freshInfos = self.horizon.account(self.address)
			for i in freshInfos["balances"]:
				if i["asset_code"] == asset:
					if i["balance"]-quantity > self.nbOfAssets:
						valid = True
					else:
						valid = False
					break
			

	def unlock(self):
		seed = self.keyInput.get()
		try:
			kp = Keypair.from_seed(seed)
			self.connected = True
			self.key = kp.seed().decode()
			self.address = kp.address().decode()
		except:
			messagebox.showerror("Wrong key", "Cannot unlock the account, please check the key you entered") 			
		self.run()
				
		
if __name__=='__main__':
	wallet = Wallet()
	wallet.run()
