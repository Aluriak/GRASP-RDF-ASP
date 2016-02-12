#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:59:29 2015

@author: Olivier Dameron
"""

dataDir = "/home/olivier/ontology/geneOntology/ecoli/"

with open(dataDir + "goa_ecoli-20150528-goUniprotUri.ttl", "w") as targetFile:
    targetFile.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    targetFile.write("@prefix uniprot: <http://purl.uniprot.org/uniprot/> .\n")
    targetFile.write("@prefix go: <http://purl.obolibrary.org/obo/> .\n")
    targetFile.write("@prefix goavoc: <http://bio2rdf.org/goa_vocabulary:> .\n")
    targetFile.write("@prefix goares: <http://bio2rdf.org/goa_resource:> .\n")
    targetFile.write("@prefix taxon: <http://bio2rdf.org/taxonomy:> .\n")
    targetFile.write("\n")
    with open(dataDir + "gene_association.ecocyc") as sourceFile:
        resourceIdent = 0
        for currentLine in sourceFile:
            if currentLine.startswith("!"):
                continue
            values = currentLine.replace("\n", "").split("\t")
            if len(values) == 0:
                continue

            uniprotID = values[1]
            goID = values[4]
            taxonID = values[12]
            
            #targetFile.write("uniprot:{0} goavoc:{1} {2} .\n".format(uniprotID, "x-taxonomy", taxonID))
            targetFile.write("uniprot:{0} goavoc:{1} go:{2} .\n".format(uniprotID, "go-term", goID.replace(":", "_")))
            
            targetFile.write("goares:{0} goavoc:{1} go:{2} .\n".format("ecoli_" + str(resourceIdent), "go-term", goID.replace(":", "_")))
            targetFile.write("goares:{0} goavoc:{1} go:{2} .\n".format("ecoli_" + str(resourceIdent), "target", uniprotID))
 
            targetFile.write("\n")
            
            resourceIdent += 1

#==============================================================================
# GENERATION de goavoc:process, goavoc:component, goavoc:function
#==============================================================================
#
# cd /home/olivier/ontology/geneOntology
# mkdir tdb-ecoli-goUniprotUri
#
# cd /usr/local/semanticWeb/jena/bin
# ./tdbloader2 --loc=/home/olivier/ontology/geneOntology/tdb-ecoli-goUniprotUri /home/olivier/ontology/geneOntology/ecoli/goa_ecoli-20150528-goUniprotUri.ttl
# ./tdbloader --loc=/home/olivier/ontology/geneOntology/tdb-ecoli-goUniprotUri /home/olivier/ontology/geneOntology/go-20150303.owl
# 
# cd /usr/local/semanticWeb/fuseki
# ./fuseki-server --update --loc /home/olivier/ontology/geneOntology/tdb-ecoli-goUniprotUri/ /eco
#
# REQUETES
# curl --data 'update=DELETE WHERE { ?prot <http://bio2rdf.org/goa_vocabulary:process> ?goTerm . }' http://localhost:3030/eco/update
# curl --data 'update=DELETE WHERE { ?prot <http://bio2rdf.org/goa_vocabulary:component> ?goTerm . }' http://localhost:3030/eco/update
# curl --data 'update=DELETE WHERE { ?prot <http://bio2rdf.org/goa_vocabulary:function> ?goTerm . }' http://localhost:3030/eco/update
#
# curl --data 'update=PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> PREFIX go: <http://purl.obolibrary.org/obo/GO_> PREFIX goavoc: <http://bio2rdf.org/goa_vocabulary:> INSERT { ?prot goavoc:process ?goTerm . } WHERE { ?assoc goavoc:go-term ?goTerm . ?assoc goavoc:target ?prot . ?goTerm rdfs:subClassOf* go:0008150 }' http://localhost:3030/eco/update 
# curl --data 'update=PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> PREFIX go: <http://purl.obolibrary.org/obo/GO_> PREFIX goavoc: <http://bio2rdf.org/goa_vocabulary:> INSERT { ?prot goavoc:component ?goTerm . } WHERE { ?assoc goavoc:go-term ?goTerm . ?assoc goavoc:target ?prot . ?goTerm rdfs:subClassOf* go:0005575 }' http://localhost:3030/eco/update 
# curl --data 'update=PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> PREFIX go: <http://purl.obolibrary.org/obo/GO_> PREFIX goavoc: <http://bio2rdf.org/goa_vocabulary:> INSERT { ?prot goavoc:function ?goTerm . } WHERE { ?assoc goavoc:go-term ?goTerm . ?assoc goavoc:target ?prot . ?goTerm rdfs:subClassOf* go:0003674 }' http://localhost:3030/eco/update 




