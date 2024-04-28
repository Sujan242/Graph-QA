import EntityExtractor 
import WikiDataRetriever 
import json

class GraphNode:
    def __init__(self, text, idx):
        self.text = text
        self.idx = idx


def write_adj_list(line, entity_extractor): 
            data = json.loads(line)
            entity_to_passage_ids = {}
            passage_id_to_entity = {}

            if not os.path.isfile(f'drive/MyDrive/Graph_QA/graphs/adj_graph_{data["id"]}.json'):
            
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
                      # child_entities = data_retriever.get_child_entities(entity)
                      # for child_entity in child_entities:
                      #     # print(child_entity)
                      #     if entity_to_passage_ids.get(child_entity[0]) != None:
                      #         for passage_id in entity_to_passage_ids[child_entity]:
                      #             adj[nodes.idx].add(passage_id)
                      for passage_id in entity_to_passage_ids.get(entity):
                        if passage_id != nodes.idx:
                              adj[nodes.idx].add(passage_id)

              adj_list = {}
              for key in adj:
                adj_list[key] = list(adj[key])

              # print("writing here")
              with open(f'drive/MyDrive/Graph_QA/graphs/adj_graph_{data["id"]}.json', 'w') as fp:
                json.dump(adj_list, fp)

def main(file_path):
    entity_extractor = EntityExtractor()
    data_retriever = WikiDataRetriever()

    num_json = 0

    with open(file_path, "r") as file:
    # Iterate over each line in the file
        for line in file:
        # Parse the JSON string into a Python dictionary
            # num_json += 1
            # if(num_json % 10 ==0):
            #   print(num_json)
            # write_adj_list(line, entity_extractor)
            with ThreadPoolExecutor(max_workers=5) as exe:
                exe.submit(write_adj_list,line, entity_extractor)
            # break

    # with open('graphs_train.json', 'w') as fp:
    #     json.dump(adjacency_lists, fp)

if __name__ == '__main__':
    file_path = "musique_data_v1.0/data/musique_ans_v1.0_train.jsonl"
    main(file_path)