"""
This class is to let us load in cypher query files. These files are text files containing the queries.
"""

import os

class CypherQueryLoader:
    
    def __init__(self, query_directory):
        """
        Initialiser for this class:
        query_directory: file path to the directory contain all cypher queries
        """
        self.query_directory = query_directory

    def load_query(self, query_name):
        """
        Function to read in all cypher queries.
        query_name: the file name (without the file type) as all files to be read in via this function are meant to be of .cypher type
        """
        file_path = os.path.join(self.query_directory, f"{query_name}.cypher")
        with open(file_path, "r") as file:
            query = file.read()
        return query