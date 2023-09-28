from sed_converter.actions.action import Action
from sed_converter.declarations.constants.constant import Constant
from sed_converter.declarations.declarations import Declarations
from sed_converter.declarations.variables.variable import Variable
from sed_converter.dependencies.dependency import Dependency
from sed_converter.io.input import Input
from sed_converter.io.output import Output
from sed_converter.metadata.metadata import Metadata
from sed_converter.sed.sed_document import SedDocument


def test_create() -> None:
    metadata = Metadata(name="test", level=1, version=1, ontologies=["sed"])
    dependency = Dependency(
        name="depname", identifier="depid", type="org1::mytype", source="mysource"
    )
    constant1 = Constant(
        name="const1", identifier="const1id", type="org1::mytype", value="const1value"
    )
    constant2 = Constant(
        name="const2", identifier="const2id", type="org1::mytype", value="const2value"
    )
    var1 = Variable(name="var1", identifier="var1id", type="org1::mytype")
    declarations = Declarations(constants=[constant1, constant2], variables=[var1])
    input1 = Input(name="input1", identifier="var1id", type="org1::mytype", target="#target1")
    input2 = Input(name="input2", identifier="var1id", type="org1::mytype", target="#target1")
    output1 = Output(name="output1", identifier="var1id", type="org1::mytype", interval=1)
    action1 = Action(name="action1", identifier="var1id", type="org1::mytype")
    doc = SedDocument(
        metadata=metadata,
        dependencies=[dependency],
        declarations=declarations,
        inputs=[input1, input2],
        outputs=[output1],
        actions=[action1],
    )

    assert doc is not None
    model_json = doc.model_dump_json()
    assert (
        model_json == '{"metadata":{"name":"test","level":1,"version":1,"ontologies":["sed"]},'
        '"dependencies":['
        '{"name":"depname","identifier":"depid","type":"org1::mytype","source":"mysource"}],'
        '"declarations":{'
        '"constants":['
        '{"name":"const1","identifier":"const1id","type":"org1::mytype","value":"const1value"},'
        '{"name":"const2","identifier":"const2id","type":"org1::mytype","value":"const2value"}],'
        '"variables":['
        '{"name":"var1","identifier":"var1id","type":"org1::mytype"}]'
        "},"
        '"actions":[{"name":"action1","identifier":"var1id","type":"org1::mytype"}],'
        '"inputs":['
        '{"name":"input1","identifier":"var1id","type":"org1::mytype","target":"#target1"},'
        '{"name":"input2","identifier":"var1id","type":"org1::mytype","target":"#target1"}],'
        '"outputs":[{"name":"output1","identifier":"var1id","type":"org1::mytype","interval":"1.0"}]}'
    )

    doc2: SedDocument = SedDocument.model_validate_json(model_json)
    assert doc2 == doc
