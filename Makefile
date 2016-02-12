DATA_DIR=data/
QUERY_DIR=queries/
RDF_DATABASE=$(DATA_DIR)owlapi.xrdf
ASP_DATABASE=$(DATA_DIR)rdf.lp
ASP_QUERY=$(QUERY_DIR)test.lp
DB_URI=http://dbpedia.org/sparql
SPARQL_QUERY=$(QUERY_DIR)test.rq
KEEP_ASP_DB=--append-asp
KEEP_BLANKS=--keep-blanks

OPTIONS=$(KEEP_ASP_DB) $(KEEP_BLANKS)


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
