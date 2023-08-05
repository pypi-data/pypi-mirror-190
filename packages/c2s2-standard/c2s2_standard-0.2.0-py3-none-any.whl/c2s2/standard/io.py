import io
import typing

from google.protobuf.json_format import Parse
from google.protobuf.message import Message
from phenopackets import Phenopacket, Cohort

from c2s2.base.model import Sample
from c2s2.base.model.simple import SimpleSample, SimplePhenotypicFeature, TermId

# A generic type for a Protobuf message
MESSAGE = typing.TypeVar('MESSAGE', bound=Message)


def read_phenopacket(phenopacket: typing.Union[Phenopacket, typing.IO, str]) -> Sample:
    """
    Read Phenopacket into a `c2s2.model.Sample`.

    :param phenopacket: a Phenopacket object, path to a phenopacket JSON file, or an IO wrapper.
    :return: the parsed `c2s2.model.Sample`.
    :raises: IOError in case of IO issues or a ValueError if the input is not a proper `Phenopacket`
    """
    if not isinstance(phenopacket, Message):
        phenopacket = _read_message(phenopacket, Phenopacket())
    return _parse_phenopacket(phenopacket)


def _parse_phenopacket(phenopacket: Phenopacket) -> Sample:
    """
    Extract the relevant parts of a `Phenopacket` into `c2s2.model.Sample`. The function uses `subject.id` for
    the `sample.identifier` and the `type.id` and `excluded` attributes of phenopacket's `PhenotypicFeature`s
    for `sample.phenotypic_features`.

    :raises: a `ValueError` if the input is not a `Phenopacket`.
    """
    if not isinstance(phenopacket, Phenopacket):
        raise ValueError(f'Expected an argument with type {Phenopacket} but got {type(phenopacket)}')
    identifier = phenopacket.subject.id
    phenotypic_features = []
    for feature in phenopacket.phenotypic_features:
        term_id = TermId.of(feature.type.id)
        observed = not feature.excluded
        pf = SimplePhenotypicFeature(term_id, status=observed)
        phenotypic_features.append(pf)

    return SimpleSample(identifier, phenotypic_features)


def read_cohort(cohort: typing.Union[Cohort, typing.IO, str]) -> typing.Sequence[Sample]:
    """
    Read Cohort into a `c2s2.model.Sample`.

    :param cohort: a Cohort object, path to a cohort JSON file, or an IO wrapper.
    :return: a sequence of `c2s2.model.Sample`s corresponding to Cohort members.
    :raises: IOError in case of IO issues or a ValueError if the input is not a proper `Cohort`.
    """
    if not isinstance(cohort, Message):
        cohort = _read_message(cohort, Cohort())
    return _parse_cohort(cohort)


def _parse_cohort(cohort: Cohort) -> typing.Sequence[Sample]:
    """
    Extract `c2s2.model.Sample`s from a `Cohort` into a sequence of `c2s2.model.Sample`s.
    Each cohort member is transformed into one `c2s2.model.Sample`.

    :raises: a `ValueError` if the input is not a `Cohort`.
    """
    if not isinstance(cohort, Cohort):
        raise ValueError(f'Expected an argument with type {Cohort} but got {type(cohort)}')
    return [_parse_phenopacket(member) for member in cohort.members]


def _read_message(fh: typing.Union[typing.IO, str], message: MESSAGE) -> MESSAGE:
    if isinstance(fh, str):
        with open(fh, 'r', encoding='utf-8') as handle:
            return _read_message(handle, message)
    elif isinstance(fh, io.TextIOBase):
        return Parse(fh.read(), message)
    elif isinstance(fh, io.BufferedIOBase):
        return Parse(fh.read().decode('utf-8'), message)
    else:
        raise ValueError(f'Expected either a path to phenopacket JSON or an IO wrapper but received {type(fh)}')
