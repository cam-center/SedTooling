from sed_converter.declarations.declarations import Declarations
from sed_converter.metadata.metadata import Metadata
from sed_converter.sed.sed_document import SedDocument


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
