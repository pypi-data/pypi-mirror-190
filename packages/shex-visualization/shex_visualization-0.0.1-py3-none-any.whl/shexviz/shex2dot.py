from ShExJSG import Schema, ShExC, ShExJ
from ShExJSG.ShExJ import Shape, IRIREF, TripleConstraint, NodeConstraint, ShapeOr, EachOf, ShapeExternal, ShapeDecl, Annotation, ObjectLiteral
from pyshex.utils.schema_loader import SchemaLoader
import graphviz

def process_tc(tc, shape_id):
    print(tc)
    dotschema.node(startshape.replace(":", ""), startshape, shape=symbol["iri"])
    if isinstance(tc, TripleConstraint):
        if isinstance(tc.valueExpr, IRIREF):
            node = tc.valueExpr
            predicate = tc.predicate
            for key in prefixmap.keys():
                node = node.replace(key, prefixmap[key])
                predicate = predicate.replace(key, prefixmap[key] + ":")
            dotschema.node(node, node, shape=symbol["iri"])
            dotschema.edge(shape.id.split("/")[-1], node, label=predicate)
        elif isinstance(tc.valueExpr, NodeConstraint):

            if tc.valueExpr.datatype:
                datatype = tc.valueExpr.datatype
                predicate = tc.predicate
                for key in prefixmap.keys():
                    datatype = datatype.replace(key, prefixmap[key] + ":")
                    predicate = predicate.replace(key, prefixmap[key] + ":")
                dotschema.node(
                    shape.id.split("/")[-1] + tc.valueExpr.datatype.split("/")[-1] + tc.predicate.split("/")[-1],
                    datatype, shape=symbol["datatype"])
                dotschema.edge(shape.id.split("/")[-1],
                               shape.id.split("/")[-1] + tc.valueExpr.datatype.split("/")[-1] + tc.predicate.split("/")[
                                   -1], label=predicate)
            elif tc.valueExpr.values:
                oneofs = []
                predicate = tc.predicate
                for value in tc.valueExpr.values:
                    for key in prefixmap.keys():
                        value = value.replace(key, prefixmap[key] + ":")
                    oneofs.append(value)
                for key in prefixmap.keys():
                    predicate = predicate.replace(key, prefixmap[key] + ":")
                dotschema.node(
                    shape.id.split("/")[-1] + "|".join(oneofs).replace(":", "") + tc.predicate.split("/")[-1],
                    "{" + "|".join(oneofs) + "}", shape=symbol["oneof"])
                dotschema.edge(shape.id.split("/")[-1],
                               shape.id.split("/")[-1] + "|".join(oneofs).replace(":", "") + tc.predicate.split("/")[
                                   -1], label=predicate)

            elif tc.valueExpr.nodeKind:
                dotschema.node(tc.valueExpr.nodeKind, tc.valueExpr.nodeKind.split("/")[-1],
                               shape=symbol[tc.valueExpr.nodeKind])
                dotschema.edge(shape.id.split("/")[-1], tc.valueExpr.nodeKind.split("/")[-1],
                               label=tc.predicate.split("/")[-1])
            elif tc.valueExpr.xone:

                dotschema.node(tc.valueExpr.xone[0].id, tc.valueExpr.xone[0].id.split("/")[-1], shape=symbol["oneof"])
                dotschema.edge(shape.id.split("/")[-1], tc.valueExpr.xone[0].id.split("/")[-1],
                               label=tc.predicate.split("/")[-1])
            else:
                print("No valueExpr")
        else:
            print("No valueExpr")

symbol = dict()
symbol["class"] = "oval"
symbol["datatype"] = "octagon"
symbol["literal"] = "rectangle"
symbol["iri"]="diamond"
symbol["bnode"]='point'
symbol["oneof"]='record'

dotschema = graphviz.Digraph('shape.gv')
dotschema.graph_attr['rankdir'] = 'LR'

shex = """
IMPORT <file_metadata.shex>
PREFIX : <http://example.org/>
PREFIX filemeta: <file_metadata.shex>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX unit: <http://qudt.org/vocab/unit/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

start = @:subject

:subject {
    dct:isPartOf filemeta:fileURI ;
    rdf:type [obo:NCIT_C16960] ; # Patient
    dct:identifier xsd:string ;
    sio:SIO_000223 @:subjectProperties ;

}

:subjectProperties {
    obo:TXPO_0001873 @:BMI ;
    obo:TXPO_0001873 @:HgbA1c ;
    ccf:has_ethnicity @:etnicity ;
}

:etnicity {
    rdfs:subClassOf [obo:NCIT_C16564] ; ## etnic group
}

:BMI {
    rdf:type qudt:Quantity ;
    qudt:hasQuantityKind [obo:NCIT_C16358] ; # Body Mass Index
    qudt:unit [unit:KiloGM-PER-M2] ; # kg/m^2
    qudt:numericValue xsd:decimal ; # 18.5 - 24.9
}

:HgbA1c {
    rdf:type qudt:Quantity ;
    qudt:hasQuantityKind [obo:NCIT_C64849] ; # HgbA1c
    qudt:unit [unit:MilliMOL-PER-MOL] ; # mmol/mol
    qudt:numericValue xsd:decimal ;
}
  """
prefixmap = dict()
for line in shex.splitlines():
    if line.startswith("PREFIX"):
        line = line.replace("PREFIX", "")
        print(line)
        prefix, uri = line.split(": ")
        prefix = prefix.strip()
        uri = uri.strip()
        prefixmap[uri.replace("<", "").replace(">", "")] = prefix
        dotschema.node(prefix, uri, shape="none", style="invis")

loader = SchemaLoader()
schema = loader.loads(shex)
# print(ShExJ(schema))
print(f"Valid: {schema._is_valid()}")
#print(f"{schema._as_json_dumps()}")
print(schema.shapes[0].expression.expressions)
for shape in schema.shapes:
    print(shape.id)
    startshape = shape.id
    for key in prefixmap.keys():
        startshape = startshape.replace(key, prefixmap[key]+":")
    if "expressions" in dir(shape.expression):
        for tc in shape.expression.expressions:
            process_tc(tc, startshape)
    else:
        tc = shape.expression
        process_tc(tc, startshape)

dotschema.view()

print(prefixmap)
print(dotschema.source)