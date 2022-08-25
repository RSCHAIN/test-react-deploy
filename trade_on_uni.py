from decimal import Decimal
import time
from web3 import Web3
import conf
import uniSwapABI

class TradeOnUni():

    def __init__ (self):
        self.rschain_url = 'http://91.169.139.91:8545'
        self.alchemy_http = 'https://eth-rinkeby.alchemyapi.io/v2/yDaDbJpYUxRfyFmSuHSeODCkBovd9njS'
        self.main_alchemy_http = 'https://eth-mainnet.g.alchemy.com/v2/RqP9MjrK43mczRQwi8u8XgpGAfc75byY'
        self.url = "https://eth-rinkeby.alchemyapi.io/v2/YAwsPVWGGRUF4aTsCTCYdgTELH4aTEPr"
        self.web3 = Web3(Web3.HTTPProvider(self.url))

        self.uniRouterContractAddress = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D' # uniswap contract address on testnet 

        self.contract  = self.web3.eth.contract(address = self.uniRouterContractAddress, abi = uniSwapABI.uniABI)

        self.sushirouterContractAddress = '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506' # sushiswap contract address on rinkeby testnet 

        self.sushiContract  = self.web3.eth.contract(address = self.sushirouterContractAddress, abi = uniSwapABI.uniABI)

        self.wallet_address = "0xe3242ca2b4036f90f42C6D7861af28d06c6161cC"

        self.wrapped_address = self.web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")

        self.eth_value = int(input("\nWhat is the amount (in percentage) of ETH you want to expend : "))
        
        self.gasValue = self.web3.toWei(int(input("\nEnter the amount of Gas you are willing to pay in addition : ")), 'gwei')

        self.link = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
        self.dai = "0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa"
        self.dAITokenMock = "0xaD6Db97C844Ec7Bb4c0641d436AA0D395fDD3f45"
        self.uni = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
        self.mToken = "0x6BD8d4c37ADB8fe976c19506012896012Da63B40"
        self.testUSDC = "0xA6Cc591f2Fd8784DD789De34Ae7307d223Ca3dDc"
        self.two = "0xE73bcbaF9ff36D66C5b7805c8c64D389FD7fdb75"
        self.blueJay = "0x787f7893474191847c7DDF3a9040509f225Dd820"
        self.lusdc = "0x787f7893474191847c7DDF3a9040509f225Dd820"
        self.mockedDAI = "0x34270631F44C24fc320283347c38515798fA4388"
        self.tokenUSDT = "0x045144F7532E498694d7Aae2d88E176c42c0ff97"
        self.govOfficialTest = "0xf945e543b997ef54d8dFC20e89F3A8465Fe5Ee9d"
        # titi = "0x2C8d6418499a1482B8624Dc7Ee64236aA303d30B"
        # tiUSD = "0xc35d591e9d5D69bf1F2513828CA57B5d15CC66c8"


        self.tokens_array = [self.link,self.dai,self.dAITokenMock,self.uni,self.mToken,self.testUSDC,self.two,self.blueJay,self.lusdc,self.mockedDAI,self.tokenUSDT]

    def handle_event(self,event):
            rs = Web3.toJSON(event)
            res = rs.replace('"', '')
            
            try:
                result = self.web3.eth.get_transaction(res)
                res_input = result['input']
                methodId = res_input[0:10]
                input_rest = res_input[10:len(res_input)]
                cut_nb = 64
                
                result_from = result['from']
                self.result_value = result['value']
                self.result_gasPrice = result['gasPrice']
                self.maxFeePerGas = result['maxFeePerGas']
                self.maxPriorityFeePerGas = result['maxPriorityFeePerGas']

                # print('\nGot other transactions...')
                # print(result)
                # print()

                # Swap Exact Tokens For Tokens 
                if(methodId == '0x38ed1739' or methodId == '0x5c11d795' or methodId == '0x8803dbee'):
                    
                    if(result_from != self.wallet_address):
                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')

                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[5], 16)

                        first_inputs = data[:2]

                        # Traverse the input data field 
                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount1 = int(first_inputs[0], 16)
                            self.amount2 = int(first_inputs[1], 16)

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)
                        
                        self.tokenToBuy = token2_address

                        if(self.tokenToBuy in self.tokens_array and self.amount2 == 0):
                            print("\n==================================== Swap Exact Tokens For Tokens ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)

                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")

                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            
                            try:
                                # time.sleep(10)
                                
                                p.BuyTokensOnUniSwap()

                            except Exception as e:
                                print('\nError in Swap Exact Tokens For Tokens Buying process', e)
                        else:
                            pass

                # Swap Exact ETH For Tokens
                if(methodId == '0x7ff36ab5' or methodId == '0xfb3bdb41' or methodId == '0xb6f9de95'):
                    
                    if(result_from != self.wallet_address):

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')

                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[4], 16)

                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount2 = int(first_inputs[0], 16)
                        self.amount1 = self.result_value 

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):

                            # print("\nToken : ",i , " is : ", j[24:]) #last_input[0]
                                
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)

                        self.tokenToBuy = token2_address

                        if(self.tokenToBuy in self.tokens_array and self.amount2 == 0):
                            print("\n==================================== Swap Exact ETH For Tokens ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)

                            
                            

                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                            
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                            
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)
                            
                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")


                            
                                
                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            
                                
                            try:
                                # time.sleep(10)
                                p.BuyTokensOnUniSwap()

                            except Exception as e:
                                print('\nError in Buying process : ', e)
                        else:
                            pass

                # swap Exact Tokens For ETH
                if(methodId == "0x18cbafe5"):
                    if (result_from != self.wallet_address):

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')

                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[5], 16)

                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount1 = int(first_inputs[0], 16)
                            self.amount2 = int(first_inputs[1], 16)

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)

                        self.tokenToBuy = token2_address

                        if(self.tokenToBuy in self.tokens_array and self.amount2 == 0):
                            print("\n==================================== Swap Exact Tokens For ETH ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)
                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)
                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")
                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            

                            # try:
                            #     # time.sleep(10)

                            #     s.SwapExactEthForTokens()

                            # except Exception as e:
                            #     print('\nError in Buying process : ', e)

                        else:
                            pass   

                # swap tokens for exact eth
                if(methodId == "0x4a25d94a"):
                    if (result_from != self.wallet_address):

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')

                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[5], 16)

                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount1 = int(first_inputs[0], 16)
                            self.amount2 = int(first_inputs[1], 16)

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)

                        self.tokenToBuy = token2_address

                        if(self.tokenToBuy in self.tokens_array and self.amount2 == 0):
                            print("\n==================================== Swap Tokens For Exact ETH ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)
                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)
                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")
                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            

                            # try:
                            #     # time.sleep(10)
                            #     s.SwapExactEthForTokens()

                            # except Exception as e:
                            #     print('\nError in Buying process : ', e)
                        else:
                            pass

                # swap exact tokens for eth + fees

                if(methodId == "0x18cbafe5"):
                    if (result_from != self.wallet_address):

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')

                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[5], 16)

                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount1 = int(first_inputs[0], 16)
                            self.amount2 = int(first_inputs[1], 16)

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)
                        
                        self.tokenToBuy = token2_address

                        if(self.tokenToBuy in self.tokens_array and self.amount2 == 0):
                            print("\n==================================== Swap Exact Tokens For ETH + Fees ====================================")
                            print(result)
                            print("\nSender's Gas Price : ", self.result_gasPrice)
                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)
                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")
                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                        

                        # try:
                        #     # time.sleep(10)

                        #     s.SwapExactEthForTokens()

                        # except Exception as e:
                        #     print('\nError in Buying process : ', e)
                        else:
                            pass
            except:
                pass

    def BuyTokensOnUniSwap(self):

            self.eth_value = (self.eth_value / 100)
            # print(value)

            self.gasValue = self.ourGasPrice

            # break_input = input("\n Break input ")

            self.amountOutMin = 0

            # nonce = web3.eth.getTransactionCount(wallet_address)

            self.tokenToSwap = self.tokenToBuy

            self.sellABI = '[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint8","name":"_decimals","type":"uint8"},{"internalType":"uint256","name":"supply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"wrapped_addresser","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"wrapped_addresser","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

            self.sellTokenContract = self.web3.eth.contract(self.tokenToSwap, abi = self.sellABI)

            self.tokenBalance = self.sellTokenContract.functions.balanceOf(self.wallet_address).call()
            self.tokenSymbol = self.sellTokenContract.functions.symbol().call()

            self.readeable_token_balance = self.web3.fromWei(self.tokenBalance, 'ether')

            print("\nYour Token " + self.tokenSymbol + " Balance is : " + str('%.18f' % Decimal(self.readeable_token_balance)) + ' ' + self.tokenSymbol)

            self.uniSwap_tx = self.contract.functions.swapExactETHForTokens(
                self.amountOutMin,
                [self.wrapped_address, self.tokenToSwap],
                self.wallet_address,
                (int(time.time()) + 10000)
            ).buildTransaction({
                'from': self.wallet_address,
                'value': self.web3.toWei(self.eth_value, 'ether'),
                'gas': 300000,
                'gasPrice': self.web3.toWei(self.gasValue, 'gwei'),
                'nonce': self.web3.eth.getTransactionCount(self.wallet_address),
            })

            # Sign & send the transaction that is the buying transaction
            self.signedTx = self.web3.eth.account.sign_transaction(self.uniSwap_tx, private_key = conf.PRIVATE_KEY)
            self.tx_token = self.web3.eth.send_raw_transaction(self.signedTx.rawTransaction)

            # sets the text color to green
            # os.system("tput setaf 2")

            print('Transaction Hash : ',self.web3.toHex(self.tx_token))

            # print(f' Your wallet address has : {readeable_token_balance} {token_symbol} after buying')

            time.sleep(20)
            try:
                p.SellTokensOnUniSwap()
                time.sleep(20)
            except Exception as e:
                print(e)

    def SellTokensOnUniSwap(self):

        # ourGasPrice = handle_event.ourGasPrice
        balance = self.web3.eth.getBalance(self.wallet_address)
        readeable_balance = self.web3.fromWei(balance, 'ether')

        # sets the text color to white
        # os.system("tput setaf 7")

        print('\nActual Balance before selling your token is : ',readeable_balance, "ETH")

        self.tokenToSell = self.tokenToBuy
        print('Token to sell back :', self.tokenToSell)

        sellABI = '[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint8","name":"_decimals","type":"uint8"},{"internalType":"uint256","name":"supply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"wrapped_addresser","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"wrapped_addresser","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

        sellTokenContract = self.web3.eth.contract(self.tokenToSell, abi = sellABI)

        tokenBalance = sellTokenContract.functions.balanceOf(self.wallet_address).call()
        tokenSymbol = sellTokenContract.functions.symbol().call()
        tokenDecimals = sellTokenContract.functions.decimals().call()
        print('\ntoken decimals : ', tokenDecimals)
        
        readeable_token_balance = self.web3.fromWei(tokenBalance, 'ether')

        sell_token_value = self.web3.toWei(readeable_token_balance, 'ether')

        print("\nYour Token " + tokenSymbol + " Balance is : " + str('%.18f' % Decimal(readeable_token_balance)) + ' ' + tokenSymbol)

        # Approve token transaction first
        try:
            token_approve = sellTokenContract.functions.approve(self.uniRouterContractAddress, tokenBalance).buildTransaction({
                'from': self.wallet_address,
                'gas': 300000,
                'gasPrice': self.web3.toWei('15', 'gwei'),
                # 'nonce': nonce_nb,
                'nonce': self.web3.eth.getTransactionCount(self.wallet_address),
            })

            signedTx = self.web3.eth.account.sign_transaction(token_approve, private_key = conf.PRIVATE_KEY)
            tx_token = self.web3.eth.send_raw_transaction(signedTx.rawTransaction)

            # sets the text color to yellow
            # os.system("tput setaf 3")

            print("Approved Transaction Hash is : " + self.web3.toHex(tx_token))
        except Exception as e:
            # sets the text color to red
            # os.system("tput setaf 1")

            print("Approval failed ", e)

        #after approve, wait for 10 sec before sending the tx
        time.sleep(10)  

        print(f"Swapping {sell_token_value} {tokenSymbol} for ETH")

        try:
            uniSwap_tx = self.contract.functions.swapExactTokensForETH(
                sell_token_value,
                0,
                [self.tokenToSell, self.wrapped_address],
                self.wallet_address,
                (int(time.time()) + 1000000)
            ).buildTransaction({
                'from': self.wallet_address,
                'gas': 300000,
                'gasPrice': self.web3.toWei(20, 'gwei'),
                # 'gasPrice': web3.toWei('20', 'gwei'),
                # 'nonce': nonce3,
                'nonce': (self.web3.eth.getTransactionCount(self.wallet_address)+1),
            })

            signedTxn = self.web3.eth.account.sign_transaction(uniSwap_tx, private_key = conf.PRIVATE_KEY)
            txn_token = self.web3.eth.send_raw_transaction(signedTxn.rawTransaction)

            # sets the text color to green
            # os.system("tput setaf 2")

            print(f"\n{tokenSymbol} sold successfully. Your transaction Hash is : " + self.web3.toHex(txn_token))
        except Exception as e:
            # sets the text color to red
            # os.system("tput setaf 1")

            print("Selling failed ", e)

        time.sleep(10)

    def log_loop(self,event_filter, poll_interval):
            while True:
                for event in event_filter.get_new_entries():
                    self.handle_event(event)
                time.sleep(poll_interval)

    def home(self):
            block_filter = self.web3.eth.filter('pending')
            self.log_loop(block_filter, 2)


p = TradeOnUni()
p.home()