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
                1 - Connect to Testnet
                2 - Connect to the Mainnet
                3 - Trade All Tokens on Testnet
                """)

            number=input("Enter your choice : ")

            try:
                
                ch = int(number)
                if(ch == 1):
                    
                    # from testnet_interface import home
                    # home()
                    import connect_testnet
                    connect_testnet.connexion()


                elif (ch == 2):
                    import mainnet
                    mainnet.main()
                
                elif (ch == 3):
                    from  all_testnet_tokens import home
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