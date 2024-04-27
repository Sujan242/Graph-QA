# !python -m spacy download en_core_web_md
# !pip install spacy-entity-linker
# !python -m spacy_entity_linker "download_knowledge_base"
import spacy 


class EntityExtractor:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.nlp.add_pipe("entityLinker", last=True)

    def get_entities(self, text):
        entities = []
        for linked_entity in nlp(text)._.linkedEntities:
            entities.append(linked_entity.get_id())
        return entities