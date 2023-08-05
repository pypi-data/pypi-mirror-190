# A module with simple implementations of the model definitions.
import copy
import typing

from . import TermId
from ._base import Sample, PhenotypicFeature


class SimpleSample(Sample):

    def __init__(self, identifier: str,
                 phenotypic_features: typing.List[PhenotypicFeature] = None):
        self._id = identifier
        self._pfs = [] if phenotypic_features is None else phenotypic_features

    @property
    def identifier(self) -> str:
        return self._id

    @property
    def phenotypic_features(self) -> typing.List[PhenotypicFeature]:
        return self._pfs

    @phenotypic_features.setter
    def phenotypic_features(self, value: typing.List[PhenotypicFeature]):
        self._pfs = value

    def __copy__(self):
        # We pass along the identifier ref but we carbon copy each phenotypic feature
        return type(self)(self.identifier, [copy.copy(feature) for feature in self.phenotypic_features])

    def __repr__(self):
        return f'SimpleSample(identifier="{self.identifier}", phenotypic_features={self.phenotypic_features})'


class SimplePhenotypicFeature(PhenotypicFeature):

    def __init__(self, term_id: TermId, status: bool):
        self._tid = term_id
        self._status = status

    @property
    def term_id(self) -> TermId:
        return self._tid

    @term_id.setter
    def term_id(self, value: TermId):
        self._tid = value

    @property
    def status(self) -> bool:
        return self._status

    def __copy__(self):
        return type(self)(self.term_id, self.status)

    def __repr__(self):
        return f'SimplePhenotypicFeature(term_id={self.term_id}, status={self.status})'
