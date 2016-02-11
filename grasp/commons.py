"""
Various definitions commonly used in the whole module.

"""

from collections import namedtuple


# all triplets are made of an object, a relation and a subject.
RDF_TRIPLET_LEFT   = 'object'
RDF_TRIPLET_MIDDLE = 'relation'
RDF_TRIPLET_RIGHT  = 'subject'
RDF_TRIPLET = (RDF_TRIPLET_LEFT, RDF_TRIPLET_MIDDLE, RDF_TRIPLET_RIGHT)

# here is a wrapper around all these definitions
RDFTriplet = namedtuple('RDFTriplet', RDF_TRIPLET)
