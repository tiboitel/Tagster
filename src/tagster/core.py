# tagster/core.py

import os
from PIL import Image
import pandas as pd
from clip_interrogator import Config, Interrogator
from concurrent.futures import ThreadPoolExecutor, as_completed
import torch

def tag_images_in_batch(ci, image_files):
    """
    Tags a batch of images using CLIP Interrogator.

    Args:
        ci (Interrogator): CLIP Interrogator instance.
        image_files (list): List of file paths to the images.

    Returns:
        list: A list of dictionaries with 'image' and 'tags' keys.
    """
    results = []
    for fp in image_files:
        img = Image.open(fp).convert("RGB")
        prompt = ci.interrogate(img)
        results.append({"image": fp, "tags": prompt})
    return results

def tag_images(path, batch_size=8):
    """
    Tags images in the given path using CLIP Interrogator.

    Args:
        path (str): Path to an image file or directory containing images.
        batch_size (int): Number of images to process in each batch.

    Returns:
        list: A list of dictionaries with 'image' and 'tags' keys.
    """
    ci = Interrogator(Config())
    results = []

    image_files = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    image_files.append(os.path.join(root, f))
    else:
        image_files.append(path)

    def process_batch(batch):
        return tag_images_in_batch(ci, batch)

    with ThreadPoolExecutor() as executor:
        future_to_batch = {}
        for i in range(0, len(image_files), batch_size):
            batch = image_files[i:i + batch_size]
            future = executor.submit(process_batch, batch)
            future_to_batch[future] = batch

        for future in as_completed(future_to_batch):
            results.extend(future.result())

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

