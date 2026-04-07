# Error Code Dictionary:

ERROR_CODES =  {
    "100": "General Connection Failure",
    "101": "GPO/Firewall Blocked Connection",
    "102": "Protocol Mismatch (Header Error)",
    "103": "Access Denied (Disk/Uploads Folder)",
    "104": "File Too Large for Target RAM"
}

def get_err(code):
    return f"Error {code}: {ERROR_CODES.get(str(code), 'Unknown')}"