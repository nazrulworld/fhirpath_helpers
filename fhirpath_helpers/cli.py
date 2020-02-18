"""Console script for fhirpath_helpers."""
import sys
import click
import os
import pathlib
from fhirpath.enums import FHIR_VERSION
from .elasticsearch.mapping import make_and_write_es_mappings

all_colors = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
             'cyan', 'white', 'bright_black', 'bright_red', \
             'bright_green', 'bright_yellow', 'bright_blue', \
             'bright_magenta', 'bright_cyan', 'bright_white'


@click.group(name="es")
@click.pass_context
def main(ctx, args=None):
    """Console script for fhirpath_helpers."""


@main.command()
@click.option("--fhir-release", "-R", type=click.STRING)
@click.argument("output-dir")
def es_generate_mapping(fhir_release, output_dir):
    """ """
    if output_dir.startswith("./"):
        output_dir = os.path.dirname(os.path.abspath(__file__)) + output_dir[1:]
    output_dir = pathlib.Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    if fhir_release:
        FHIR_VERSION[fhir_release]
    else:
        fhir_release = FHIR_VERSION.R4.value

    try:
        make_and_write_es_mappings(output_dir, fhir_release)
        return 0
    except Exception as exc:
        click.echo(str(exc), color=click.style("red", bold=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
