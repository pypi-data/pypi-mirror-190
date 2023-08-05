from owlready2 import *


class OwlModel:
    ontology: Ontology

    def __init__(self, ontology_url):
        self.ontology = get_ontology(ontology_url).load()

    def get_base_iri(self):
        if hasattr(self.ontology,"base_iri"):
            return self.ontology.base_iri
        else:
            return ""

    def get_license(self):
        if hasattr(self.ontology.metadata,"license"):
            return self.ontology.metadata.license
        else:
            return ""

    def get_backward_compatibility(self):
        if hasattr(self.ontology.metadata,"backwardCompatibleWith"):
            return self.ontology.metadata.backwardCompatibleWith
        else:
            return ""

    def get_creator(self):
        if hasattr(self.ontology.metadata, "creator"):
            return self.ontology.metadata.creator
        else:
            return ""

    def get_created(self):
        if hasattr(self.ontology.metadata, "created"):
            return self.ontology.metadata.created
        else:
            return ""

    def get_modified(self):
        if hasattr(self.ontology.metadata, "modified"):
            return self.ontology.metadata.modified
        else:
            return ""

    def get_preferred_namespace_prefix(self):
        if hasattr(self.ontology.metadata, "preferredNamespacePrefix"):
            return self.ontology.metadata.preferredNamespacePrefix
        else:
            return ""

    def get_preferred_namespace_uri(self):
        if hasattr(self.ontology.metadata, "preferredNamespaceUri"):
            return self.ontology.metadata.preferredNamespaceUri
        else:
            return ""

    def get_version_iri(self):
        if hasattr(self.ontology.metadata, "versionIRI"):
            return self.ontology.metadata.versionIRI
        else:
            return ""

    def get_citation(self):
        if hasattr(self.ontology.metadata,"citation"):
            return self.ontology.metadata.citation
        else:
            return ""

    def get_title(self):
        if hasattr(self.ontology.metadata, "title"):
            return self.ontology.metadata.title
        else:
            return ""
    def get_metadata(self):
        list_metadata = []
        for metadata in self.ontology.metadata:
            if isinstance(metadata, AnnotationPropertyClass):
                list_metadata.append(metadata)
        return list_metadata

