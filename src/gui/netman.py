import psutil

def check_adapter_status():
    stats = psutil.net_if_stats()
    for name, info in stats.items():
        if "Wi-Fi" in name or "Wireless" in name:
            if info.isup:
                return f"{name} is Enabled and Connected"
            else:
                return f"{name} is Disconnected/Disabled"
    return "No Wi-Fi adapter found"
