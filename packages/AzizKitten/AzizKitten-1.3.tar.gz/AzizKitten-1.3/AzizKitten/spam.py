class Spam():
    def start():
        from platform import system as platform
        from time import sleep
        if platform == 'iOS':
            print('This feature doesn\'t support iOS.')
        elif platform == 'android':
            print('This feature doesn\'t support android.')
        else:
            try:
                from pyautogui import typewrite,press
                limit = int(input("Select limit of the messages:\n>>    "))
                if limit == 0:
                    print("Sorry, limit can't be 0")
                elif limit < 0:
                    print("Sorry, limit can't be negative")
                else:
                    msg = input("Enter the message:\n>>    ")
                    sleep(3)
                    while limit > 0:            
                        typewrite(msg)
                        press('Enter')
                        limit -= 1
            except:
                from pip import main
                from os import system as sys
                main(["install", "--user", "pyautogui"])
                if platform == 'windows':
                    cmd = 'clear'
                else:
                    cmd = 'cls'
                sys(cmd)
                from pyautogui import typewrite,press
                limit = int(input("Select limit of the messages:\n>>    "))
                if limit == 0:
                    print("Sorry, limit can't be 0")
                elif limit < 0:
                    print("Sorry, limit can't be negative")
                else:
                    msg = input("Enter the message:\n>>    ")
                    sleep(3)
                    while limit > 0:            
                        typewrite(msg)
                        press('Enter')
                        limit -= 1