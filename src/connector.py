import configparser
import io
import os.path
import pathlib
import re
import psycopg2

from src.utils import *


class Graph:
    """класс, осуществляющий подключение к графу и чтение записей"""

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.connector = psycopg2.connect(config['database']['DB_CONFIG'])
        self.cursor = self.connector.cursor()

    def get_graph_record(self, graph_id):
        query_to_read = self.__generate_query_to_read(graph_id)
        self.cursor.execute(query_to_read)
        attribute_names = [desc[0] for desc in self.cursor.description]
        attribute_values = self.cursor.fetchone()
        graph_record = {attr: value for attr, value in zip(attribute_names, attribute_values)}
        return graph_record

    def __generate_query_to_read(self, graph_id):
        self.graph_id = self.__validate_graph_id(graph_id)
        query_to_read = ('SELECT * '
                         'FROM public.graph '
                         f'WHERE public.graph.id = {self.graph_id};')
        return query_to_read

    def search(self, text):
        query_to_search = self.__generate_query_to_search(text)
        self.cursor.execute(query_to_search)
        
        graph_attribute_names = [desc[0] for desc in self.cursor.description]
        graph_attribute_values = self.cursor.fetchone()
        graph_node_with_text = {attr: [] for attr in graph_attribute_names}
        while graph_attribute_values:
            for attr, value in zip(graph_attribute_names, graph_attribute_values):
                graph_node_with_text[attr].append(value)
            graph_attribute_values = self.cursor.fetchone()

        return graph_node_with_text

    def __generate_query_to_search(self, text):
        query_to_search = ('SELECT public.graph.id, public.graph.path '
                           'FROM public.graph '
                           f"WHERE public.graph.document LIKE '%{text}%';")
        return query_to_search

    def __validate_graph_id(self, graph_id):
        query_to_check = ('SELECT public.graph.id '
                          'FROM public.graph '
                          f'WHERE public.graph.id = {graph_id};')
        self.cursor.execute(query_to_check)
        if self.cursor.fetchone():
            return graph_id
        else:
            raise ValueError(f'graph.id {graph_id} не существует в таблице')

    def __del__(self):
        self.connector.close()


class GraphNode:
    """класс с информацией об узле графа"""

    def __init__(self, graph_record):
        self.id = graph_record['id']
        self.rootname = graph_record['rootname']
        self.level = graph_record['level']
        self.name = graph_record['name']
        self.path = graph_record['path']
        self.redirect = graph_record['redirect']
        self.parent = graph_record['parent']
        self.document = graph_record['document']
        self.file = graph_record['file']
        self.type = graph_record['type']
        self.done = graph_record['done']
        self.hash = graph_record['hash']
        self.href = graph_record['href']
        self.timestamp = graph_record['timestamp']
        self.file_ext = self.__get_file_ext(self.path)

    def save_file(self, path=None):
        content = io.BytesIO(self.file)
        file_name = str(self.id)

        if path is None:
            path = pathlib.Path().absolute()
        
        if self.file_ext:
            file_name += self.file_ext
        complete_path = os.path.join(path, file_name)

        if self.file_ext == '.htm':
            with open(complete_path, 'w') as f:
                content = self.document
                f.write(content)
        else:
            with open(complete_path, 'wb') as f:
                f.write(content.getbuffer())

    def __get_file_ext(self, path):
        match = ext_regex.search(path)
        if match:
            return match.group(1)
