DATA_DIR=data/
QUERY_DIR=queries/
RDF_DATABASE=$(DATA_DIR)owlapi.xrdf
ASP_DATABASE=$(DATA_DIR)rdf.lp
ASP_QUERY=$(QUERY_DIR)test.lp

convert:
	python -m grasp convert $(RDF_DATABASE) $(ASP_DATABASE)

query:
	python -m grasp query $(ASP_QUERY) $(ASP_DATABASE)
