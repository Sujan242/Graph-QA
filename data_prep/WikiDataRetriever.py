# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

class WikiDataRetriever:

    def __init__(self):
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        self.query_template =   """
SELECT ?item ?itemLabel ?itemImage ?value ?valueLabel ?valueImage ?edgeLabel WHERE {{
  BIND(wd:Q{QID} AS ?item)
  ?item ?wdt ?value.
  ?edge a wikibase:Property;
        wikibase:propertyType wikibase:WikibaseItem; # note: to show all statements, removing this is not enough, the graph view only shows entities
        wikibase:directClaim ?wdt.
  OPTIONAL {{ ?item wdt:P18 ?itemImage. }}
  OPTIONAL {{ ?value wdt:P18 ?valueImage. }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}""" 
        self.cache = {}

    def get_child_entities(self, entityId):
        if self.cache.get(entityId) != None:
            return self.cache[entityId]

        # print(self.query_template)
        query = self.query_template.format(QID = entityId)
        sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        query_result = sparql.query().convert()

        childEntities = [] 
        for result in query_result["results"]["bindings"]:
            qid = result["value"]["value"].split("/")[-1][1:]

            childEntities.append([qid, result['edgeLabel']['value']])

        self.cache[entityId] = childEntities
        return childEntities