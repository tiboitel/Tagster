# tests/test_cli.py
import subprocess

def test_help():
    result = subprocess.run(["python", "src/cli.py", "--help"], capture_output=True, text=True)
    assert "Usage" in result.stdout

