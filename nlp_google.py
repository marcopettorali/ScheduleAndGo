from google.cloud import language_v1
import os


class NaturalProcessingLanguageGoogleCloud:
    def __init__(self):
        # write path of Google Cloud Credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "googlekey.json"
        # set parameters for each request
        self.client = language_v1.LanguageServiceClient()
        self.type_ = language_v1.Document.Type.PLAIN_TEXT
        self.encoding_type = language_v1.EncodingType.UTF8

    def analyze_task(self, text_content):
        # build request JSON
        document = {"content": text_content, "type_": self.type_}
        # get list of entities
        entities = self.extract_entities(self.client, self.encoding_type, document)
        # get list of words
        words = self.extract_syntax(self.client, self.encoding_type, document)
        # return the task observed in this sentence
        return self.extract_task(entities, words)

    def extract_entities(self, client, encoding_type, document):

        # send request
        response = client.analyze_entities(request={'document': document, 'encoding_type': encoding_type})
        entities = []
        for entity in response.entities:
            # get first mention from all entities (the entitiy itself) to get the bof
            mention = entity.mentions[0]
            entities.append({
                # text of the entity
                "txt": mention.text.content,
                # type of entity (eg LOCATION, PERSON...)
                "typ": language_v1.Entity.Type(entity.type_).name,
                # position of the first char of the entity in the sentence
                "bof": mention.text.begin_offset,
                # position of the last char + 1 of the entity in the sentence
                "eof": len(mention.text.content) + mention.text.begin_offset,
                # mark entity if already checked (not to have duplicates when extracting entities from words, an entity can be composed by more words)
                "chk": False
            })
        return entities

    def extract_syntax(self, client, encoding_type, document):
        # send request
        response = client.analyze_syntax(request={'document': document, 'encoding_type': encoding_type})
        words = []

        for token in response.tokens:
            text = token.text
            dependency_edge = token.dependency_edge
            words.append({
                # text of the word
                "txt": text.content,
                # position of the first char of the word in the sentence
                "bof": text.begin_offset,
                # part of speech of the word (eg VERB, NOUN...)
                "pos": language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name,
                # head token index: index of the parent word in the dependency tree of the sentence
                "hti": dependency_edge.head_token_index,
                # lemma of the word (to get the infinitive verb of conjugated ones)
                "lem": token.lemma
            })

        return words

    def extract_task(self, entities, words):
        action = {}
        destination = ""

        for entity in entities:
            # add all the locations found in the destination (assuming a sentence only contains one destination)
            if entity['typ'] == 'LOCATION':
                destination += entity['txt'] + " "

        for word in words:
            # check all the nouns
            if word['pos'] == "NOUN":
                # extract the verb of the examined word
                verb = self.get_target(word, words)
                # extract the entity of which the word is part
                entity = self.pop_entity(word, entities)
                # if the entity is an object/person/event...
                if entity is not None and entity['typ'] not in ["LOCATION", "ADDRESS", "DATE", "PRICE"]:
                    # for each verb, put the list of all the objects/persons/events correlated to it
                    if verb['lem'] not in action:
                        action[verb['lem'].lower()] = entity['txt'] + " "
                    else:
                        action[verb['lem'].lower()] += entity['txt'] + " "

        # warn the user of a missing destination or action
        if destination == "" or action is None:
            print("WARNING: missing destination or action!")
            return None
        else:
            # build the task as destination + action
            task = {"destination": destination.strip(), "action": action}
            return task

    def pop_entity(self, word, entities):
        for entity in entities:
            # check if the word's bof is part of a non-marked entity
            if entity['chk'] == False and entity['bof'] <= word['bof'] < entity['eof']:
                # mark the entity
                entity['chk'] = True
                return entity
            elif entity['chk'] == True and entity['bof'] <= word['bof'] < entity['eof']:
                # if already marked, do not add another entity
                return None

    def get_target(self, word, words, target="VERB"):
        stop = False
        analyzed_word = word
        while not stop:
            # stop when find a verb
            if analyzed_word['pos'] == target:
                return analyzed_word
            # exit to prevent cycling on the same word (in case of get_target on a ROOT word)
            elif analyzed_word == words[analyzed_word['hti']]:
                return None
            # else analyze the parent of this node in the dependency tree
            else:
                analyzed_word = words[analyzed_word['hti']]