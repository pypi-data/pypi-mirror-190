import typing
import numpy as np
from c2s2.base.explain import ExplainMethod, fisher_freeman_halton
from c2s2.base.model import Sample, TermId, PhenotypicFeature
from c2s2.base.model.simple import SimplePhenotypicFeature
import networkx as nx
import copy


class FisherFreemanHalton(ExplainMethod):
    """
     Perform the Fisher-Freeman-Halton test on all combinations of prevalence of HPO terms between
     detected clusters to find the differences between them
    """

    def __init__(self, hpo_graph: nx.DiGraph, use_bonferroni: bool =True):
        self._use_bonferroni = use_bonferroni
        self._hpo_graph = hpo_graph

    def explain(self, samples: typing.Sequence[Sample], cluster_labels: np.ndarray) -> tuple[
        list[PhenotypicFeature], np.ndarray, float]:
        """Explain differences using Fisher-Freeman-Halton test on the detected clusters
        samples : the samples to detect the difference for
        cluster_labels: the determined labels of the clusters
        hpo_graph: the HPO graph in networkx format
        """
        assert (len(samples) == len(cluster_labels))
        all_included_features = []

        samples_with_positive_ancestors = []
        for sample in samples:
            sample = self.make_ancestors_positive(sample, self._hpo_graph)
            samples_with_positive_ancestors.append(sample)

        for sample in samples_with_positive_ancestors:
            all_included_features.extend(sample.phenotypic_features)

        #  remove duplicates in this list
        all_included_features = list(set(all_included_features))

        # now that we have every unique feature, create 2xk table with prevalence
        np_contingency = np.zeros((len(all_included_features), 2, len(np.unique(cluster_labels))), dtype=int)

        samples_with_positive_ancestors = np.array(samples_with_positive_ancestors)
        for i, phenotypic_feature in enumerate(all_included_features):
            for j, cluster in enumerate(np.unique(cluster_labels)):
                total_in_this_cluster = np.sum(cluster_labels == cluster)
                pos_this_cluster = 0
                for sample in samples_with_positive_ancestors[cluster_labels == cluster]:
                    pos_this_cluster += phenotypic_feature in sample.phenotypic_features
                neg_this_cluster = total_in_this_cluster - pos_this_cluster
                np_contingency[i, 0, j] = pos_this_cluster
                np_contingency[i, 1, j] = neg_this_cluster

        p_threshold = 0.05
        if self._use_bonferroni:
            p_threshold = p_threshold / len(all_included_features)

        np_contingency_sig, sig_features = [], []
        for i in range(len(all_included_features)):
            # now run FFH test for every phenotypic feature
            result_ffh = fisher_freeman_halton(np_contingency[i, :, :])
            if result_ffh['p'] < p_threshold and not np.isinf(result_ffh['t']):
                sig_features.append(all_included_features[i])
                np_contingency_sig.append(np_contingency[i, :, :])
        return sig_features, np.array(np_contingency_sig, dtype=int), p_threshold

    @staticmethod
    def make_ancestors_positive(sample: Sample, hpo_graph: nx.DiGraph) -> Sample:
        copy_sample = copy.copy(sample)
        features_to_be_added = []
        for feature in copy_sample.phenotypic_features:
            for ancestor in list(nx.ancestors(hpo_graph, feature.term_id.value)):
                features_to_be_added.append(SimplePhenotypicFeature(term_id=TermId.of(ancestor), status=True))
        copy_sample.phenotypic_features.extend(features_to_be_added)
        # remove duplicates to not count features twice later
        copy_sample.phenotypic_features = list(set(copy_sample.phenotypic_features))
        return copy_sample
