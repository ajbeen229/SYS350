from os import system
import vmutils as utils
import vmfunctions as functions


def utilMenu():
    print("\n[1] vCenter Info")
    print("[2] Session Details")
    print("[3] VM Details")
    print("[4] Configure VMs")
    print("[0] Exit")



def functionMenu():
    print("\n[1] Power On VM")
    print("[2] Power Off VM")
    print("[3] Snapshot VM")
    print("[4] Create VM From Template")
    print("[5] Move VM to Folder")
    print("[6] Delete VM")
    print("[0] Return")



while True:

    system('clear')
    print("=====================================")
    print("             VM Utilities            ")
    print("=====================================")
    utilMenu()
    option = input("Enter option: ")

    match option:
        case "1":
            utils.vcenterInfo()
            input()
        case "2":
            utils.sessionInfo()
            input()
        case "3":
            utils.vmInfo()
            input()
        case "4":
            
            while True:
                system('clear')
                print("=====================================")
                print("             VM Functions            ")
                print("=====================================")
                functionMenu()
                option = input("Enter option: ")

                match option:
                    case "1":
                        functions.powerOn()
                        input()
                    case "0":
                        break

        case "0":
            break
        case _:
            break