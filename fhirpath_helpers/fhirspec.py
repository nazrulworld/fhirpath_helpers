# -*- coding: utf-8 -*-
import zipfile
import shutil
import pathlib
import tempfile
import os
import io
import json

__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


def build_minified_json(
    archive_file: pathlib.Path,
    version_info: pathlib.Path,
    destination_dir: pathlib.Path,
):
    """ """
    tmp_dir = tempfile.mkdtemp()
    if not destination_dir.exists():
        destination_dir.mkdir(parents=True)

    with zipfile.ZipFile(str(archive_file), "r") as zip_ref:
        zip_ref.extractall(tmp_dir)

    shutil.copyfile(str(version_info), str(destination_dir / "version.info"))
    search_param_file = "search-parameters.json"

    shutil.copyfile(
        os.path.join(tmp_dir, search_param_file), str(destination_dir / search_param_file)
    )

    for filename in ["profiles-types.json", "profiles-resources.json"]:
        new_bundle = dict(entry=list())

        with io.open(os.path.join(tmp_dir, filename), "r", encoding="utf-8") as fp:
            bundle_json = json.loads(fp.read())

        for entry in bundle_json["entry"]:
            resource = entry["resource"].copy()
            if "StructureDefinition" == resource["resourceType"]:
                del resource["text"]
                del resource["snapshot"]
                new_bundle["entry"].append(
                    {"fullUrl": entry.get("fullUrl"), "resource": resource}
                )
        del bundle_json["entry"]
        new_bundle.update(bundle_json)
        newfilename = filename.split(".")[:-1] + ["min", "json"]
        with open(str(destination_dir / ".".join(newfilename)), "w", encoding="utf-8") as fp:
            json.dump(new_bundle, fp, indent=2)

    # Work with valuset
    with io.open(os.path.join(tmp_dir, "valuesets.json"), "r", encoding="utf-8") as fp:
        new_bundle = dict(entry=list())
        bundle_json = json.loads(fp.read())
        for entry in bundle_json["entry"]:
            resource = entry["resource"].copy()
            if "ValueSet" == resource["resourceType"]:
                assert "url" in resource

            elif "CodeSystem" == resource["resourceType"]:
                assert "url" in resource
                if "content" not in resource and "concept" not in resource:
                    continue
            else:
                continue

            del resource["text"]
            new_bundle["entry"].append(
                {"fullUrl": entry.get("fullUrl"), "resource": resource}
            )
        del bundle_json["entry"]
        new_bundle.update(bundle_json)
        with open(str(destination_dir / "valuesets.min.json"), "w", encoding="utf-8") as fp:
            json.dump(new_bundle, fp, indent=2)

    shutil.rmtree(tmp_dir)
