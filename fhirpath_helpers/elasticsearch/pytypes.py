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
from copy import deepcopy

__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"
date_pattern = "-?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1]))?)?"
datetime_pattern = "-?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1])(T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\\.[0-9]+)?(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?"  # noqa
Boolean = {"type": "boolean", "store": False}
Float = {"type": "float", "store": False}
Integer = {"type": "integer", "store": False}
Long = {"type": "long", "store": False}
Token = {
    "type": "keyword",
    "index": True,
    "store": False,
    "normalizer": "fhir_normalizer",
    "fields": {"raw": {"type": "keyword"}},
}
ReferenceToken = {
    "type": "text",
    "index": True,
    "store": False,
    "analyzer": "fhir_reference_analyzer",
}
PathToken = {"type": "text", "index": True, "store": False, "analyzer": "path_analyzer"}
Text = {
    "type": "text",
    "index": True,
    "store": False,
    "analyzer": "standard",
    #    "index_prefixes": {"min_chars": 1, "max_chars": 10},
}
SearchableText = {"type": "text", "index": True, "analyzer": "standard", "store": False}

Date = {
    "type": "date",
    "format": "date_time_no_millis||date_optional_time",
    "store": False,
}
Time = {"type": "date", "format": "basic_t_time_no_millis", "store": False}

Attachment = {"properties": {"url": Token, "language": Token, "title": Text, "creation": Date}}

Coding = {"properties": {"system": Token, "code": Token, "display": Token}}

CodeableConcept = {
    "properties": {"text": Text, "coding": {"type": "nested", "properties": Coding["properties"]}}
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

Quantity = {"properties": {"value": Float, "code": Token, "system": Token, "unit": Token}}

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
    "properties": {"period": Period, "rank": Integer, "system": Token, "use": Token, "value": Text}
}


ContactDetail = {"properties": {"name": Token, "telecom": {**ContactPoint, "type": "nested"}}}

Annotation = {
    "properties": {"authorReference": Reference, "authorString": Text, "text": Text, "time": Date}
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

RelatedArtifact_STU3 = {"properties": {"type": Token, "url": Token, "resource": Reference}}


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
    "properties": {"contentType": Token, "when": Date, "whoReference": Reference, "whoUri": Token}
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

# Common
Id = Token
Meta = {
    "properties": {
        "versionId": Token,
        "lastUpdated": Date,
        "profile": Token,
        "tag": {**Coding, "type": "nested"},
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

fhir_data_types_maps = {
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
    "Money": Money,
    "Duration": Duration,
    "Range": Range,
    "Ratio": Ratio,
    "Period": Period,
    "Identifier": Identifier,
    "HumanName": HumanName,
    "Address": Address,
    "ContactPoint": ContactPoint,
    "Timing": Timing,
    "Dosage": Dosage,
    "Meta": Meta,
    "Annotation": Annotation,
    "ContactDetail": ContactDetail,
    "Age": Age,
    "Reference": Reference,
    "RelatedArtifact": RelatedArtifact,
    "Signature": Signature,
    "Population": Population,
    "Narrative": Narrative,
    "Expression": Expression,
}
fhir_data_types_maps_STU3 = deepcopy(fhir_data_types_maps)
fhir_data_types_maps_STU3.update(
    {
        "Dosage": Dosage_STU3,
        "Money": Money_STU3,
        "RelatedArtifact": RelatedArtifact_STU3,
        "Signature": Signature_STU3,
    }
)
