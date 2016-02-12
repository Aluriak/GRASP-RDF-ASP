"""
RDF to ASP converting functions.

Main API is rdffile_to_aspfile(3), and triplet_to_atom(1).

"""
import rdflib


UNWANTED_CHARS = set("\"'\n\r")


# Follows various private methods definitions


def humanized(triplet):
    """Return same triplet, human readable"""
    def uri_removed(item):
        if item.startswith('http:/'):
            return item[item.rfind('/')+1:]
        else:
            return item
    return tuple(
        ''.join(c for c in uri_removed(item) if c not in UNWANTED_CHARS)
        for item in triplet
    )


def _is_blank(triplet):
    """True if given triplet describes a blank node"""
    return any(item.__class__ is rdflib.term.BNode for item in triplet)


def _triplets_from_file(filename, no_blank=True):
    """Yield triplets found in RDF file of given filename"""
    return (triplet for triplet in rdflib.Graph().parse(filename)
            if not _is_blank(triplet))


def _aspify(filename, end='\n', process=humanized):
    """Yield processed triplets as ASP atoms, ended by end character"""
    yield from (triplet_to_atom(process(triplet)) + end
                for triplet in _triplets_from_file(filename))


# Main API


def triplet_to_atom(triplet):
    """Return given triplet as an ASP readable atom"""
    return 'triplet("' + '","'.join(str(item) for item in triplet) + '").'


def file_to_file(input_filename, output_filename, atom_process=humanized,
                 erase_previous_data=True):
    """Put data in input_filename (RDF) in output_filename (ASP atoms)"""
    of_mode = 'w' if erase_previous_data else 'a'
    with open(output_filename, of_mode) as of:
        for atom in _aspify(input_filename, process=atom_process):
            of.write(atom)
