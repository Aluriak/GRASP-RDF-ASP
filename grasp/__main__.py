"""
usage:
    __main__.py [--help]
    __main__.py convert <input_RDF_filename> <output_filename> [options]
    __main__.py retrieve <database_URI> <input_SPARQL_query> <output_filename> [options]
    __main__.py query <input_ASP_query> <input_ASP_data> [options]

options:
    -h, --help            print this message
    --keep-prev-asp       append the new data to local db instead of replace it
    --keep-blanks         don't filter out triplets containing any blank data
    --decompose           decompose more ASP atoms, allowing finer treatments
    --no-uri              remove URIs from atoms values
    --atom-name=STR       name of atoms pushed in ASP db
    --gringo-options=STR  options send to the grounder
    --clasp-options=STR   options send to the solver

convert:
    Converts given RDF file in an ASP readable file.

retrieve:
    Queries given database with given SPARQL query, convert results in ASP
    readable format and put it in given output file.

query:
    Performs the ASP query on the ASP readable format.
    Print the output in stdout.

"""
from functools import partial

from docopt import docopt

from . import rdftoasp
from . import sparql
import grasp


if __name__ == '__main__':
    # get arguments and retrieve flags
    args = docopt(__doc__)
    keep_prev_asp = args['--keep-prev-asp']
    keep_blank_nodes = args['--keep-blanks']
    decompose_atom = args['--decompose']

    # curry the postprocess function that convert the values
    atom_converter = partial(rdftoasp.aspified, no_uri=args['--no-uri'],
                              decompose=decompose_atom,
                              atom_name=args['--atom-name'], end='.\n')

    # perform the targeted treatment
    if args['convert']:
        grasp.convert(args['<input_RDF_filename>'],
                      args['<output_filename>'],
                      erase=not keep_prev_asp,
                      converter=atom_converter,
                      keep_blank_nodes=keep_blank_nodes)

    elif args['retrieve']:
        grasp.retrieve(args['<database_URI>'], args['<input_SPARQL_query>'],
                       args['<output_filename>'], erase=not keep_prev_asp,
                       converted=atom_converter)

    elif args['query']:
        answers = grasp.query(args['<input_ASP_query>'],
                              args['<input_ASP_data>'],
                              gringo_options=args['--gringo-options'],
                              clasp_options=args['--clasp-options'])
        if len(answers) == 0:
            print('No answers !')
        for idx, answer in enumerate(answers):
            print('\nAnswer ' + str(idx) + ':')
            print('\t' + '\n\t'.join(sorted(answer)))
