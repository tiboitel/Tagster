import os
import sys
import json
import click
import pandas as pd
from PIL import Image
from clip_interrogator import Config, Interrogator

@click.command(context_settings=dict(help_option_names=["-h","--help"]))
@click.argument("path", type=click.Path(exists=True))
@click.option("-o","--output", type=click.Path(), help="CSV or JSON output file")
@click.option("--format", "fmt", type=click.Choice(["csv","json"]), default="csv")
def main(path, output, fmt):
    """
    Auto-tag images or directories for LoRA training.
    """
    # initialize once
    ci = Interrogator(Config())
    results = []

    def tag_image(fp):
        img = Image.open(fp).convert("RGB")
        prompt = ci.interrogate(img)
        click.echo(f"{os.path.basename(fp)} → {prompt}")
        results.append({"image": fp, "tags": prompt})

    if os.path.isdir(path):
        for root,_,files in os.walk(path):
            for f in files:
                if f.lower().endswith((".jpg",".jpeg",".png",".webp")):
                    tag_image(os.path.join(root, f))
    else:
        tag_image(path)

    if output:
        df = pd.DataFrame(results)
        if fmt == "json":
            df.to_json(output, orient="records", lines=True)
        else:
            df.to_csv(output, index=False)
        click.echo(f"✨ Saved results to {output}")

if __name__=="__main__":
    main()

