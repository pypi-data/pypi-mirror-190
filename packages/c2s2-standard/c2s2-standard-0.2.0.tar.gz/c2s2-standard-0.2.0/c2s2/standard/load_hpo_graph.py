import json
from urllib.request import urlopen

import networkx as nx


def get_hpo_graph_in_networkx(hpo_url: str = None, hpo_path: str = None) -> nx.DiGraph:
    """
    Obtain the HPO graph in networkx format
    :param hpo_url: path to the HPO json file.
    :param hpo_path:
    """
    if hpo_url:
        with urlopen(hpo_url, timeout=30) as uh:
            data = uh.read()
            hpo_json = json.loads(data.decode("utf-8"))
    elif hpo_path:
        with open(hpo_path) as fh:
            hpo_json = json.load(fh)
    else:
        raise ValueError(f'`hpo_url` or `hpo_path` must be provided')

    edge_list_in_json = hpo_json['graphs'][0]['edges']

    edge_list = []
    for edge in edge_list_in_json:
        # fix formatting to correspond to our wanted format
        # this does include obsolete terms, but does not add synonyms
        node_1 = edge['obj'].replace('http://purl.obolibrary.org/obo/', '').replace('_', ':')
        node_2 = edge['sub'].replace('http://purl.obolibrary.org/obo/', '').replace('_', ':')
        edge_list.append((node_1, node_2))

    G = nx.from_edgelist(edge_list, create_using=nx.DiGraph)

    obsolete_terms = []  # use a list to delete them all at once later and not call graph.remove_node each time
    for node in hpo_json['graphs'][0]['nodes']:
        term = node['id'].replace('http://purl.obolibrary.org/obo/', '').replace('_', ':')
        if 'meta' in node:
            if 'deprecated' in node['meta']:
                if node['meta']['deprecated']:
                    obsolete_terms.append(term)
        if term in G.nodes():
            G.nodes()[term]['label'] = node['lbl']

    G.remove_nodes_from(obsolete_terms)
    return G
