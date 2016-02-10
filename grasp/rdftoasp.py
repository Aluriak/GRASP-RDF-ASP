"""
RDF to ASP converting functions.

Main API is rdffile_to_aspfile(3).

"""
import rdflib


UNWANTED_CHARS = set("\"'\n\r")


def triplet_to_atom(triplet):
    """Return given triplet as an ASP readable atom"""
    return 'triplet("' + '","'.join(str(item) for item in triplet) + '").'


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


def is_blank(triplet):
    """True if given triplet describes a blank node"""
    return any(item.__class__ is rdflib.term.BNode for item in triplet)


def triplets_from_file(filename, no_blank=True):
    """Yield triplets found in RDF file of given filename"""
    return (triplet for triplet in rdflib.Graph().parse(filename)
            if not is_blank(triplet))


def aspify(filename, end='\n', process=humanized):
    """Yield processed triplets as ASP atoms, ended by end character"""
    yield from (triplet_to_atom(process(triplet)) + end
                for triplet in triplets_from_file(filename))


def rdffile_to_asp(input_filename, output_filename, atom_process=humanized):
    """Put data in input_filename (RDF) in output_filename (ASP atoms)"""
    with open(output_filename, 'w') as of:
        for atom in aspify(input_filename, process=atom_process):
            of.write(atom)
