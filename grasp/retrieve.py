"""
Definition of the main API for retrieving.

"""
import os
from . import rdftoasp
from . import sparql


def retrieve(db_url, sparql_query, output_file, erase=True,
             converted=rdftoasp.aspified):
    """Retrieve data from given db with given sparql query, and push it in
    ASP format in the given output filename.

    db_url: URL to the queried database.
    sparql_query: (filename containing) the SPARQL query.
    output_file: filename or file descriptor to be written.
    erase: flag, set to False for append new data to the output filename.
    converted: callable taking one tuple of data, returning a string version.
               (default is grasp.rdftoasp.aspify)
    return: number of processed atoms.

    """
    assert callable(converted)

    if os.path.isfile(sparql_query):
        with open(sparql_query) as fd:
            sparql_query = fd.read()
    # sparql_query is now the raw query as string
    assert isinstance(sparql_query, str)

    if isinstance(output_file, str):
        output_desc = open(output_file, 'w' if erase else 'a')
    else:  # output_file is a file descriptor
        assert output_file.write
        output_desc = output_file

    for idx, data_tuple in enumerate(sparql.query(db_url, sparql_query)):
        assert isinstance(data_tuple, tuple)
        output_desc.write(converted(data_tuple))

    if os.path.isfile(output_file):
        output_desc.close()

    return idx

