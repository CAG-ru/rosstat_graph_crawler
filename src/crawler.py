import sys
import pandas as pd
import numpy as np
from src.connector import Graph, GraphNode
from src.parsers import *
from src.cos_sim import *


def crawl_graph(graph_id):
    try:
        graph_record = Graph().get_graph_record(graph_id)
        graph_node = GraphNode(graph_record)
        path = graph_node.path
        if graph_id == 55072:
            raise ValueError('обрабатывать вручную')
        parser = choose_parser(graph_node)
        tables = parser.get_tables_info()

        if len(tables) != 0:
            for table in tables:
                table.graph_id = graph_id
                table.path = path
            df_success = pd.DataFrame(data=[table.__dict__ for table in tables])
            df_success = df_success.replace(r'^\s*$', np.nan, regex=True)
            df_success = df_success.dropna(subset=['name'])
            df_success._name = 'df_success'
            return df_success
        else:
            message = 'таблицы в файле не найдены'
            df_failure = pd.DataFrame(data={'graph_id': [graph_id],
                                            'path': [path],
                                            'message': [message]})
            df_failure._name = 'df_failure'
            return df_failure
    except (ValueError, TypeError):
        message = str(sys.exc_info()[1])
        df_failure = pd.DataFrame(data={'graph_id': [graph_id],
                                        'path': [path],
                                        'message': [message]})
        df_failure._name = 'df_failure'
        return df_failure
