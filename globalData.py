import time
from web3 import Web3
import uniSwapABI

class GlobalData():

        def setGlobalData(self):
                self.rschain_url = 'http://91.169.139.91:8545'
                self.alchemy_http = 'https://eth-rinkeby.alchemyapi.io/v2/yDaDbJpYUxRfyFmSuHSeODCkBovd9njS'
                self.web3 = Web3(Web3.HTTPProvider(self.rschain_url))
                self.wallet_address = "0xe3242ca2b4036f90f42C6D7861af28d06c6161cC"
                self.uniRouterContractAddress = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D' # uniswap contract address on testnet 
                self.contract  = self.web3.eth.contract(address = self.uniRouterContractAddress, abi = uniSwapABI.uniABI)
                self.wrapped_address = self.web3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab") # weth address on testnet 0xc778417E063141139Fce010982780140Aa0cD5Ab
                self.start = time.time()

                self.nonce = self.web3.eth.getTransactionCount(self.wallet_address)

                # Token list : 
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


                self.tokens_array = [link,dai,dAITokenMock,uni,mToken,testUSDC,two,blueJay,lusdc,mockedDAI,tokenUSDT]
                print("\nYou Token List is : ")
                print(self.tokens_array)


g = GlobalData()
g.setGlobalData()