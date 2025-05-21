# tagster/core.py

import os
from PIL import Image
import pandas as pd
from clip_interrogator import Config, Interrogator


def tag_images(path):
    """
    Tags images in the given path using CLIP Interrogator.

    Args:
        path (str): Path to an image file or directory containing images.

    Returns:
        list: A list of dictionaries with 'image' and 'tags' keys.
    """
    ci = Interrogator(Config())
    results = []

    def tag_image(fp):
        img = Image.open(fp).convert("RGB")
        prompt = ci.interrogate(img)
        results.append({"image": fp, "tags": prompt})

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    tag_image(os.path.join(root, f))
    else:
        tag_image(path)

    return results


def save_results(results, output, fmt="csv"):
    """
    Saves the tagging results to a file.

    Args:
        results (list): List of tagging results.
        output (str): Output file path.
        fmt (str): Format to save the results ('csv' or 'json').
    """
    df = pd.DataFrame(results)
    if fmt == "json":
        df.to_json(output, orient="records", lines=True)
    else:
        df.to_csv(output, index=False)
