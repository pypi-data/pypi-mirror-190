import typing

import numpy as np

from c2s2.base.consensus.simple import SimpleConsensusClustering
from c2s2.base.model import TermId
from c2s2.base.perturb import NoiseAdding
from c2s2.base.semsim import SimilarityMatrixCreator, Phenomizer, read_ic_mica_data
from c2s2.standard.cluster import SpectralClustering
from c2s2.standard.load_hpo_graph import get_hpo_graph_in_networkx
from c2s2.standard.parse_phenopackets import process_phenopackets_directory, PhenotypeAndDisease


def pp_with_one_disease_to_array(pp_data: typing.List[PhenotypeAndDisease]):
    ok = []
    for pp in pp_data:
        if len(pp.disease_ids) != 1:
            print(f'Skipping the phenopacket {pp.pp_id} with #diseases {len(pp.disease_ids)}!=1')
            continue
        ok.append([pp.term_ids, pp.term_labels, pp.disease_ids[0]])
    return np.array(ok)


if __name__ == "__main__":
    # TODO turn into unit test
    PHENOPACKETS_DIR = ""
    MICA_DICT_PATH = ""
    LOCAL_HPO_JSON = "path/to/local/hp.json"

    pp_data = process_phenopackets_directory(PHENOPACKETS_DIR)
    np_phenopackets = pp_with_one_disease_to_array(pp_data)

    #  lets start with the 4 largest diseases in the dataset
    unique, counts = np.unique(np_phenopackets[:, 2], return_counts=True)
    top_4_diseases = unique[np.argpartition(counts, -4)[-4:]]
    np_phenopackets = np_phenopackets[np.isin(np_phenopackets[:, 2], top_4_diseases)]
    np_phenopackets = np_phenopackets[np.argsort(np_phenopackets[:, 2])]

    print("Loaded " + str(len(np_phenopackets)) + " phenopackets.")
    hpo_list = np_phenopackets[:, 0]
    sim_kernel = Phenomizer(read_ic_mica_data(MICA_DICT_PATH))
    sim_matrix_creator = SimilarityMatrixCreator(sim_kernel)
    hpo_graph = get_hpo_graph_in_networkx(hpo_url="https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.json")
    perturb_method = NoiseAdding(number_of_terms_to_add=4, nodes=[TermId.of(node) for node in hpo_graph.nodes()])
    clustering_algorithm = SpectralClustering()
    consensus = SimpleConsensusClustering(k_clusters=6, n_resample=100, sim_matrix_creator=sim_matrix_creator,
                                          perturb_method=perturb_method, clustering_algorithm=clustering_algorithm)
    print("Initialized, now starting consensus clustering.")
    consensus.consensus_cluster(hpo_list)
    for i in range(len(consensus.k_clusters)):
        print(consensus.connectivity_matrix[i, :, :])
    print(consensus.pac)
