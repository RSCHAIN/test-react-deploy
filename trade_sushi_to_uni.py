from decimal import Decimal
import os
import time
from web3 import Web3
import conf
import uniSwapABI

class TradeUniToSushi():

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
                if(methodId == '0x38ed1739'):
                    
                    if(result_from != self.wallet_address):

                            print("\n==================================== Swap Exact Tokens For Tokens ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)

                            self.gasAddition = self.result_gasPrice + self.gasValue
                            self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                            self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                            self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            # Traverse the input data field 
                            data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                            nb_tokens = int(data[5], 16)

                            first_inputs = data[:2]

                            for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                                self.amount1 = int(first_inputs[0], 16)
                                self.amount2 = int(first_inputs[1], 16)

                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")

                            last_inputs = data[-nb_tokens:]
                            
                            for i,j in enumerate(last_inputs):
                                token1 = last_inputs[0]
                                token1_checksum = "0x" + token1[24:]
                                token1_address = self.web3.toChecksumAddress(token1_checksum)
                                token2 = last_inputs[-1]
                                token2_checksum = "0x" + token2[24:]
                                token2_address = self.web3.toChecksumAddress(token2_checksum)

                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            self.tokenToBuy = token2_address
                            


                            try:
                                # time.sleep(10)
                                
                                p.BuyTokensOnSushiSwap()

                            except Exception as e:
                                print('\nError in Swap Exact Tokens For Tokens Buying process', e)

                # Swap Tokens For Exact Tokens               
                if(methodId == '0x8803dbee'):
                    if(result_from != self.wallet_address):

                            print("\n==================================== Swap Tokens For Exact Tokens ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)

                            self.gasAddition = self.result_gasPrice + self.gasValue
                            self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                            self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                            self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            # # Traverse the input data field 
                            data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                            nb_tokens = int(data[5], 16)

                            first_inputs = data[:2]

                            for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                                self.amount1 = int(first_inputs[0], 16)
                                self.amount2 = int(first_inputs[1], 16)

                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")

                            last_inputs = data[-nb_tokens:]
                            
                            for i,j in enumerate(last_inputs):
                                token1 = last_inputs[0]
                                token1_checksum = "0x" + token1[24:]
                                token1_address = self.web3.toChecksumAddress(token1_checksum)
                                token2 = last_inputs[-1]
                                token2_checksum = "0x" + token2[24:]
                                token2_address = self.web3.toChecksumAddress(token2_checksum)

                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            self.tokenToBuy = token2_address

                            try:
                                # time.sleep(10)
                                
                                p.BuyTokensOnSushiSwap()

                            except Exception as e:
                                print('\nError in Swap Tokens For Exact Tokens Buying process : ', e)        

                # Swap Exact ETH For Tokens
                if(methodId == '0x7ff36ab5'):
                    
                    if(result_from != self.wallet_address):
                        print("\n==================================== Swap Exact ETH For Tokens ====================================")
                        print(result)

                        print("\nSender's Gas Price : ", self.result_gasPrice)

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                        print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                        # Traverse the input data field 
                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[4], 16)
                        # # # print("\nNumber of tokens being traded : ", nb_tokens)

                        
                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount2 = int(first_inputs[0], 16)

                        self.amount1 = self.result_value 
                        print("\nAmount 1 : ", self.amount1 , " Wei")
                        print("\nAmount 2 : ", self.amount2 , " Wei")


                        last_inputs = data[-nb_tokens:]
                        
                        for i,j in enumerate(last_inputs):

                            # print("\nToken : ",i , " is : ", j[24:]) #last_input[0]
                            
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)
                            
                        print("\nToken 1 : ",token1_address)
                        print("\nToken 2 : ",token2_address)
                        self.tokenToBuy = token2_address
                            
                        try:
                            # time.sleep(10)
                            p.BuyTokensOnSushiSwap()

                        except Exception as e:
                            print('\nError in Buying process : ', e)

                # Swap ETH For Exact Tokens
                if(methodId == '0xfb3bdb41'):
                    if(result_from != self.wallet_address):

                        print("\n==================================== Swap ETH For Exact Tokens ====================================")
                        print(result)
                      
                        print("\nSender's Gas Price : ", self.result_gasPrice)

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                        print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                        target = res_input[394:458]
                        token_address_to_buy = '0x'+ target[24:64]
                        
                        self.tokenToBuy = self.web3.toChecksumAddress(token_address_to_buy)

                        # # # Traverse the input data field 
                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[4], 16)
                        # print("\nNumber of tokens being traded : ", nb_tokens)

                        
                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount2 = int(first_inputs[0], 16)
                        self.amount1 = self.result_value 
                        print("\nAmount 1 : ", self.amount1 , " Wei")
                        print("\nAmount 2 : ", self.amount2 , " Wei")


                        last_inputs = data[-nb_tokens:]
                        
                        for i,j in enumerate(last_inputs):

                            # print("\nToken : ",i , " is : ", j[24:]) #last_input[0]
                            
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)
                            
                        print("\nToken 1 : ",token1_address)
                        print("\nToken 2 : ",token2_address)
                        self.tokenToBuy = token2_address

                        try:
                            # time.sleep(10)
                            
                            p.BuyTokensOnSushiSwap()

                        except Exception as e:
                            print('\nError in Swap ETH For Exact Tokens Buying process : ', e)

                # swap Exact Tokens For ETH
                if(methodId == "0x18cbafe5"):
                    if (result_from != self.wallet_address):

                            print("\n==================================== Swap Exact Tokens For ETH ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)

                            self.gasAddition = self.result_gasPrice + self.gasValue
                            self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                            self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                            self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            # Traverse the input data field 
                            data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                            nb_tokens = int(data[5], 16)

                            first_inputs = data[:2]

                            for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                                self.amount1 = int(first_inputs[0], 16)
                                self.amount2 = int(first_inputs[1], 16)

                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")

                            last_inputs = data[-nb_tokens:]
                            
                            for i,j in enumerate(last_inputs):
                                token1 = last_inputs[0]
                                token1_checksum = "0x" + token1[24:]
                                token1_address = self.web3.toChecksumAddress(token1_checksum)
                                token2 = last_inputs[-1]
                                token2_checksum = "0x" + token2[24:]
                                token2_address = self.web3.toChecksumAddress(token2_checksum)

                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            self.tokenToBuy = token2_address

                            # try:
                            #     # time.sleep(10)

                            #     s.SwapExactEthForTokens()

                            # except Exception as e:
                            #     print('\nError in Buying process : ', e)
                            

                # swap tokens for exact eth
                if(methodId == "0x4a25d94a"):
                    if (result_from != self.wallet_address):
                            print("\n==================================== Swap Tokens For Exact ETH ====================================")
                            print(result)

                            print("\nSender's Gas Price : ", self.result_gasPrice)

                            self.gasAddition = self.result_gasPrice + self.gasValue
                            self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                            print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                            self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                            print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                            self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                            print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            # Traverse the input data field 
                            data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                            nb_tokens = int(data[5], 16)

                            first_inputs = data[:2]

                            for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                                self.amount1 = int(first_inputs[0], 16)
                                self.amount2 = int(first_inputs[1], 16)

                            print("\nAmount 1 : ", self.amount1 , " Wei")
                            print("\nAmount 2 : ", self.amount2 , " Wei")

                            last_inputs = data[-nb_tokens:]
                            
                            for i,j in enumerate(last_inputs):
                                token1 = last_inputs[0]
                                token1_checksum = "0x" + token1[24:]
                                token1_address = self.web3.toChecksumAddress(token1_checksum)
                                token2 = last_inputs[-1]
                                token2_checksum = "0x" + token2[24:]
                                token2_address = self.web3.toChecksumAddress(token2_checksum)

                            print("\nToken 1 : ",token1_address)
                            print("\nToken 2 : ",token2_address)
                            self.tokenToBuy = token2_address

                            # try:
                            #     # time.sleep(10)
                            #     s.SwapExactEthForTokens()

                            # except Exception as e:
                            #     print('\nError in Buying process : ', e)

                # swap exact tokens for tokens + fees
                if(methodId == "0x5c11d795"):
                    if (result_from != self.wallet_address):
                        print("\n==================================== Swap Exact Tokens For Tokens + Fees ====================================")
                        print(result)

                        print("\nSender's Gas Price : ", self.result_gasPrice)

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                        print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            # Traverse the input data field 
                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[5], 16)

                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount1 = int(first_inputs[0], 16)
                            self.amount2 = int(first_inputs[1], 16)

                        print("\nAmount 1 : ", self.amount1 , " Wei")
                        print("\nAmount 2 : ", self.amount2 , " Wei")

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)

                        print("\nToken 1 : ",token1_address)
                        print("\nToken 2 : ",token2_address)
                        self.tokenToBuy = token2_address

                        try:
                            # time.sleep(10)
                            p.BuyTokensOnSushiSwap()

                        except Exception as e:
                            print('\nError in Buying process : ', e)

                # swap exact eth for tokens + fees
                if(methodId == "0xb6f9de95"):

                    if (result_from != self.wallet_address):

                        print("\n==================================== Swap Exact ETH For Tokens + Fees ====================================")
                        print(result)

                        print("\nSender's Gas Price : ", self.result_gasPrice)

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                        print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                        target = res_input[394:458]
                        token_address_to_buy = '0x'+ target[24:64]
                            
                        self.tokenToBuy = self.web3.toChecksumAddress(token_address_to_buy)

                        # os.system("tput setaf 7")

                        # # Traverse the input data field 
                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[4], 16)
                        # # print("\nNumber of tokens being traded : ", nb_tokens)

                        
                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                            # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount2 = int(first_inputs[0], 16)
                        self.amount1 = self.result_value 
                        print("\nAmount 1 : ", self.amount1 , " Wei")
                        print("\nAmount 2 : ", self.amount2 , " Wei")


                        last_inputs = data[-nb_tokens:]
                        
                        for i,j in enumerate(last_inputs):

                            # print("\nToken : ",i , " is : ", j[24:]) #last_input[0]
                            
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)
                            
                        print("\nToken 1 : ",token1_address)
                        print("\nToken 2 : ",token2_address)
                        self.tokenToBuy = token2_address

                        try:
                            # time.sleep(10)
                            p.BuyTokensOnSushiSwap()

                        except Exception as e:
                            print('\nError in Buying process : ', e)
                        

                # swap exact tokens for eth + fees
                if(methodId == "0x18cbafe5"):
                    if (result_from != self.wallet_address):
                        print("\n==================================== Swap Exact Tokens For ETH + Fees ====================================")
                        print(result)

                        print("\nSender's Gas Price : ", self.result_gasPrice)

                        self.gasAddition = self.result_gasPrice + self.gasValue
                        self.ourGasPrice = self.web3.fromWei(self.gasAddition, 'gwei')

                        print("\nOur proposed Gas Price (Sender Gas Price + Our input Gas Price ) : ", self.ourGasPrice , " Gwei")

                        self.maxFeePerGasGwei = self.web3.fromWei(self.maxFeePerGas, 'gwei')
                        print('\nMax Fee Per Gas', self.maxFeePerGasGwei)

                        self.maxPriorityFeePerGasGwei = self.web3.fromWei(self.maxPriorityFeePerGas, 'gwei')
                        print('\nMax Priority Fee Per Gas', self.maxPriorityFeePerGasGwei)

                            # Traverse the input data field 
                        data = [input_rest[i:i+cut_nb] for i in range(0, len(input_rest), cut_nb)]
                        nb_tokens = int(data[5], 16)

                        first_inputs = data[:2]

                        for i,t in enumerate(first_inputs):
                                # print("\nAmounts ", i, " : ", int(t, 16), " Wei")
                            self.amount1 = int(first_inputs[0], 16)
                            self.amount2 = int(first_inputs[1], 16)

                        print("\nAmount 1 : ", self.amount1 , " Wei")
                        print("\nAmount 2 : ", self.amount2 , " Wei")

                        last_inputs = data[-nb_tokens:]
                            
                        for i,j in enumerate(last_inputs):
                            token1 = last_inputs[0]
                            token1_checksum = "0x" + token1[24:]
                            token1_address = self.web3.toChecksumAddress(token1_checksum)
                            token2 = last_inputs[-1]
                            token2_checksum = "0x" + token2[24:]
                            token2_address = self.web3.toChecksumAddress(token2_checksum)

                        print("\nToken 1 : ",token1_address)
                        print("\nToken 2 : ",token2_address)
                        self.tokenToBuy = token2_address

                        # try:
                        #     # time.sleep(10)

                        #     s.SwapExactEthForTokens()

                        # except Exception as e:
                        #     print('\nError in Buying process : ', e)
            except:
                pass
    

    def BuyTokensOnSushiSwap(self):

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

            self.uniSwap_tx = self.sushiContract.functions.swapExactETHForTokens(
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


p = TradeUniToSushi()
p.home()