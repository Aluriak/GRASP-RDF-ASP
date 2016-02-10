"""
usage:
    __main__.py convert <input_RDF_filename> <output_filename> [options]
    __main__.py query <input_ASP_data> <input_ASP_query> [options]

options:
    -h, --help      print this message


"""
import sys
from docopt import docopt
from .rdftoasp import rdffile_to_asp
from . import query


DEFAULT_OUTPUT_FILE = 'rdf.lp'


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['convert']:
        rdffile_to_asp(args['<input_RDF_filename>'], args['<output_filename>'])
    elif args['query']:
        file_data = args['<input_ASP_data>']
        file_query = args['<input_ASP_query>']
        for idx, answer in enumerate(query.answers(file_query, file_data)):
            print('\nAnswer ' + str(idx) + ':')
            print('\t' + '\n\t'.join(sorted(answer)))
