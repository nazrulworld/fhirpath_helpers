# -*- coding: utf-8 -*-
# @Date    : 2020-02-15 17:48:31
# @Author  : Md Nazrul Islam <email2nazrul@gmail.com>
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
"""Compound mapping types:
Based on https://www.hl7.org/fhir/R4/datatypes.html, for other version
need to make compatibility
"""
from fhirpath.enums import FHIR_VERSION

__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


def fhir_types_mapping(
    fhir_release: str, reference_analyzer=None, token_normalizer=None,
):
    Boolean = {"type": "boolean", "store": False}
    Float = {"type": "float", "store": False}
    Integer = {"type": "integer", "store": False}
    Token = {
        "type": "keyword",
        "index": True,
        "store": False,
        "fields": {
            # index the raw text without normalization for exact matching
            "raw": {"type": "keyword"}
        },
    }
    if token_normalizer:
        Token.update({"normalizer": token_normalizer})

    ReferenceToken = {
        "type": "text",
        "index": True,
        "store": False,
    }
    if reference_analyzer:
        ReferenceToken.update({"analyzer": reference_analyzer})

    Text = {
        "type": "keyword",
        "index": True,
        "store": False,
        "fields": {
            # re-index the raw text without normalization for exact matching
            "raw": {"type": "keyword"},
        },
    }

    SearchableText = {
        "type": "text",
        "index": True,
        "analyzer": "standard",
        "store": False,
    }

    Date = {
        "type": "date",
        "format": "date_time_no_millis||date_optional_time",
        "store": False,
    }
    Time = {"type": "date", "format": "basic_t_time_no_millis", "store": False}

    Attachment = {
        "properties": {"url": Token, "language": Token, "title": Text, "creation": Date}
    }

    Coding = {"properties": {"system": Token, "code": Token, "display": Token}}

    CodeableConcept = {
        "properties": {
            "text": Text,
            "coding": {"type": "nested", "properties": Coding["properties"]},
        }
    }

    Period = {"properties": {"start": Date, "end": Date}}
    Timing = {"properties": {"event": Date, "code": CodeableConcept}}

    Identifier = {
        "properties": {
            "use": Token,
            "system": Token,
            "value": Token,
            "type": {"properties": {"text": Text}},
        }
    }

    Reference = {"properties": {"reference": ReferenceToken, "identifier": Identifier}}

    Quantity = {
        "properties": {"value": Float, "code": Token, "system": Token, "unit": Token}
    }

    Money = {"properties": {"value": Float, "currency": Token}}
    Money_STU3 = Quantity
    Range = {"properties": {"high": Quantity, "low": Quantity}}
    Ratio = {"properties": {"numerator": Quantity, "denominator": Quantity}}

    Age = Quantity
    Address = {
        "properties": {
            "city": Token,
            "country": Token,
            "postalCode": Token,
            "state": Token,
            "use": Token,
        }
    }

    HumanName = {
        "properties": {
            "family": Token,
            "text": Text,
            "prefix": Token,
            "given": Token,
            "use": Token,
            "period": Period,
        },
    }

    Duration = Quantity

    ContactPoint = {
        "properties": {
            "period": Period,
            "rank": Integer,
            "system": Token,
            "use": Token,
            "value": Text,
        }
    }

    ContactDetail = {
        "properties": {"name": Token, "telecom": {**ContactPoint, "type": "nested"}}
    }

    Annotation = {
        "properties": {
            "authorReference": Reference,
            "authorString": Text,
            "text": Text,
            "time": Date,
        }
    }

    Dosage = {
        "properties": {
            "asNeededBoolean": Boolean,
            "asNeededCodeableConcept": CodeableConcept,
            "site": CodeableConcept,
            "text": Text,
            "timing": Timing,
            "patientInstruction": Text,
            "doseAndRate": {
                "properties": {
                    "doseQuantity": Quantity,
                    "type": CodeableConcept,
                    "rateRatio": Ratio,
                    "rateRange": Range,
                    "rateQuantity": Quantity,
                }
            },
            "maxDosePerPeriod": Ratio,
            "maxDosePerAdministration": Quantity,
            "maxDosePerLifetime": Quantity,
        }
    }
    Dosage_STU3 = {
        "properties": {
            "asNeededBoolean": Boolean,
            "asNeededCodeableConcept": CodeableConcept,
            "doseQuantity": Quantity,
            "doseRange": Range,
            "site": CodeableConcept,
            "text": Text,
            "timing": Timing,
        }
    }

    RelatedArtifact = {
        "properties": {
            "type": Token,
            "url": Token,
            "resource": Reference,
            "label": Text,
            "display": Text,
        }
    }

    RelatedArtifact_STU3 = {
        "properties": {"type": Token, "url": Token, "resource": Reference}
    }

    Signature = {
        "properties": {
            "type": Coding,
            "when": Date,
            "who": Reference,
            "targetFormat": Token,
            "sigFormat": Token,
            "onBehalfOf": Reference,
        }
    }

    Signature_STU3 = {
        "properties": {
            "contentType": Token,
            "when": Date,
            "whoReference": Reference,
            "whoUri": Token,
        }
    }
    Population = {
        "properties": {
            "ageRange": Range,
            "ageCodeableConcept": CodeableConcept,
            "gender": CodeableConcept,
            "race": CodeableConcept,
            "physiologicalCondition": CodeableConcept,
        }
    }

    Meta = {
        "properties": {
            "versionId": Token,
            "lastUpdated": Date,
            "profile": Token,
            "tag": {**Coding, "type": "nested", "include_in_root": True},
        }
    }

    Expression = {
        "properties": {
            "description": Token,
            "name": Token,
            "language": Token,
            "expression": Token,
            "reference": Token,
        }
    }

    Narrative = {"properties": {"status": Token, "div": SearchableText}}

    Count = Quantity
    Distance = Quantity

    return {
        "boolean": Boolean,
        "base64Binary": Token,
        "integer": Integer,
        "string": Text,
        "decimal": Float,
        "uri": Token,
        "url": Token,
        "canonical": Token,
        "instant": Date,
        "date": Date,
        "dateTime": Date,
        "time": Time,
        "code": Token,
        "oid": Token,
        "id": Token,
        "unsignedInt": Integer,
        "positiveInt": Integer,
        "uuid": Token,
        "Attachment": Attachment,
        "Coding": Coding,
        "CodeableConcept": CodeableConcept,
        "Quantity": Quantity,
        "Distance": Distance,
        "Count": Count,
        "Money": {FHIR_VERSION.STU3.name: Money_STU3, FHIR_VERSION.R4.name: Money}[
            fhir_release
        ],
        "Duration": Duration,
        "Range": Range,
        "Ratio": Ratio,
        "Period": Period,
        "Identifier": Identifier,
        "HumanName": HumanName,
        "Address": Address,
        "ContactPoint": ContactPoint,
        "Timing": Timing,
        "Dosage": {FHIR_VERSION.STU3.name: Dosage_STU3, FHIR_VERSION.R4.name: Dosage}[
            fhir_release
        ],
        "Meta": Meta,
        "Annotation": Annotation,
        "ContactDetail": ContactDetail,
        "Age": Age,
        "Reference": Reference,
        "RelatedArtifact": {
            FHIR_VERSION.STU3.name: RelatedArtifact_STU3,
            FHIR_VERSION.R4.name: RelatedArtifact,
        }[fhir_release],
        "Signature": {
            FHIR_VERSION.STU3.name: Signature_STU3,
            FHIR_VERSION.R4.name: Signature,
        }[fhir_release],
        "Population": Population,
        "Narrative": Narrative,
        "Expression": Expression,
    }
