#!/usr/bin/env python

"""Tests for `fhirpath_helpers` package."""
import pytest


from click.testing import CliRunner

from fhirpath_helpers import fhirpath_helpers
from fhirpath_helpers import cli
from fhirpath.fhirspec import FHIRSearchSpecFactory
from fhirpath.fhirspec import FhirSpecFactory
from fhirpath.enums import FHIR_VERSION
from fhirpath_helpers.elasticsearch.mapping import generate_mappings

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_fhir_spec():
    """ """
    search_spec = FHIRSearchSpecFactory.from_release(FHIR_VERSION.R4.value)
    resources_elements = generate_mappings()
    pytest.set_trace()
    """
    pat.elements[0].represents_class
True
(Pdb) pat.elements[1].represents_class
False
(Pdb) pat.elements[2].represents_class
False
'Patient.multipleBirth[x]'>>>resources_elements["Patient"][10].definition.types
(Pdb) resources_elements["Patient"][10].definition.types[0]
<fhirpath.fhirspec.spec.FHIRElementType object at 0x10e43b2d0>
(Pdb) dir(resources_elements["Patient"][10].definition.types[0])
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'code', 'parse_from', 'profile']
(Pdb) resources_elements["Patient"][10].definition.types[0].code
'boolean'
(Pdb) resources_elements["Patient"][10].definition.types[1].code
'integer'
(Pdb)

    """


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'fhirpath_helpers.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
