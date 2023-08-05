import typing
from abc import ABCMeta, abstractmethod
from copy import copy

import networkx as nx
import numpy as np

from c2s2.base.model import Sample, TermId, PhenotypicFeature
from c2s2.base.perturb import Perturbation


class BaseImprecision(Perturbation, metaclass=ABCMeta):

    def __init__(self, hpo_graph: nx.DiGraph, number_of_terms_to_replace: int):
        self._hpo_graph: nx.DiGraph = hpo_graph
        if number_of_terms_to_replace <= 0:
            raise ValueError(f'Number of terms to replace {number_of_terms_to_replace} must be greater than 0')
        self._number_of_terms_to_replace = number_of_terms_to_replace

    def perturb(self, samples: typing.Sequence[Sample]) -> typing.Sequence[Sample]:
        perturbed_items = []

        for sample in samples:
            # We must not alter the original sample
            perturbed = copy(sample)

            # We can sample at most all phenotypic features for this sample.
            terms_to_replace = min(len(perturbed.phenotypic_features), self._number_of_terms_to_replace)

            # Sample n phenotypic feature indices without replacement
            pf_idxs = np.random.choice(len(perturbed.phenotypic_features), size=terms_to_replace, replace=False)

            for i in pf_idxs:
                pf: PhenotypicFeature = perturbed.phenotypic_features[i]
                # Replace in place. No issue since we cloned above
                pf.term_id = self._find_replacement(pf)

            perturbed_items.append(perturbed)

        return perturbed_items

    @abstractmethod
    def _find_replacement(self, pf: PhenotypicFeature) -> TermId:
        pass


class NLevelsUpImprecision(BaseImprecision):
    """
    The pertuber chooses n HPO terms and replaces them with their ancestor (a less specific term)
    to simulate imprecision. The number of hops up the ancestry chain(s) is controlled by the `level` hyperparameter.
    Use `1` for parent, `2` for grandparent, and so on.
    """

    def __init__(self, hpo_graph: nx.DiGraph,
                 number_of_terms_to_replace: int,
                 level: int = 1):
        """
        Create the pertuber.

        :param hpo_graph: HPO graph
        :param number_of_terms_to_replace:
        :param level: number of levels to go (1 for parent, 2 for grand-parent, etc.)
        """
        super().__init__(hpo_graph, number_of_terms_to_replace)
        if level <= 0:
            raise ValueError(f'Level {level} must be greater than 0')
        self._level = level

    def _find_replacement(self, pf: PhenotypicFeature) -> TermId:
        current = pf.term_id.value

        for _ in range(self._level):
            ancestors = list(self._hpo_graph.predecessors(current))
            if ancestors:
                # The term may have multiple parents. Choose one randomly
                current = np.random.choice(ancestors)
            else:
                # We must have hit the root term
                break

        return TermId.of(current)


class Imprecision(NLevelsUpImprecision):
    """
    Replace n phenotypic features with their direct ancestors/parents. In case of multiple parents, the term
    is sampled randomly.
    If the sample has less than n phenotypic features, all features are replaced.

    The perturber is a special case of `NLevelsUpImprecision` where `level=1`.
    """

    def __init__(self, hpo_graph: nx.DiGraph, number_of_terms_to_replace: int):
        """
        Create imprecision perturber.

        :param hpo_graph: the HPO graph
        :param number_of_terms_to_replace: number of HPO terms to replace by ancestor terms
        """
        super().__init__(hpo_graph, number_of_terms_to_replace, level=1)
