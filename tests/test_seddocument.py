import pytest
import json
import dataclasses
from pydantic.tools import parse_obj_as

from sed_converter.Sed.SedDocument import SedDocument, Metadata, Declarations


def test_create():
    metadata = Metadata(name="test", level=1, version=1, Ontologies=["sed"])
    doc = SedDocument(
        Metadata=metadata,
        Dependencies=[],
        Declarations=Declarations(Constants=[], Variables=[]),
        Inputs=[],
        Outputs=[],
        Actions=[],
    )

    assert doc is not None
    model_json = doc.model_dump_json()
    assert (
        model_json == '{"Metadata":{"name":"test","level":1,"version":1,"Ontologies":["sed"]},'
        '"Dependencies":[],'
        '"Declarations":{"Constants":[],"Variables":[]},'
        '"Actions":[],'
        '"Inputs":[],'
        '"Outputs":[]}'
    )

    # doc2: SedDocument = SedDocument.__pydantic_model__.parse_raw(model_json)
    # assert doc2 == doc
