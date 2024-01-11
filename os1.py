import subprocess
import re
import numpy as np
# Get the command from the user
'''All Installed software’s list
Internet Speed
Screen resolvution
CPU model
No of core and threads of CPU
GPU model ( If exist )
RAM Size ( In GB )
Screen size ( like, 15 inch, 21 inch)
Wifi/Ethernet mac address
Public IP address
Windows version
'''


def getScreenResolution():
    result='wmic path WIn32_VideoController get CurrentHorizontalResolution,CurrentVerticalResolution'
    runCommand(result)
def getInstalledSoftwareNames():
    result='wmic product get name'
    runCommand(result) 
def getInternetSpeed():
    result='speedtest'
    runCommand(result)
def getCPUModel():
    result='wmic cpu get caption'
    runCommand(result)
def getCPUCoresAndThreads():
    result='wmic cpu get numberofcores,numberoflogicalprocessors'
    runCommand(result)
def getGPUModel():
    result='wmic path win32_videocontroller get caption'
    runCommand(result)
def getRAMSize():
    try:
        result = subprocess.run(['wmic', 'memorychip', 'get', 'capacity'], capture_output=True, text=True, check=True)
        capacities = result.stdout.strip().split('\n')[1:]
        total_ram = sum([int(capacity) for capacity in capacities if capacity.strip()])
        print(total_ram / (1024**3))  # Convert to GB)
    except subprocess.CalledProcessError as e:
        print(f"Error running wmic command: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
def get_screen_resolution():
    try:
        result = subprocess.run('wmic path WIn32_VideoController get CurrentHorizontalResolution,CurrentVerticalResolution', capture_output=True, text=True, check=True)
        match = re.search(r'(\d+)\s+(\d+)', result.stdout)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running wmic command: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
def getVersion():
    result='systeminfo'
    try:
        result = subprocess.run(result, capture_output=True, text=True, check=True)
        OS_match = re.search(r'OS Name[.\s:]+([a-zA-Z0-9 ]+)', result.stdout)
        version_match=re.search(r'OS Version[.\s:]+([a-zA-Z0-9 ./]+)', result.stdout)
        if OS_match and version_match:
            OS_name = OS_match.group()
            Version=version_match.group()
            print(OS_name)
            print(Version)
        else:
            print("version not found.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running ipconfig command: {e}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def calculateScreenSize(resolution, dpi=142):
    width, height = resolution
    diagonal_pixels = (width ** 2 + height ** 2) ** 0.5
    diagonal_inches = diagonal_pixels / dpi
    return diagonal_inches
def getWifiAddress():
    try:
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, check=True)
        mac_addresses_result = subprocess.run('getmac', capture_output=True, text=True, check=True)
        mac_addresses_lines = mac_addresses_result.stdout.strip().split('\n')
        mac_addresses_lines.pop(1)
        mac_array=np.array(mac_addresses_lines)
        ip_address_match = re.search(r'IPv4 Address[.\s:]+([0-9. ]+)', result.stdout)
        if ip_address_match and mac_addresses_lines is not None:
            ip_address=ip_address_match.group(1)
            print('ip address',ip_address)
            print(mac_array)
        else:
            print("Mac address or ip address not found.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running ipconfig or getmac command: {e}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
            
def runCommand(result):
    try:
        result = subprocess.run(result, shell=True, capture_output=True, text=True)

    # Print the command output
        print("Command Output:")
        print(result.stdout)

    # Print any error output
        if result.stderr:
            print("Error Output:")
            print(result.stderr)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

print('1.Internet Speed')
print('2. CPU model: ')
print('3. No of core and threads of CPU')
print('4. Screen Resolution')
print('5. GPU model')
print('6. RAM Size')
print('7. Screen size')
print('8. Wifi/Ethernet mac address and ip address')
print('9. Windows version')
choice=int(input('choose any one option:'))
if choice==1:
    getInternetSpeed()
elif choice==2:
    getCPUModel()
elif choice==3:
    getCPUCoresAndThreads()
elif choice==4:
    getScreenResolution()
elif choice==5:
    getGPUModel()
elif choice==6:
    getRAMSize()
elif choice==7:
    resolution = get_screen_resolution()
    
    if resolution is not None:
        screen_size = calculateScreenSize(resolution)
        print(f"Estimated Screen Size: {screen_size:.2f} inches")
    else:
        print("Unable to retrieve screen resolution.")
elif choice==8:
    getWifiAddress()
elif choice==9:
    getVersion()
    
