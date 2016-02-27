"""
RDF to ASP converting functions.

Main API is rdffile_to_aspfile(3), and triplet_to_atom(1).

"""
import os
import rdflib


UNWANTED_CHARS = set("\n\r")
ESCAPABLE_CHARS = set("\"'\\")
DEFAULT_ATOM_NAME = 'entry'


# Follows various private methods definitions


def _callable_to(to_be_call):
    """Return a callable, depending of what is to_be_call.

    If to_be_call is a callable, it will be returned.
    If to_be_call is a string and a valid filename, the file will be open as a
        python module and a function named 'to_be_call' will be returned,
        if found in the python file. If not, a ValueError is raised.
    Else, a callable taking one parameter and returning always to_be_call
        will be returned.

    """
    if callable(to_be_call):
        return to_be_call

    if to_be_call and os.path.isfile(to_be_call):
        raise NotImplementedError

    return lambda _: to_be_call


def _aspify_item(item, prefix='', suffix=''):
    """Return item, human readable"""
    return prefix + ''.join(
        ('\\' + c) if c in ESCAPABLE_CHARS else c
        for c in item
        if c not in UNWANTED_CHARS
    ) + suffix
    return ret


def _is_blank(triplet):
    """True if given triplet describes a blank node"""
    return any(item.__class__ is rdflib.term.BNode for item in triplet)


def _triplets_from_file(filename, keep_blank_nodes=False, input_format=None):
    """Yield triplets found in RDF file of given filename"""
    # guess input format if not given
    if input_format is None:
        input_format = rdflib.util.guess_format(filename)
    # parse triplets and eventually filter out blank nodes
    triplets = rdflib.Graph().parse(filename, format=input_format)
    if not keep_blank_nodes:
        triplets = (triplet for triplet in triplets if not _is_blank(triplet))
    # convert triplets class in tuple
    yield from (tuple(item.toPython() for item in triplet)
                for triplet in triplets)


# Main API


def aspified(data_tuple, atom_name=None, no_uri=False,
             decompose=False, end='.'):
    """Return the atom holding given data, with the name returned by
    atom_name(data_tuple) and eventually no URI.

    data_tuple: tuple of data to be aspified.
    atom_name: callable, taking data_tuple and returning a string, or string.
    no_uri: flag, True for remove URI/URL from data_tuple items.
    decompose: flag, True for split data_tuple items in sub items on ':' char.
    end: string added at the end of the returned string.

    Note that the atom_name can be:
        - string: this string will be used as atom name for all retrieved data,
                  or, if its a valid filename, will be read and will use the
                  first function named 'atom_name' as a callable as input.
        - callable: will be called for each tuple of data, with the tuple as
                    single argument. Must return a string, that will be used
                    as atom name for the considered tuple.

    >>>aspified('go:47 a go:18')
    'entry("go:47","a","go:18").'
    >>>aspified('go:47 a go:18', decompose=True)
    'entry(("go","47"),"a",("go","18")).'
    >>>aspified('go:47 a go:18', end='')
    'entry("go:47","a","go:18")'

    """

    # get a callable giving atom name knowing data_tuple
    atom_name_func = _callable_to(atom_name if atom_name else DEFAULT_ATOM_NAME)

    # process and eventually convert to int the data
    processed_items = []
    for item in data_tuple:
        try:
            item = int(item)
        except ValueError:
            if no_uri and item.startswith('http://'):
                item = item[item.rfind('/')+1:]
            item = _aspify_item(item)
            if decompose and ':' in item:
                item = '("' + '","'.join(item.split(':')) + '")'
            else:
                item = '"' + item + '"'
        processed_items.append(item)
    # create the final atom
    args = '(' + ','.join(str(item) for item in processed_items) + ')'
    return atom_name_func(data_tuple) + args + end


def file_to_file(input_filename, output_filename, converter=aspified,
                 erase=True, keep_blank_nodes=False):
    """Put data in input_filename (RDF) in output_filename, using the converter
    callable for convert the data."""

    converted_atoms = (
        converter(triplet)
        for triplet in _triplets_from_file(input_filename, keep_blank_nodes)
    )

    with open(output_filename, 'w' if erase else 'a') as of:
        for atom in converted_atoms:
            of.write(atom)
