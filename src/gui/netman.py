import platform
import psutil

# Added Ethernet Compatibility. (#2) @3/6/26
# Added Cross-Platform Compatability. @4/12/26

def check_adapter_status():
    system_os = platform.system()
    stats = psutil.net_if_stats()
    for name, info in stats.items():
        lname = name.lower()
        status = "Enabled/Connected" if info.isup else "Disconnected/Disabled"
        if system_os == "Windows":
            if any(word in lname for word in ["wi-fi", "wireless", "ethernet", "lan"]):
                return f"{name} is {status}"
        elif system_os == "Linux":
            if lname.startswith(('w', 'e')) and name != "lo":  # ignore 'lo' (loopback)
                if lname.startswith('w') and name != "lo":
                    return f"Wireless Network is {status}"
                elif lname.startswith('e') and name != "lo":
                    return f"Wired network is {status}"
                return f"{name} is {status}"
    return "No matching adapter found"
