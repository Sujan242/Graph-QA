# pip install spacy-entity-linker
# python -m spacy_entity_linker "download_knowledge_base"
import spacy  # version 3.5

# initialize language model
nlp = spacy.load("en_core_web_md")

# add pipeline (declared through entry_points in setup.py)
nlp.add_pipe("entityLinker", last=True)


def main():
	file_path = "musique_data_v1.0/data/musique_ans_v1.0_train.jsonl"

	with open(file_path, "r") as file:
    # Iterate over each line in the file
        for line in file:
        # Parse the JSON string into a Python dictionary
            data = json.loads(line)
            
            question = data["question"]

            question_decompositions = data["question_decomposition"]

            linked_entities_question = nlp(question)._.linkedEntities

            # get wikidata link
            # get en wikipedia url 
            # extract contents of this wikipedia article 
            # go through all the passages and add an edge between this node and that node, 
            # if there is a similarity greater than threshold 
            # create new json object with a key called edges 

            # approach-2 
            # get entitiies and wikidataIds for all passages 
            # then add an edge between passage-1 to passage-2 if there is an entity in the entity graph of passage-1
            # that matches an entity is passage-2.  