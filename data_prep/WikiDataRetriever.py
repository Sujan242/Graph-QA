import sys
from SPARQLWrapper import SPARQLWrapper, JSON

class WikiDataRetriever:

	def __init__(self):
		this.endpoint_url = "https://query.wikidata.org/sparql"
		this.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
		this.cache = {}

	def get_child_entities(self, entityId):
		if this.cache.get(entityId) != None:
			return this.cache[entityId]

		query =  f"""#All statements of an item containing another item (direct / first-degree connections)
					#defaultView:Graph
					#TEMPLATE={ "template": { "en": "All statements of ?item containing another item" }, "variables": { "?item": {} } }
					SELECT ?item ?itemLabel ?itemImage ?value ?valueLabel ?valueImage ?edgeLabel WHERE {
					  BIND(wd:{entityId} AS ?item)
					  ?item ?wdt ?value.
					  ?edge a wikibase:Property;
					        wikibase:propertyType wikibase:WikibaseItem; # note: to show all statements, removing this is not enough, the graph view only shows entities
					        wikibase:directClaim ?wdt.
					  OPTIONAL { ?item wdt:P18 ?itemImage. }
					  OPTIONAL { ?value wdt:P18 ?valueImage. }
					  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
					}
				"""
	    sparql = SPARQLWrapper(this.endpoint_url, agent=this.user_agent)
	    sparql.setQuery(query)
	    sparql.setReturnFormat(JSON)
	    query_result = sparql.query().convert()

	    childEntities = [] 
	    for result in results["results"]["bindings"]:
	    	childEntities.append([result["value"]["value"], result['edgeLabel']['value']])

	    this.cache[entityId] = childEntities
	    return childEntities