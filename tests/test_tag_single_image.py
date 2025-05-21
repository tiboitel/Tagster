# tests/test_tag_single_image.py
import subprocess

def test_tag_single_image():
    img = "tests/assets/test.jpg"
    result = subprocess.run(["python", "src/tagster/cli.py", img], capture_output=True, text=True)
    assert "→" in result.stdout

