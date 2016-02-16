# Directories
DATA_DIR=data/
QUERY_DIR=queries/

# Local databases
ASP_DATABASE=$(DATA_DIR)rdf.lp
RDF_DATABASE=$(DATA_DIR)owlapi.xrdf
RDF_DATABASE=$(DATA_DIR)goa_ecoli-20150528-goUniprotUri.ttl
#RDF_DATABASE=$(DATA_DIR)test.ttl

# Queries
ASP_QUERY=$(QUERY_DIR)test.lp
SPARQL_QUERY=$(QUERY_DIR)test.rq

ASP_QUERY=$(QUERY_DIR)goa_scoring.lp
#SPARQL_QUERY=$(QUERY_DIR)goa_scoring.rq

# Database uri (for retrieve routine)
DB_URI=http://dbpedia.org/sparql

# Grasp options
#KEEP_ASP_DB=--keep-prev-asp
#KEEP_BLANKS=--keep-blanks
DECOMPOSE=--decompose
NO_URI=--no-uri

OPTIONS=$(KEEP_ASP_DB) $(KEEP_BLANKS) $(DECOMPOSE) $(NO_URI)


c:
	python -m grasp convert $(RDF_DATABASE) $(ASP_DATABASE) $(OPTIONS)

r:
	python -m grasp retrieve $(DB_URI) $(SPARQL_QUERY) $(ASP_DATABASE) $(OPTIONS)

q:
	python -m grasp query $(ASP_QUERY) $(ASP_DATABASE) $(OPTIONS)

t:
	python3 test.py

h:
	python -m grasp --help


# verbose aliases
help: h
test: t
query: q
convert: c
retrieve: r
