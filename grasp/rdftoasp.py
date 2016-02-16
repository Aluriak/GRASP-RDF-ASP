"""
RDF to ASP converting functions.

Main API is rdffile_to_aspfile(3), and triplet_to_atom(1).

"""
import rdflib


UNWANTED_CHARS = set("\"'\n\r\\")


# Follows various private methods definitions


def humanized(triplet, no_uri=False):
    """Return same triplet, human readable"""
    assert len(triplet) == 3
    def uri_removed(item):
        if item.startswith('http:/'):
            return item[item.rfind('/')+1:]
        else:
            return item
    if no_uri:
        triplet = (uri_removed(item) for item in triplet)
    ret = tuple(
        ''.join(c for c in item if c not in UNWANTED_CHARS)
        for item in triplet
    )
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


def _aspify(filename, process=humanized, keep_blank_nodes=False,
            decompose_atom=False, end='\n'):
    """Yield processed triplets as ASP atoms, ended by end character"""
    yield from (triplet_to_atom(triplet, processed=process,
                                decompose=decompose_atom) + end
                for triplet in _triplets_from_file(filename, keep_blank_nodes))


# Main API


def triplet_to_atom(triplet, processed=humanized, decompose=False):
    """Return given triplet as an ASP readable atom.

    If decompose is True, the atom will be decomposed as possible, for example:
    prefix:value is converted as ("prefix", "value") in atoms.

    >>>triplet_to_atom('go:47 a go:18')
    triplet("go:47","a","go:18").
    >>>triplet_to_atom('go:47 a go:18', decompose=True)
    triplet(("go","47"),"a",("go","18")).

    """
    processed_items = []
    # process and eventually convert to int the wanted triplets
    for item in (_ for _ in processed(triplet)):
        try:
            item = int(item)
        except ValueError:
            if decompose and ':' in item:
                item = '("' + '","'.join(sub for sub in item.split(':')) + '")'
            else:
                item = '"' + item + '"'
        processed_items.append(item)
    ret = 'triplet(' + ','.join(str(item) for item in processed_items) + ').'
    return ret


def file_to_file(input_filename, output_filename, atom_processed=humanized,
                 keep_previous_data=True, keep_blank_nodes=False,
                 decompose_atom=False):
    """Put data in input_filename (RDF) in output_filename (ASP atoms)"""
    of_mode = 'a' if keep_previous_data else 'w'
    with open(output_filename, of_mode) as of:
        for atom in _aspify(input_filename, process=atom_processed,
                            keep_blank_nodes=keep_blank_nodes,
                            decompose_atom=decompose_atom):
            of.write(atom)
