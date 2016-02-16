# -*- coding: utf-8 -*-
"""
Definitions of model_from(5) that encapsulate
 the ASP grounder and solver calls.

"""
from collections import deque
from pyasp import asp


ASP_GRINGO_OPTIONS = ''
ASP_CLASP_OPTIONS  = '--parallel-mode 4 split'


def model_from(base_atoms, aspfiles, aspargs={},
               gringo_options='', clasp_options=''):
    """Compute a model from ASP source code in aspfiles, with aspargs
    given as grounding arguments and base_atoms given as input atoms.

    base_atoms -- string, ASP-readable atoms
    aspfiles -- (list of) filename, contains the ASP source code
    aspargs -- dict of constant:value that will be set as constants in aspfiles
    gringo_options -- string of command-line options given to gringo
    clasp_options -- string of command-line options given to clasp

    """
    # use the right basename and use list of aspfiles in all cases
    if isinstance(aspfiles, str):
        aspfiles = [aspfiles]
    elif isinstance(aspfiles, tuple):  # solver take only list, not tuples
        aspfiles = list(aspfiles)

    # define the command line options for gringo and clasp
    constants = ' -c '.join(str(k)+'='+str(v) for k,v in aspargs.items())
    if len(aspargs) > 0:  # must begin by a -c to announce the first constant
        constants = '-c ' + constants
    gringo_options = ' '.join((constants, ASP_GRINGO_OPTIONS, gringo_options))
    clasp_options += ' ' + ' '.join(ASP_CLASP_OPTIONS)

    #  create solver and ground base and program in a single ground call.
    solver = asp.Gringo4Clasp(gringo_options=gringo_options,
                              clasp_options=clasp_options)
    answers = solver.run(aspfiles, additionalProgramText=base_atoms)

    # return all found stable models
    return answers
