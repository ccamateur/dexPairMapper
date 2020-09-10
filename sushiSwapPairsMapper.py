from web3 import Web3
import json
import sys
from itertools import combinations

#setting up environment: immporting credentials from file
fo = open("credentials.txt", "r")
infura_url = fo.readline().rstrip('\n')
public_key = fo.readline().rstrip('\n')
private_key = fo.readline().rstrip('\n')
tokenNames = []
tokenPairs = []
output_list = []
exchangeMap = {}


#Setting up a web3 object
w3 = Web3(Web3.HTTPProvider(infura_url))

#Check that the connection has been made
if (w3.isConnected() == False):
    print("No web3 connection!")
    sys.exit(0)

#Basic user dashboard with connection details, block number and current Ether balance
print("\n************************************")
print("Connected to Web3 via {}".format(infura_url))
print("Current block is {}".format(w3.eth.blockNumber))
balance = w3.eth.getBalance(public_key)
print("Current ETH balance:" + str(w3.fromWei(balance, 'ether')))
print("************************************")


# Importing JSON Array of ERC-20 tokens
try:
    data_file = open("data.json")
    global database
    database = json.load(data_file)
    print("Loaded database successfully!")

    for key in database["tokens"]:
        tokenNames.append((database["tokens"][key]['sign']))
    print("Loaded tokens successfully!")
except:
    print("Database error. Inspect database")
    sys.exit(0)

#Hooking up to the UniswapV2 smart contract

SushiFactory = w3.eth.contract(address=database['exchanges']['SushiSwapFactory']['address'],
                            abi=database['exchanges']['SushiSwapFactory']['ABI'])

#Trying out some combinatorics - I might be a little rusty. I'm currently saying
#that order doesn't matter - is there any difference between a USDC/USDT and
#USDT/USDC trading pair? Not that I know of - Uniswap is weird though, so I
#could be wrong
for pair in (list(combinations(tokenNames, 2))):
    token1 = database['tokens'][pair[0]]
    token2 = database['tokens'][pair[1]]
    tradingPair = (pair[0] + '/' + pair[1])

    ## I  check here that an exchange exists
    address = SushiFactory.functions.getPair(w3.toChecksumAddress(token1['address']),
    w3.toChecksumAddress(token2['address'])).call()
    if (int(address, 0) != 0):
        print(tradingPair + " : " + address)
        exchangeMap[tradingPair] = address

#Finally, dump the dictionary to a JSON for export.
with open('sushiPairsMap.json', 'w') as output:
    json.dump(exchangeMap, output)
    print("Written to sushiPairsMap.json")



# A quick test I did - you get the same address if you pass in the tokens in a different order, which is pretty neat IMO.
    # address = V2Factory.functions.getPair(w3.toChecksumAddress(token2['address']),
    # w3.toChecksumAddress(token1['address'])).call()
    #
    # tradingPair = (pair[1] + '/' + pair[0])
    # print(tradingPair + " : " + address)


##So it totally works - thanks libraries. I can't check the math now, but it
##seems to make sense. Now onto storage
