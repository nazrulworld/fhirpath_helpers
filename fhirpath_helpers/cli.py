"""Console script for fhirpath_helpers."""
import sys
import click
import os
import pathlib
from fhirpath.enums import FHIR_VERSION
import hashlib
import shutil
from .elasticsearch.mapping import make_and_write_es_mappings
from .helpers import download
from .helpers import resolve_path
from .fhirspec import build_minified_json

BASE_PATH = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
CACHE_DIR = BASE_PATH / ".cache"
all_colors = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
)


@click.group()
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


@main.command()
@click.option(
    "--release",
    "-r",
    required=True,
    type=click.Choice(["STU3", "R4"], case_sensitive=True),
)
@click.option(
    "--version",
    "-v",
    required=True,
    type=click.Choice(["3.0.1", "3.0.2", "4.0.0", "4.0.1"], case_sensitive=True),
)
@click.option("--output-dir", "-o", required=True, type=click.STRING)
@click.option("--no-cache", "-c", is_flag=True, default=False)
def fhirspec_build_minified_static_json(
    release: str, version: str, output_dir: str, no_cache: bool
):
    """ """
    if release == "R4" and version not in ("4.0.1", "4.0.0"):
        sys.stderr.write(f"Invalid version {version} has been provided for release {release}\n")
        return 1
    if release == "STU3" and version not in ("3.0.1", "3.0.2"):
        sys.stderr.write(f"Invalid version {version} has been provided for release {release}\n")
        return 1
    use_cache = no_cache is False
    cache_dir = CACHE_DIR / "spec"
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    base_url = "https://github.com/nazrulworld/fhir-parser/raw/master/archives/HL7/FHIR"
    output_dir = resolve_path(output_dir)
    if not output_dir.name == version:
        if not output_dir.parent.name == release:
            output_dir = output_dir / release
        output_dir = output_dir / version

    version_info_url = f"{base_url}/{release}/{version}-version.info"
    version_info_hash = hashlib.md5(version_info_url.encode()).digest().hex()
    version_info_file = cache_dir / version_info_hash

    definition_achieve_url = f"{base_url}/{release}/{version}-definitions.json.zip"
    definition_achieve_hash = hashlib.md5(definition_achieve_url.encode()).digest().hex()
    definition_achieve_file = cache_dir / definition_achieve_hash

    if use_cache is False or not version_info_file.exists():
        filename = download(version_info_url)
        shutil.copyfile(filename, version_info_file)
        shutil.rmtree(filename.parent)

    if use_cache is False or not definition_achieve_file.exists():
        filename = download(definition_achieve_url)
        shutil.copyfile(filename, definition_achieve_file)
        shutil.rmtree(filename.parent)

    build_minified_json(
        archive_file=definition_achieve_file,
        version_info=version_info_file,
        destination_dir=output_dir,
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
