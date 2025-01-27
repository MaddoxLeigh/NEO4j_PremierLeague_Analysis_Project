import os

class CypherQueryLoader:
    def __init__(self, query_directory):
        self.query_directory = query_directory

    def load_query(self, query_name):
        file_path = os.path.join(self.query_directory, f"{query_name}.cypher")
        with open(file_path, "r") as file:
            query = file.read()
        return query