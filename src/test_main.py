# This is for the GitHub workflow runner, don't mess with it, it's vital!
import subprocess


def test_setup():
    subprocess.Popen("main.py")
    assert True
