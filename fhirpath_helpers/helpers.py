"""Main module."""
import requests
import pathlib
import io
import sys
import shutil
import tempfile
import os
from urllib.parse import urlparse

__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


def resolve_path(string_path: str, parent: pathlib.PurePath = None):
    """ """
    if os.path.isabs(string_path):
        return pathlib.Path(string_path)
    elif string_path.startswith("~"):
        return pathlib.Path(os.path.expanduser(string_path))

    if parent is None:
        parent = pathlib.Path(os.getcwd())
    if string_path == ".":
        return parent

    me = parent
    for part in string_path.split(os.sep):
        if not part:
            continue
        if part == ".":
            continue
        elif part == "..":
            me = me.parent
        else:
            me = me / part
    return me


def filename_from_url(url: str):
    """ """
    return pathlib.Path(urlparse(url).path).name


def download(url: str, output_path: pathlib.Path = None):
    """ """
    if output_path is None:
        output_path = pathlib.Path(tempfile.mkdtemp())

    def _get_file_name(resp):
        """ """
        parts = resp.headers.get("Content-Disposition", "").split(";")
        if len(parts) == 1 and parts[0] == "":
            return filename_from_url(url)

        for part in parts:
            part = part.strip()
            if not part:
                continue
            if part.lower().startswith("filename"):
                filename = part.split("=", 1)[1]
                return filename.strip()
        return filename_from_url(url)

    try:
        sys.stdout.write(f"### helpers.download> Start downloading file from {url}\n")
        with requests.get(
            url, stream=True, allow_redirects=True, verify=True
        ) as response:
            assert response.status_code == 200
            if output_path.is_dir():
                if not output_path.exists():
                    output_path.mkdir()
                filename = _get_file_name(response)
                output_path = output_path / filename
            write_mode = (
                response.headers.get("Content-Type").lower().startswith("text/")
                and "w"
                or "wb"
            )
            with io.open(str(output_path), write_mode) as fp:
                if write_mode == "w":
                    fp.write(response.text)
                else:
                    shutil.copyfileobj(response.raw, fp)
            sys.stdout.write(
                f"### helpers.download> download completed within {response.elapsed} sec.\n"
            )
            sys.stdout.write(
                f"### helpers.download> File has been written to {output_path}.\n"
            )
    except requests.exceptions.HTTPError as exc:
        sys.stderr.write(str(exc) + "\n")
        return
    return output_path
