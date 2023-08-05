from owlready2 import Ontology

def check_metadata(metadata_uri, ontology):
    if metadata_uri in ontology.metadata:
        return True
    else:
        return False

