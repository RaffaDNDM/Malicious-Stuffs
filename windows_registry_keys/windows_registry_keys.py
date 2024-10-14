#######################
# @author: RaffaDNDM
# @date:   2022-09-11
#######################

import winreg
from contextlib import suppress
import itertools

LINE = '__________________________________________________'

KEY_TYPES = {   'Windows SYSTEM info': {
                    'Version': (winreg.HKEY_LOCAL_MACHINE, [r'SOFTWARE\Microsoft\Windows NT\CurrentVersion',]),
                    'Hostname': (winreg.HKEY_LOCAL_MACHINE, [r'SYSTEM\ControlSet001\Control\ComputerName\ComputerName',]),
                    'Timezone': (winreg.HKEY_LOCAL_MACHINE, ['SYSTEM\\ControlSet001\\Control\\TimeZoneInformation',]),
                    'Last Access Time': (winreg.HKEY_LOCAL_MACHINE, ['SYSTEM\\ControlSet001\\Control\\FileSYSTEM',]),
                    'Shutdown Time': (winreg.HKEY_LOCAL_MACHINE, ['SYSTEM\\ControlSet001\\Control\\Windows',]),
                    #'Network Information': (winreg.HKEY_LOCAL_MACHINE, ['SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged', 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Managed', 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Nla\\Cache', 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Profiles']),
                    'Shared Folders': (winreg.HKEY_LOCAL_MACHINE, ['SYSTEM\\ControlSet001\\Services\\LanmanServer\\Shares',]),
                    #'Autostart programs': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run','NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce','SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Runonce','SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run','SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run']),
                    'Explorer searches': (winreg.HKEY_CURRENT_USER, ['SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\WordwheelQuery',]),
                    'Typed Paths': (winreg.HKEY_CURRENT_USER, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths',]),
                    #'Recent Docs': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs',]),
                    'MRUs': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedMRU', 'NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LasVisitedPidlMRU', 'NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\Op enSaveMRU', 'NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\Op enSavePidlMRU']),
                    #'Last Run Commands': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU', 'NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Policies\\RunMR']),
                    'Last Run Commands': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU', ])
                },
              
                'Shellbags': {
                    'Explorer Access': (winreg.HKEY_LOCAL_MACHINE, ['USRCLASS.DAT\\Local Settings\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags', 'USRCLASS.DAT\\Local Settings\\SOFTWARE\\Microsoft\\Windows\\Shell\\BagMRU']),
                    'Desktop Access': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\Shell\\BagMRU', 'NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags'])
                },

                'USB Information': {
                    'Device information': (winreg.HKEY_LOCAL_MACHINE, ['HKLM\\SYSTEM\\ControlSet001\\Enum\\USBSTOR',]),
                    'User that used the device': (winreg.HKEY_LOCAL_MACHINE, ['NTUSER.DAT\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Mountpoints2',]),
                    'Last mounted': (winreg.HKEY_LOCAL_MACHINE, ['SYSTEM\\MoutedDevices',]),
                    'Volume Serial Number': (winreg.HKEY_LOCAL_MACHINE, ['SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\EMDMgmt',])
                }
}

def get_reg(key_info, name=None):
    try:
        key_type, registry_paths = key_info
        subkeys={}
        
        for reg_path in registry_paths:
            with winreg.OpenKey(key_type, reg_path, 0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ)) as registry_key:
                if name:
                    value, regtype = winreg.QueryValueEx(registry_key, name)
                    subkeys[name] = value

                else:
                    for i in range(winreg.QueryInfoKey(registry_key)[1]):
                        try:
                            key_value = winreg.EnumValue(registry_key,i)
                            if key_value[0]!='':
                                subkeys[key_value[0]] = key_value[1]
                        except Exception as e:
                            pass
        
        return subkeys

    except WindowsError:
        return None
    
def menu():
    global KEY_TYPES
    global LINE
    count=1

    print(f'\nSelect which information do you want to print:')
    print(LINE)
    for k in KEY_TYPES:
        print(f'{count}) {k}')

        for x in KEY_TYPES[k]:
            print(f'\t- {x}')

        count+=1
        
        if count!=(len(KEY_TYPES)+1):
            print('')

    print(LINE)

def submenu(key_type):
    print('\n'+key_type.upper().center(len(LINE)))
    print(LINE)

    count = 1
    for key_subtype in KEY_TYPES[key_type]:
        print(f'{count}) {key_subtype}')
        count+=1

    print(f'\n{count}) All information')
    print(f'0) Back to main menu')
    print(LINE)

def print_keys(subkeys, key_subtype):
    print('\n'+key_subtype.upper().center(len(LINE)))
    print(LINE)
    
    for k in subkeys:
        print(f'{k}: {subkeys[k]}')
    
    print(LINE, end='\n\n')

def main():
    global KEY_TYPES

    menu_choice = -1

    while menu_choice<0 or menu_choice>len(KEY_TYPES):
        menu()

        try:
            menu_choice = int(input())    
        
        except ValueError:
            menu_choice=-1
            continue
    
        if menu_choice==0:
            break

        elif menu_choice>0 and menu_choice<=len(KEY_TYPES):
            key_type=list(KEY_TYPES.keys())[menu_choice-1]
            submenu(key_type)
            submenu_choice = -1

            while submenu_choice<0 or submenu_choice>len(KEY_TYPES[key_type]):
                try:
                    submenu_choice = int(input())
                
                except ValueError:
                    submenu_choice=-1
                    continue

                if submenu_choice>0 and submenu_choice<=len(KEY_TYPES[key_type]):
                    #Print the keys for the selected subtype
                    key_subtype = list(KEY_TYPES[key_type].keys())[submenu_choice-1]
                    #print(key_subtype)
                    subkeys=get_reg(KEY_TYPES[key_type][key_subtype])
                    #print(KEY_TYPES[key_type][key_subtype])

                    print_keys(subkeys, key_subtype)

                elif submenu_choice==(len(KEY_TYPES[key_type])+1):
                    #Print the keys for all subtypes
                    for key_subtype in KEY_TYPES[key_type]:
                        subkeys=get_reg(KEY_TYPES[key_type][key_subtype])

                        print_keys(subkeys, key_subtype)

                        


        menu_choice=-1


if __name__=='__main__':
    main()