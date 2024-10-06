import vcenterConnect as vcenter
import json


def vcenterInfo():
    print("\n")
    print("=====================================")
    print("             About Info              ")
    print("=====================================\n")
    print(vcenter.si.content.about)


def sessionInfo():

    print("\n")
    print("=====================================")
    print("            Session Info             ")
    print("=====================================\n")

    content = vcenter.si.RetrieveContent()
    session = content.sessionManager.currentSession
    print(f"Username: {session.userName:>27}")
    with open("vcenterConf.json", "r") as file:
        data = json.load(file)
        hostname = data["vCenter"]["vCenterHost"]
        print(f"Hostname: {hostname:>27}")
    print(f"IP Address: {session.ipAddress:>25}")


def vmInfo():
    filter = input("Filter by name [none]: ")
    
    content = vcenter.si.RetrieveContent()
    # get all of items in inventory
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity

            for vm in vmlist:
                # making sure the object we're accessing is a VM and not a folder or something else
                if('VirtualMachine' in str(type(vm))):
                    summary = vm.summary
                    if filter in summary.config.name and summary.config.template != True:
                        print("\n")
                        print("=====================================")
                        print("               VM Info               ")
                        print("=====================================\n")
                        print(f"VM Name: {summary.config.name:>28}")
                        print(f"IP Address: {summary.guest.ipAddress:>25}")
                        print(f"Power State: {summary.runtime.powerState:>24}")
                        print(f"Number of CPUs: {summary.config.numCpu:>21}")
                        print(f"Memory: {int(summary.config.memorySizeMB)/1000:>27.0f}GB")


