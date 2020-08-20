# _*_ coding: utf-8 _*_
from collections import defaultdict
from fhirpath.fhirspec import FhirSpecFactory
from fhirpath.enums import FHIR_VERSION
from .pytypes import fhir_data_types_maps
from .pytypes import fhir_data_types_maps_STU3
import datetime
import json
import logging
import click

__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"

ignored_datatype = [
    "markdown",
    "UsageContext",
    "TriggerDefinition",
    "DataRequirement",
    "ParameterDefinition",
    "MarketingStatus",
    "ProdCharacteristic",
    "SampledData",
    "Contributor",
    "ElementDefinition",
    "ProductShelfLife",
    "Resource",
    "Extension",
    "SubstanceAmount",
]


def generate_mappings(fhir_release=None):
    """ """
    fhir_release = fhir_release or FHIR_VERSION.R4.name

    fhir_spec = FhirSpecFactory.from_release(fhir_release)

    resources_elements = defaultdict()

    for definition_klass in fhir_spec.profiles.values():
        if definition_klass.name in ("Resource", "DomainResource"):
            # exceptional
            resources_elements[definition_klass.name] = definition_klass.elements
            continue
        if definition_klass.structure.subclass_of != "DomainResource":
            # we accept domain resource only
            continue

        resources_elements[definition_klass.name] = definition_klass.elements

    elements_paths = build_elements_paths(resources_elements)

    maps = dict()
    if fhir_release == "STU3":
        data_maps = fhir_data_types_maps_STU3
    else:
        data_maps = fhir_data_types_maps

    for resource, paths_def in elements_paths.items():
        maps[resource] = create_resource_mapping(paths_def, data_maps)
        maps[resource]["resourceType"] = data_maps["code"].copy()

    return maps


def build_elements_paths(resources_elements):
    """ """
    resources_elements_paths = defaultdict()
    default_paths = extract_elements_paths(resources_elements.pop("Resource"))
    default_domain_paths = extract_elements_paths(resources_elements.pop("DomainResource"))
    for resource, elements in resources_elements.items():
        paths = extract_elements_paths(elements)
        apply_default_paths(resource, default_paths, paths)
        apply_default_paths(resource, default_domain_paths, paths)
        resources_elements_paths[resource] = paths

    return resources_elements_paths


def extract_elements_paths(elements):
    """ """
    paths = list()

    for el in elements:
        if el.is_main_profile_element:
            continue
        if len(el.definition.types) == 0:
            continue

        if el.path.endswith("[x]"):
            assert len(el.definition.types) > 1
            for ty in el.definition.types:
                addon = ty.code[0].upper() + ty.code[1:]
                paths.append((el.path.replace("[x]", addon), ty.code, (el.n_max != "1")))
        else:
            paths.append((el.path, el.definition.types[0].code, (el.n_max != "1")))
    return paths


def apply_default_paths(resource, defaults, container):
    """ """
    for path_, code, multiple in defaults:
        parts = path_.split(".")
        _path = ".".join([resource] + list(parts[1:]))
        container.append((_path, code, multiple))


def add_mapping_meta(resource, mappings, fhir_release):
    """ """
    data = {
        "resourceType": resource,
        "meta": {"lastUpdated": datetime.datetime().ISO8601(), "versionId": fhir_release},
        "mapping": {"properties": mappings},
    }
    return data


def create_resource_mapping(elements_paths_def, fhir_data_types_maps):
    """ """
    mapped = dict()

    # this generator function iterates over the list of elements definitions and groups
    # children elements with their parents to reflect thbe nested resource structure.
    def iterate_elements():
        mapped_elements = list()
        for path, code, multiple in elements_paths_def:
            if path not in mapped_elements:
                children = [x for x in elements_paths_def if x[0].startswith(path) and x[0] != path]
                mapped_elements.extend([path, *[c[0] for c in children]])
                yield path, code, multiple, children

    for path, code, multiple, children in iterate_elements():
        name = path.split(".")[-1]
        try:
            map_ = fhir_data_types_maps[code].copy()
        except KeyError:
            # if the element is of type BackboneElement, it means that it has no external definition
            # and needs to be mapped dynamically based on its inline definition.
            if code == "BackboneElement":
                map_ = {
                    "type": "nested",
                    "properties": create_resource_mapping(children, fhir_data_types_maps),
                }
            elif code in ignored_datatype:
                logging.debug(f"{path} won't be indexed in elasticsearch: type {code} is ignored")
                continue
            else:
                logging.debug(f"{path} won't be indexed in elasticsearch: type {code} is unknown")
                raise

        if multiple and "type" not in map_:
            map_.update({"type": "nested"})

        mapped[name] = map_

    return mapped


def write_resource_mapping(output_dir, resource, mappings, fhir_release):
    """ """
    data = add_mapping_meta(resource, mappings, fhir_release)
    path_ = str(output_dir / "{0}.mapping.json".format(resource))
    with open(path_, "w") as fp:
        text = json.dumps(data, indent=2)
        fp.write(text)
    click.echo(f"Mapping File has been written to {path_}", color=click.style("green"))


def make_and_write_es_mappings(output_dir, fhir_release):
    """ """
    resources_mappings = generate_mappings(fhir_release)

    for resource, mappings in resources_mappings.items():
        write_resource_mapping(output_dir, resource, mappings, fhir_release)
    click.echo(
        f"Total {len(resources_mappings)} files have been written to {output_dir}",
        color=click.style("green"),
    )
