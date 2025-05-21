# tagster/cli.py

import click
from tagster.core import tag_images, save_results


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(),
              help="CSV or JSON output file")
@click.option("--format", "fmt", type=click.Choice(["csv", "json"]),
              default="csv")
def main(path, output, fmt):
    """
    Auto-tag images or directories for LoRA training.
    """
    results = tag_images(path)
    for item in results:
        click.echo(f"{item['image']} → {item['tags']}")

    if output:
        save_results(results, output, fmt)
        click.echo(f"✨ Saved results to {output}")


if __name__ == "__main__":
    main()
