import os
from pkg_resources import resource_string, resource_listdir, resource_filename

class ResourcesManager:

    def get_resource(self,path) -> str:
        f = open(path, "r")
        return f.read()
