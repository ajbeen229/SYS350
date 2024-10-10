import vcenterConnect as vcenter
from pyVmomi import vim
import traceback


def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print("Operation successful.")
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            print(task.info.error)
            task_done = True


def getNumberInput(prompt):
    userInput = input(prompt)
    isNumber = False
    while not isNumber:
        try:
            userInput = int(userInput)
            isNumber = True
        except:
            print("Did not enter a number.")
            userInput = input(prompt)

    return userInput


def powerOn():
    try:
        content = vcenter.si.RetrieveContent()
        obj_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
        vmlist = obj_view.view
        obj_view.Destroy()
        
        print("\n# ***** List of VMs *****\n")
        vms = [vm for vm in vmlist if not vm.summary.config.template]
        for vm in vms:
            print(f"{vm.name:<20} {vm.runtime.powerState}")

        option = input("\nWhich one would you like to power on? ")
        while option not in [vm.name for vm in vms]:
            option = input("Please enter a name from the list: ")

        print(f"Powering on {option}...")
        for vm in vms:
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
        vms = [vm for vm in vmlist if not vm.summary.config.template]
        for vm in vms:
            print(f"{vm.name:<20} {vm.runtime.powerState}")

        option = input("\nWhich one would you like to power off? ")
        while option not in [vm.name for vm in vms]:
            option = input("Please enter a name from the list: ")

        print(f"Powering off {option}")
        if option == "vcenter":
            confirmation = input("WARNING. You have selected the vCenter machine. Are you sure you want to power off? (y/n)")
            if confirmation == 'n':
                return
        
        for vm in vms:
            if vm.name == option:
                vm.PowerOff()
                print("Operation successful.")
    
    except Exception as e:
        print("Failed to power off selected machine")
        print(e)


def snapshot():
    try:
        content = vcenter.si.RetrieveContent()
        obj_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
        vmlist = obj_view.view
        obj_view.Destroy()
        
        print("\n# ***** List of VMs *****\n")
        vms = [vm for vm in vmlist if not vm.summary.config.template]
        for vm in vms:
            print(vm.name)

        option = input("\nWhich one would you like to snapshot? ")
        while option not in [vm.name for vm in vms]:
            option = input("Please enter a name from the list: ")
        
        for vm in vms:
            if vm.name == option:
                name = input("Enter a name for the snapshot: ")
                desc = input("Enter a description for the snapshot: ")
                print(f"\nCreating a snapshot for {option}")
                vm.PowerOff()
                wait_for_task(vm.CreateSnapshot(name, desc, False, False)) # name, description, capture memory, quiesce (capture file system while on)
        
    except Exception as e:
        print("Failed to snapshot selected machine")
        print(e)


def configSpecs(vm):
    spec = vim.vm.ConfigSpec()
    
    name = vm.name
    
    oldnumCPU = vm.summary.config.numCpu
    oldmemAmt = vm.summary.config.memorySizeMB

    newnumCPU = 0
    newmemAmt = 0

    while True:
        print("\nWhat would you like to configure?")
        print(f"\n[1] VM Name ({name})")
        print(f"\n[2] Number of CPU Cores ({oldnumCPU})")
        print(f"\n[3] Memory Amount ({int(oldmemAmt)/1000:.0f}GB)")
        print("\n[0] Return")
        option = input("\nEnter number: ")

        match option:
            case "1":
                name = input("\nEnter new name: ")
            case "2":
                newnumCPU = input("\nEnter the number of cores: ")
                try:
                    newnumCPU = int(newnumCPU)
                except:
                    print("Did not enter a number")
            case "3":
                newmemAmt = input("\nEnter memory amount (GB): ")
                try:
                    newmemAmt = int(newmemAmt)
                except:
                    print("Did not enter a number")
            case "0":
                break

    spec.name = name
    if newnumCPU: spec.numCPUs = newnumCPU
    if newmemAmt: spec.memoryMB = newmemAmt * 1000

    return spec


def tweak():
    try:
        content = vcenter.si.RetrieveContent()
        obj_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
        vmlist = obj_view.view
        obj_view.Destroy()
        
        print("\n# ***** List of VMs *****\n")
        vms = [vm for vm in vmlist if not vm.summary.config.template]
        for vm in vms:
            print(vm.name)

        option = input("\nWhich one would you like to reconfigure? ")
        while option not in [vm.name for vm in vms]:
            option = input("Please enter a name from the list: ")

        vm = None
        for v in vms:
            if v.name == option:
                vm = v
                
        spec = configSpecs(vm)

        for vm in vms:
            if vm.name == option:
                print(f"Reconfiguring {option}...")
                task = vm.PowerOff()
                wait_for_task(vm.Reconfigure(spec))
                task = vm.PowerOn()

    
    except Exception as e:
        print("Failed to reconfigure selected machine:")
        print(e)
        print(traceback.format_exc())


def configClone(content, vmlist, option):
    
    # default value
    snapshotSpec = None
    
    name = input("Name for the new VM: ")

    vmfolder = None
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder

    locationSpec = vim.vm.RelocateSpec()

    # Snapshot to create a linked clone
    for machine in vmlist:
        if machine.name == option:
            vm = machine

    if not machine.summary.config.template:
        snapshotSpec = vm.snapshot.rootSnapshotList[len(vm.snapshot.rootSnapshotList) - 1].snapshot

    # the specifications for cloning the machine
    cloneSpec = vim.vm.CloneSpec(
        location=locationSpec,
        powerOn=True,
        snapshot=snapshotSpec,
        template=False
    )

    return vmfolder, name, cloneSpec


def cloneVM():
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

        option = input("\nWhich one would you like to clone? ")
        while option not in [vm.name for vm in vmlist]:
            option = input("Please enter a name from the list: ")

        if option == "vcenter":
            print("You should not clone vCenter.")
            return

        folder, name, spec = configClone(content, vmlist, option)

        for vm in vmlist:
            if vm.name == option:
                print(f"Cloning {option}...")
                vm.PowerOff()
                wait_for_task(vm.Clone(folder, name, spec))
                vm.PowerOn()
    
    except Exception as e:
        print("Failed to clone selected machine")
        print(e)
        print(traceback.format_exc())


def deleteVM():
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

        option = input("\nWhich one would you like to delete? ")
        while option not in [vm.name for vm in vmlist]:
            option = input("Please enter a name from the list: ")

        if option == "vcenter":
            print("You should not delete vCenter.")
            return

        for vm in vmlist:
            if vm.name == option:
                print(f"Deleting {option}...")
                vm.PowerOff()
                wait_for_task(vm.Destroy())
    
    except Exception as e:
        print("Failed to delete selected machine")
        print(e)

