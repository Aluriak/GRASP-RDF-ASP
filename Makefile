DATA_DIR=data/
QUERY_DIR=queries/
RDF_DATABASE=$(DATA_DIR)owlapi.xrdf
ASP_DATABASE=$(DATA_DIR)rdf.lp
ASP_QUERY=$(QUERY_DIR)test.lp
DB_URI=http://dbpedia.org/sparql
SPARQL_QUERY=$(QUERY_DIR)test.dql

c:
	python -m grasp convert $(RDF_DATABASE) $(ASP_DATABASE)

r:
	python -m grasp retrieve $(DB_URI) $(SPARQL_QUERY) $(ASP_DATABASE)

q:
	python -m grasp query $(ASP_QUERY) $(ASP_DATABASE)

t:
	python3 test.py


# verbose aliases
test: t
query: q
convert: c
retrieve: r
