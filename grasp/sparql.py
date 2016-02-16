"""
Definition of functions allowing interrogation of a database with one query.

"""
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from . import commons


def _json_to_triplet(json):
    """Return an RDFTriplet, created by parsing given json dict.

    Expected json object should be as {triplet component: {'value': value}},
    where triplet component is one in commons.RDF_TRIPLET, and value the value
    that will be used as component id.

    """
    return commons.RDFTriplet(*(json[term]['value']
                                for term in commons.RDF_TRIPLET))

def valid_query(query, expected_fields=commons.RDF_TRIPLET):
    """True iff given query is valid, ie will produce an expected output,
    regarding to the selected variables.

    Expected output is composed of the strings given expected fields

        >>>> q = "SELECT ?a ?b WHERE { ... }"
        >>>> valid_query(q, ('a', 'b'))
        True
        >>>> valid_query(q, ('a', 'b', 'c'))
        False
        >>>> valid_query(q, ('a'))
        False
        >>>> valid_query(q, (,))
        False

    """
    reg = re.compile(r"SELECT\s+\?" + "\s+\?".join(expected_fields))
    return reg.search(query)


def query(database_uri, query):
    """Wait for a valid database URI, and a SPARQL query.
    Yields all triplets returned by the query.

    The query need to yield three values, named object, relation and subject.

    """
    assert valid_query(query)
    sparql = SPARQLWrapper(database_uri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results['results']['bindings']:
        yield _json_to_triplet(result)
