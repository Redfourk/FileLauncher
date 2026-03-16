import psutil

# This netman is only for the CLI:

# Added Ethernet Compatibility. (#2) @3/6/26

def check_adapter_status():
    stats = psutil.net_if_stats()

    for name, info in stats.items():
        if "wi-fi" in name.lower() or "wireless" in name.lower():
            status = "Enabled/Connected" if info.isup else "Disconnected/Disabled"
            return f"{name} is {status}"
        if "ethernet" in name.lower() or "lan" in name.lower():
            status = "Enabled/Connected" if info.isup else "Disconnected/Disabled"
            return f"{name} is {status}"
    return "No matching adapter found"

