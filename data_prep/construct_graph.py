import EntityExtractor 
import WikiDataRetriever 
import json

class GraphNode:
    def __init__(self, text, idx):
        self.text = text
        self.idx = idx


def main(file_path):
    entity_extractor = EntityExtractor()
    data_retriever = WikiDataRetriever()

    with open(file_path, "r") as file:
    # Iterate over each line in the file
        for line in file:
        # Parse the JSON string into a Python dictionary
            data = json.loads(line)
            entity_to_passage_ids = {}
            passage_id_to_entity = {}
            
            question = data["question"]

            graph_nodes = [GraphNode(question, -1)]

            paragraphs = data["paragraphs"]

            for paragraph in paragraphs: 
                paragraph_text = paragraph["title"]
                paragraph_text += paragraph["paragraph_text"]
                idx = paragraph["idx"]
                graph_nodes.append(GraphNode(paragraph_text, idx))

            for nodes in graph_nodes:
                entities = entity_extractor.get_entities(nodes.text) 
                # print(entities)
                passage_id_to_entity[nodes.idx] = set()
                for entity in entities:
                    if entity_to_passage_ids.get(entity) == None:
                        entity_to_passage_ids[entity] = set() 
                    entity_to_passage_ids[entity].add(nodes.idx)
                    passage_id_to_entity[nodes.idx].add(entity)

            adj = {}
            for nodes in graph_nodes:
                adj[nodes.idx] = set()
                for entity in passage_id_to_entity[nodes.idx]:
                    child_entities = data_retriever.get_child_entities(entity)
                    for child_entity in child_entities:
                        # print(child_entity)
                        if entity_to_passage_ids.get(child_entity[0]) != None:
                            for passage_id in entity_to_passage_ids[child_entity]:
                                adj[nodes.idx].add(passage_id)
                    for passage_id in entity_to_passage_ids.get(entity):
                      if passage_id != nodes.idx:
                            adj[nodes.idx].add(passage_id)


            print(adj)
            print(entity_to_passage_ids)
            print(passage_id_to_entity)
            break

if __name__ == '__main__':
    file_path = "musique_data_v1.0/data/musique_ans_v1.0_train.jsonl"
    main(file_path)