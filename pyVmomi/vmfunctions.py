import vcenterConnect as vcenter
from pyVmomi import vim


def powerOn():
    try:
        content = vcenter.si.RetrieveContent()
        obj_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
        vmlist = obj_view.view
        obj_view.Destroy()
        
        print("\n# ***** List of VMs *****\n")
        for vm in vmlist:
            print(vm.name)

        option = input("\nWhich one would you like to power on? ")

        print(f"Powering on {option}...")
        for vm in vmlist:
            if vm.name == option:
                vm.PowerOn()
        print("Operation successful.")
    
    except Exception as e:
        print("Failed to power on selected machine")
        print(e)


def powerOff():
    try:
        content = vcenter.si.RetrieveContent()
        obj_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
        vmlist = obj_view.view
        obj_view.Destroy()
        
        print("\n# ***** List of VMs *****\n")
        for vm in vmlist:
            print(vm.name)

        option = input("\nWhich one would you like to power on? ")
        print(f"Powering off {option}")
        if option == "vcenter":
            confirmation = input("WARNING. You have selected the vCenter machine. Are you sure you want to power off? (y/n)")
            if confirmation == 'n':
                return
        
        for vm in vmlist:
            if vm.name == option:
                vm.PowerOff()
        print("Operatoin successful.")
    
    except Exception as e:
        print("Failed to power off selected machine")
        print(e)


def snapshot():
    pass


def createFromTemplate():
    pass


def migrateVM():
    pass


def deleteVM():
    pass


