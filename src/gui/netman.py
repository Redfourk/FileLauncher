import psutil


def check_network_status():
    stats = psutil.net_if_stats()
    results = {"Ethernet": "Not Found", "Wi-Fi": "Not Found"}

    for name, info in stats.items():
        if any(keyword in name for keyword in ["Ethernet", "LAN", "eth", "en"]):
            status = "Connected" if info.isup else "Disconnected"
            results["Ethernet"] = f"{status} ({name})"
            results_string = results["Ethernet"]

        elif any(keyword in name for keyword in ["Wi-Fi", "Wireless", "wlan"]):
            status = "Connected" if info.isup else "Disconnected"
            results["Wi-Fi"] = f"{status} ({name})"
            results_string = results["Wi-Fi"]

    return results_string


# Example Usage
status = check_network_status()
print(f"Ethernet: " + status)
print(f"Wi-Fi: " + status)
