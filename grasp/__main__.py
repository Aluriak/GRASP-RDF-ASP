"""
usage:
    __main__.py [--help]
    __main__.py convert <input_RDF_filename> <output_filename> [options]
    __main__.py retrieve <database_URI> <input_SPARQL_query> <output_filename> [options]
    __main__.py query <input_ASP_data> <input_ASP_query> [options]

options:
    -h, --help      print this message
    --append-asp    append the new data to local db instead of replace it
    --keep-blanks   don't filter out triplets containing any blank data

convert:
    Converts given RDF file in an ASP readable file.

retrieve:
    Queries given database with given SPARQL query, convert results in ASP
    readable format and put it in given output file.
    Note that the SPARQL query should expose the 3 variables object,
    relation and subject.

query:
    Performs the ASP query on the ASP readable format.
    Print the output in stdout.

"""
import sys
from docopt import docopt
from . import rdftoasp
from . import query
from . import sparql


if __name__ == '__main__':
    args = docopt(__doc__)
    keep_prev_asp = args['--append-asp']
    no_blank_nodes = not args['--keep-blanks']

    if args['convert']:
        rdftoasp.file_to_file(args['<input_RDF_filename>'],
                              args['<output_filename>'],
                              erase_previous_data=keep_prev_asp,
                              no_blank_nodes=no_blank_nodes)

    elif args['retrieve']:
        db_uri = args['<database_URI>']
        sparql_query = args['<input_SPARQL_query>']
        output_filename = args['<output_filename>']
        of_mode = 'a' if keep_prev_asp else 'w'
        with open(sparql_query) as qf, open(output_filename, of_mode) as of:
            for triplet in sparql.query(db_uri, qf.read()):
                of.write(rdftoasp.triplet_to_atom(triplet))

    elif args['query']:
        file_data = args['<input_ASP_data>']
        file_query = args['<input_ASP_query>']
        for idx, answer in enumerate(query.answers(file_query, file_data)):
            print('\nAnswer ' + str(idx) + ':')
            print('\t' + '\n\t'.join(sorted(answer)))
