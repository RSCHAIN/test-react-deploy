import os



class MainBot():

    def connexion(self):
        # sets the text color to green
        os.system("tput setaf 2")

        print("\n\t\tWelcome To Smart Trading Terminal User Interface\t\t\t")
        
        # sets the text color to white
        os.system("tput setaf 7")
        
        print("\t-------------------------------------------------")
        print("\n\tEnter a number to do an action \t")

        while True:
            print("""
                1 - Trade Only on UniSwap
                2 - Trade Only on SushiSwap
                3 - Buy on UniSwap and Sell on SushiSwap
                4 - Buy on SushiSwap and Sell on UniSwap
                0 - Trade Some Tokens
                """)

            number=input("Enter your choice : ")

            try:
                
                ch = int(number)

                if(ch == 1):
                    from trade_on_uni import home
                    home()
                
                elif (ch == 2):
                    from trade_on_sushi import home
                    home()

                elif (ch == 3):
                    from trade_uni_to_sushi import home
                    home()
                    
                elif (ch == 4):
                    from trade_sushi_to_uni import home
                    home()
                
                elif (ch == 0):
                    from testnet_interface import home
                    home()
                
                elif (type(ch) != int):
                    print("Invalid entry")
                    input("Press enter to continue or CTRL + C to exit ")
                    os.system("clear")

                else:
                    print("Invalid entry")
            
                input("Press enter to continue or CTRL + C to exit ")
                os.system("clear")

            except:
                print('Please enter a digit')


m = MainBot()
m.connexion()