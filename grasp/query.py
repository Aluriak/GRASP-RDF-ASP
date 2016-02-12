"""
Implementation of the query solving.

"""
from . import solving


def humanized(model):
    """Return the given model, humanized"""
    for atom in model:
        pass


def arg(atom):
    """Return the argument of given atom, as a tuple if necessary.
    If the atom have only one arg, the arg itself will be used.
    >>>> split('edge(lacA,lacZ)')
    ('lacA', 'lacZ')
    >>>> split('score(13)')
    ('13',)
    >>>> split('lowerbound')
    ()

    """
    try:
        return tuple(atom.strip(').').split('(')[1].split(','))
    except ValueError:  # no args
        return tuple()


def answers(file_query, file_data):
    """Yield answers of RDF triplets found in data that answer the query"""
    return solving.model_from('', [file_query, file_data])
