from web3 import Web3
import time

# Our URLs
rschain_url = 'http://91.169.139.91:8547'
rink_alchemy_http = 'https://eth-rinkeby.alchemyapi.io/v2/yDaDbJpYUxRfyFmSuHSeODCkBovd9njS'
main_alchemy_http = 'https://eth-mainnet.g.alchemy.com/v2/RqP9MjrK43mczRQwi8u8XgpGAfc75byY'
url = "https://eth-rinkeby.alchemyapi.io/v2/YAwsPVWGGRUF4aTsCTCYdgTELH4aTEPr"
web3 = Web3(Web3.HTTPProvider(main_alchemy_http)) 

if(web3.isConnected() == True):
    print('\nConnected successfully to the Mainnet...')
else:
    print('\nConnexion to the Mainnet failed')

# Function to handle or manage pending transactions found in the below functions

class Mainnet():
    
    def handle_event(self,event):

        # Convert transaction to JSON format...
        rs = Web3.toJSON(event)

        # ...And clear all the quotation marks in orer to get it in readeable format
        res = rs.replace('"', '')

        # print('\nGot other transactions ...')
        
        try:
            # Get the transaction hash in text format in order to retrieve or extract data from it
            result = web3.eth.get_transaction(res)

            # Get the contract address the transaction is communicating with 
            result_to = result['to']

            # Get the input values where we can get the tokens and amounts being traded
            res_input = result['input']

            # Get the method ID in order to identify what kind of transaction we got 
            methodId = res_input[0:10]

            # Get the Max Fee Per Gas

            result_maxFeePerGas = result['maxFeePerGas']

            # Get the Max Priority Fee Per Gas

            result_maxPriorityFeePerGas = result['maxPriorityFeePerGas']

            # print('\nGot some other transactions ....')

            if(methodId == '0x38ed1739'):
                
                # Swap Exact Tokens For Tokens
                print("\n==================================== Sell Exact Amount Of Tokens For Buying Some Tokens ====================================\n")
                print(result)

                # Get the contract address the transaction is communicating with 
                print('\nTo Market Contract : ', result_to)

                amountOut = res_input[10:74]
                amountOutDEC = int(amountOut, 16)
                print('\nAmount being traded :', amountOutDEC, ' Wei')

                # token_decimals = GetTokenValues.tokenDecimals
                # amountETH = amountOutDEC / 10**token_decimals
                # print('\nAmount being traded in readeable format:', amountETH)
                
                # If the input data length is equal to 522, that means there is no intermediary token between the two tokens being traded
                # So we got 8 entries in the array
                if(len(res_input) == 522 ):
                    token1 = res_input[394:458]
                    token1_address = '0x'+token1[24:64]
                    trading_token1 = web3.toChecksumAddress(token1_address)
                    print("\nToken 1 to Sell :", trading_token1)

                    target = res_input[458:522]
                    token_address_to_buy = '0x'+target[24:64]
                    trading_token = web3.toChecksumAddress(token_address_to_buy)
                    # handle_event.trading_token = trading_token

                    print("\nToken 2 to Buy :", trading_token)

                    print('\nMax Fee Per Gas : ', web3.fromWei(result_maxFeePerGas, ' gwei') , ' Gwei')
                    print('\nMax Priority Fee Per Gas : ', web3.fromWei(result_maxPriorityFeePerGas, 'gwei'), ' Gwei')

                # If the input data length is equal to 586, that means there is an intermediary token between the two tokens being traded.
                
                # So we got 9 entries in the array
                elif(len(res_input) == 586 ):
                    token1 = res_input[394:458]
                    token1_address = '0x'+token1[24:64]
                    trading_token1 = web3.toChecksumAddress(token1_address)
                    print("\nToken 1 to Sell :", trading_token1)

                    target = res_input[522:586]
                    token_address_to_buy = '0x'+target[24:64]
                    trading_token = web3.toChecksumAddress(token_address_to_buy)
                    # handle_event.trading_token = trading_token

                    print("\nToken 2 to Buy :", trading_token)

                else:
                    print('Error found in result input')


            if(methodId == '0x8803dbee'):
                # Swap Tokens For Exact Tokens
                print("\n==================================== Sell Some Tokens For Buying Exact Amount Of Tokens ====================================\n")
                print(result)
                print('\nTo Market Contract : ', result_to)

                amountOut = res_input[10:74]
                amountOutDEC = int(amountOut, 16)
                print('\nAmount being traded :', amountOutDEC, ' Wei')

                # token_decimals = GetTokenValues.tokenDecimals
                # amountETH = amountOutDEC / 10**token_decimals
                # print('\nAmount being traded in readeable format:', amountETH)
                

                if(len(res_input) == 522 ):
                    token1 = res_input[394:458]
                    token1_address = '0x'+token1[24:64]
                    trading_token1 = web3.toChecksumAddress(token1_address)
                    print("\nToken 1 being traded :", trading_token1)

                    target = res_input[458:522]
                    token_address_to_buy = '0x'+target[24:64]
                    trading_token = web3.toChecksumAddress(token_address_to_buy)
                    # handle_event.trading_token = trading_token

                    print("\nToken 2 to buy :", trading_token)

                elif(len(res_input) == 586 ):
                    token1 = res_input[394:458]
                    token1_address = '0x'+token1[24:64]
                    trading_token1 = web3.toChecksumAddress(token1_address)
                    print("\nToken 1 being traded :", trading_token1)

                    target = res_input[522:586]
                    token_address_to_buy = '0x'+target[24:64]
                    trading_token = web3.toChecksumAddress(token_address_to_buy)
                    # handle_event.trading_token = trading_token

                    print("\nToken 2 to buy :", trading_token)

                else:
                    print('Error found in result input')

                    
            if(methodId == "0x7ff36ab5"):
                # Swap Exact ETH For Tokens
                print("\n==================================== Sell Exact Amount Of ETH For Buying Some Tokens ====================================\n")
                print(result)
                print('\nTo Market Contract : ', result_to)

                amountOut = res_input[10:74]
                amountOutDEC = int(amountOut, 16)
                print('\nAmount being traded :', amountOutDEC, ' Wei')

                # token_decimals = GetTokenValues.tokenDecimals
                # amountETH = amountOutDEC / 10**token_decimals
                # print('\nAmount being traded in readeable format:', amountETH)
                

                if(len(res_input) == 458 ):
                    token1 = res_input[330:394]
                    token1_address = '0x'+token1[24:64]
                    trading_token1 = web3.toChecksumAddress(token1_address)
                    print("\nToken 1 being traded :", trading_token1)

                    target = res_input[394:458]
                    token_address_to_buy = '0x'+target[24:64]
                    trading_token = web3.toChecksumAddress(token_address_to_buy)
                    # handle_event.trading_token = trading_token

                    print("\nToken 2 to Buy :", trading_token)

                # elif(len(res_input) == 522 ):
                #     target = res_input[458:522]
                #     token_address_to_buy = '0x'+target[24:64]
                #     trading_token = web3.toChecksumAddress(token_address_to_buy)
                #     # handle_event.trading_token = trading_token

                #     print("\nToken to buy :", trading_token)

                # else:
                #     print('Error found in result input')

                        

            if(methodId == '0xfb3bdb41'):
                # 0x7419c508
                
                # Swap ETH For Exact Tokens
                print("\n==================================== Sell ETH For Buying Exact Amount Of Tokens ====================================\n")
                print(result)
                amountOut = res_input[10:74]
                amountOutDEC = int(amountOut, 16)
                print('\nAmount being traded :', amountOutDEC, ' Wei')

                # token_decimals = GetTokenValues.tokenDecimals
                # amountETH = amountOutDEC / 10**token_decimals
                # print('\nAmount being traded in readeable format:', amountETH)
                

                if(len(res_input) == 458 ):
                    token1 = res_input[330:394]
                    token1_address = '0x'+token1[24:64]
                    trading_token1 = web3.toChecksumAddress(token1_address)
                    print("\nToken 1 to Sell :", trading_token1)

                    target = res_input[394:458]
                    token_address_to_buy = '0x'+target[24:64]
                    trading_token = web3.toChecksumAddress(token_address_to_buy)
                    # handle_event.trading_token = trading_token

                    print("\nToken 2 to Buy :", trading_token)

                # elif(len(res_input) == 522 ):
                #     target = res_input[458:522]
                #     token_address_to_buy = '0x'+target[24:64]
                #     trading_token = web3.toChecksumAddress(token_address_to_buy)
                #     # handle_event.trading_token = trading_token

                #     print("\nToken to buy :", trading_token)

                # else:
                #     print('Error found in result input')

                

        except :
            pass


    # Loop function for going through new entry transactions
    def log_loop(self,event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(poll_interval)

    # Function to retrieve pending transactions through the loop function just above
    def main(self):
        block_filter = web3.eth.filter('pending')
        self.log_loop(block_filter, 2)



m = Mainnet()
m.main()