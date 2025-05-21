def test_tag_single_image():
    img = "tests/assets/test.jpg"
    result = subprocess.run(["python", "src/cli.py", img], capture_output=True, text=True)
    assert "→" in result.stdout

