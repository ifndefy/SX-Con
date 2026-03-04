from pathlib import Path

def get_login_logo_path():
    path = Path(__file__).parent / 'sxc_logo.png'
    return str(path)

def get_window_logo_path():
    path = Path(__file__).parent / 'sxc_window_logo.png'
    return str(path)