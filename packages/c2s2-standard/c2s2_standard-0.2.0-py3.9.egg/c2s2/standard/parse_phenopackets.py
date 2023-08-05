import os
import typing
from collections import namedtuple
from glob import glob

from google.protobuf.json_format import Parse
from phenopackets import Phenopacket

PhenotypeAndDisease = namedtuple('PhenotypeAndDisease', ['pp_id', 'term_ids', 'term_labels', 'disease_ids'])


def get_hpo_from_phenopacket(phenopacket: Phenopacket) -> PhenotypeAndDisease:
    """
    Get ids and labels of non-excluded phenotype terms and diseases from a phenopacket

    :param phenopacket: phenopacket object

    """
    hpo_ids, hpo_labels = [], []
    for feature in phenopacket.phenotypic_features:
        if not feature.excluded:
            hpo_ids.append(feature.type.id)
            hpo_labels.append(feature.type.label)

    assert len(hpo_ids) == len(hpo_labels)  # these should be same length

    omim_diagnoses = []
    for disease in phenopacket.diseases:
        omim_diagnoses.append(disease.term.id)
    return PhenotypeAndDisease(phenopacket.id, hpo_ids, hpo_labels, omim_diagnoses)


def process_phenopackets_directory(path_to_dir) -> typing.List[PhenotypeAndDisease]:
    """
    Get all phenopackets in a directory and extract phenotypic features and diseases.

    :param path_to_dir: path to directory with phenopackets v2
    :return: a list of phenotype and disease objects
    """
    files_in_dir = glob(os.path.join(path_to_dir, '*.json'))

    data = []

    for file_path in files_in_dir:
        phenopacket = _read_phenopacket(file_path)
        if not phenopacket:
            raise ValueError(f"Unable to decode phenopacket at {file_path}")

        ph_data = get_hpo_from_phenopacket(phenopacket)
        data.append(ph_data)

    return data


def _read_phenopacket(json_path):
    """Decode phenopacket JSON into Protobuf object trying `utf-8` and `utf-16` encodings.
    Returns `None` if the decoding fails.
    """
    encodings = ['utf-8', 'utf-16']  # can add more if necessary
    for encoding in encodings:
        try:
            with open(json_path, 'r', encoding=encoding) as jsfile:
                return Parse(message=Phenopacket(), text=jsfile.read())
        except UnicodeDecodeError:
            pass

    return None
