
from decimal import Decimal
from web3 import Web3
import time
import conf
import os
# import globalData
rschain_url = 'http://91.169.139.91:8545'
alchemy_http = 'https://eth-rinkeby.alchemyapi.io/v2/yDaDbJpYUxRfyFmSuHSeODCkBovd9njS'
web3 = Web3(Web3.HTTPProvider(alchemy_http))

wallet_address = "0xe3242ca2b4036f90f42C6D7861af28d06c6161cC"

link = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
dai = "0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa"
dAITokenMock = "0xaD6Db97C844Ec7Bb4c0641d436AA0D395fDD3f45"
uni = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
mToken = "0x6BD8d4c37ADB8fe976c19506012896012Da63B40"
testUSDC = "0xA6Cc591f2Fd8784DD789De34Ae7307d223Ca3dDc"
two = "0xE73bcbaF9ff36D66C5b7805c8c64D389FD7fdb75"
blueJay = "0x787f7893474191847c7DDF3a9040509f225Dd820"
lusdc = "0x787f7893474191847c7DDF3a9040509f225Dd820"
mockedDAI = "0x34270631F44C24fc320283347c38515798fA4388"
tokenUSDT = "0x045144F7532E498694d7Aae2d88E176c42c0ff97"
govOfficialTest = "0xf945e543b997ef54d8dFC20e89F3A8465Fe5Ee9d"
titi = "0x2C8d6418499a1482B8624Dc7Ee64236aA303d30B"
tiUSD = "0xc35d591e9d5D69bf1F2513828CA57B5d15CC66c8"


tokens_array = [link,dai,dAITokenMock,uni,mToken,testUSDC,two,blueJay,lusdc,mockedDAI,tokenUSDT,titi,tiUSD]


class StartTrading():

    def SwapEthForExactTokens(self):
            # nonce = web3.eth.getTransactionCount(wallet_address)

            self.tokenToTrade = self.tokenToBuy

            self.value = (self.Interface.value / 100)
            # print(value)

            self.gasValue = self.Interface.gasValue

            self.amountOut = self.tradedAmount

            self.balance = self.web3.eth.getBalance(self.wallet_address)
            self.readeable_balance = self.web3.fromWei(self.balance, 'ether')
            # print('\nActual Balance before selling your token is : ',readeable_balance, "ETH")

            # tokenToSell = handle_event.tokenToTrade

            # print('Token to sell back :', tokenToSell)

            self.sellABI = '[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint8","name":"_decimals","type":"uint8"},{"internalType":"uint256","name":"supply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"wrapped_addresser","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"wrapped_addresser","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wrapped_addresser","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

            self.sellTokenContract = self.web3.eth.contract(self.tokenToTrade, abi = self.sellABI)

            self.tokenBalance = self.sellTokenContract.functions.balanceOf(self.wallet_address).call()
            self.tokenSymbol = self.sellTokenContract.functions.symbol().call()

            self.readeable_token_balance = self.web3.fromWei(self.tokenBalance, 'ether')

            print('\nActual Balance before selling your token is : ',self.readeable_balance, "ETH")

            print("\nYour Token " + self.tokenSymbol + " Balance in ETH is : " + str('%.18f' % Decimal(self.readeable_token_balance)) + ' ' + self.tokenSymbol)

            uniSwap_tx = self.contract.functions.swapETHForExactTokens(
                self.amountOut,
                [self.wrapped_address, self.tokenToTrade],
                self.wallet_address,
                (int(time.time()) + 10000)
            ).buildTransaction({
                'from': self.wallet_address,
                'value': self.web3.toWei(self.value, 'ether'),
                'gas': 300000,
                'gasPrice': self.web3.toWei(self.gasValue, 'gwei'),
                # 'nonce': nonce,
                'nonce': self.web3.eth.getTransactionCount(self.wallet_address),
            })

            # Sign & send the transaction that is the buying transaction
            signedTx = self.web3.eth.account.sign_transaction(uniSwap_tx, private_key = conf.PRIVATE_KEY)
            tx_token = self.web3.eth.send_raw_transaction(signedTx.rawTransaction)

            # sets the text color to green
            os.system("tput setaf 2")

            print('\nTransaction Hash : ',self.web3.toHex(tx_token))

            # print(f' Your wallet address has : {readeable_token_balance} {token_symbol} after buying') 

            time.sleep(20)
            try:
                import selling
                selling.SellingProcess()
            except Exception as e:
                print(e)
    
    def SwapExactEthForTokens(self):

        self.value = (self.value / 100)
        # print(value)

        self.gasValue = self.gasValue

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
            'value': self.web3.toWei(self.value, 'ether'),
            'gas': 300000,
            'gasPrice': self.web3.toWei(self.gasValue, 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.wallet_address),
        })

        # Sign & send the transaction that is the buying transaction
        self.signedTx = self.web3.eth.account.sign_transaction(self.uniSwap_tx, private_key = conf.PRIVATE_KEY)
        self.tx_token = self.web3.eth.send_raw_transaction(self.signedTx.rawTransaction)

        # sets the text color to green
        os.system("tput setaf 2")

        print('Transaction Hash : ',self.web3.toHex(self.tx_token))

        # print(f' Your wallet address has : {readeable_token_balance} {token_symbol} after buying')

        time.sleep(20)
        try:
            import selling
            selling.SellingProcess()
            time.sleep(20)
        except Exception as e:
            print(e)

    def handle_event(self,event):
        rs = Web3.toJSON(event)
        res = rs.replace('"', '')
        
        try:
            result = web3.eth.get_transaction(res)
            res_input = result['input']
            methodId = res_input[0:10]
            result_from = result['from']

            print('\nGot other transactions...')
            # print(result)
            # print()

            if(methodId == '0x38ed1739'):
                # print("\n==================================== Swap Exact Tokens For Tokens ====================================")
                # print(result)
                if(result_from != wallet_address):

                    target = res_input[458:522]
                    token_address_to_buy = '0x'+ target[24:64]
                    # token to buy  = input value
                    
                    self.tokenToBuy = web3.toChecksumAddress(token_address_to_buy)

                    # tokens_to_trade = tokens_to_trade

                    # sets the text color to white
                    os.system("tput setaf 7")

                    if(self.tokenToBuy in tokens_array):
                        print("\n==================================== Swap Exact Tokens For Tokens ====================================")
                        print(result)

                        print('\nToken Address to Buy : ',self.tokenToBuy)

                        
                        amountOut = res_input[74:138]
                        self.amountOutDEC = int(amountOut, 16)
                        

                        print('\nAmount being traded :', self.amountOutDEC, ' wei')
                        try:
                            # time.sleep(10)
                            s.SwapEthForExactTokens()

                        except Exception as e:
                            print('\nError in Swap Exact Tokens For Tokens Buying process', e)
                            


            if(methodId == '0x8803dbee'):
                # print("\n==================================== Swap Tokens For Exact Tokens ====================================")
                # print(result)
                if(result_from != wallet_address):

                    # Toke Addresses filter goes here
                    # tokens_array = [link,dai,dAITokenMock,uni,mToken,testUSDC,two,blueJay,lusdc,mockedDAI,tokenUSDT]

                    target = res_input[458:522]
                    token_address_to_buy = '0x'+ target[24:64]
                    
                    self.tokenToBuy = web3.toChecksumAddress(token_address_to_buy)

                    # tokens_to_trade = tokens_to_trade

                    # sets the text color to white
                    os.system("tput setaf 7")

                    if(self.tokenToBuy in tokens_array):
                        print("\n==================================== Swap Tokens For Exact Tokens ====================================")
                        print(result)

                        print('\nToken Address to Buy :',self.tokenToBuy)


                        amountOut = res_input[10:74]
                        self.amountOutDEC = int(amountOut, 16)

                        print('Amount being traded :', self.amountOutDEC, ' wei')

                        try:
                            # time.sleep(10)
                            s.SwapEthForExactTokens()

                        except Exception as e:
                            print('\nError in Swap Tokens For Exact Tokens Buying process : ', e)        

                


            if(methodId == '0x7ff36ab5'):
                # print("\n==================================== Swap Exact ETH For Tokens ====================================")
                # print(result)
                if(result_from != wallet_address):

                    target = res_input[394:458]
                    token_address_to_buy = '0x'+ target[24:64]
                    
                    self.tokenToBuy = web3.toChecksumAddress(token_address_to_buy)

                    os.system("tput setaf 7")

                    if(self.tokenToBuy in tokens_array):
                        print("\n==================================== Swap Exact ETH For Tokens ====================================")
                        print(result)

                        print('\nToken Address to Buy :',self.tokenToBuy)


                        amountOut = res_input[10:74]
                        self.amountOutDEC = int(amountOut, 16)
                       
                        print('Amount being traded :', self.amountOutDEC, ' wei')
                       
                        try:
                            # time.sleep(10)

                            s.SwapExactEthForTokens()

                        except Exception as e:
                            print('\nError in Buying process : ', e)



            if(methodId == '0xfb3bdb41'):
                # print("\n==================================== Swap ETH For Exact Tokens ====================================")
                # print(result)
                if(result_from != wallet_address):


                    target = res_input[394:458]
                    token_address_to_buy = '0x'+ target[24:64]
                    
                    self.tokenToBuy = web3.toChecksumAddress(token_address_to_buy)

                    os.system("tput setaf 7")

                    if(self.tokenToBuy in tokens_array):
                        print("\n==================================== Swap ETH For Exact Tokens ====================================")
                        print(result)

                        print('\nToken Address to Buy : ',self.tokenToBuy)
                        
                        amountOut = res_input[10:74]
                        self.amountOutDEC = int(amountOut, 16)
                            
                        print('Amount being traded :', self.amountOutDEC, ' wei')

                        try:
                            # time.sleep(10)

                            s.SwapEthForExactTokens()
                        except Exception as e:
                            print('\nError in Swap ETH For Exact Tokens Buying process : ', e)

        except:
            pass

    def log_loop(self,event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(poll_interval)

    def home(self):
        block_filter = web3.eth.filter('pending')
        self.log_loop(block_filter, 2)


s = StartTrading()
s.home()