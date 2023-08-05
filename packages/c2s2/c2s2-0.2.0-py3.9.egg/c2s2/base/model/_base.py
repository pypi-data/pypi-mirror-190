# A module with data model definitions.

from abc import ABCMeta, abstractmethod
import typing


class TermId:
    """
    TermId is a value object that represents an ontology concept.

    TermId has two properties: `prefix` and `id`.
    """

    @staticmethod
    def of(value: str):
        idx = value.index(':')
        if idx < 0:
            raise ValueError(f'The value {value} has no colon')
        return TermId(value[:idx], value[idx + 1:])

    def __init__(self, prefix: str, id: str):
        self._prefix = prefix
        self._id = id

    def __hash__(self):
        return hash((self._prefix, self._id))

    def __eq__(self, other):
        if isinstance(other, TermId):
            return self._prefix == other._prefix and self._id == other._id
        return False

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def id(self) -> str:
        return self._id

    @property
    def value(self) -> str:
        return self.prefix + ':' + self.id

    def __eq__(self, other):
        if not isinstance(other, TermId):
            return False
        return self.prefix == other.prefix and self.id == other.id

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'TermId(prefix="{self.prefix}", id="{self.id}")'


class PhenotypicFeature(metaclass=ABCMeta):
    """
    PhenotypicFeature is a value object consisting of a `term_id` and `status` (observed/excluded)
    """

    @property
    @abstractmethod
    def term_id(self) -> TermId:
        pass

    @term_id.setter
    @abstractmethod
    def term_id(self, value: TermId):
        pass

    @property
    @abstractmethod
    def status(self) -> bool:
        """
        Observation status of the phenotypic feature.
        Returns `True` if the feature is observed and `False` if it is excluded.
        """
        pass

    def is_observed(self) -> bool:
        """
        Returns `True` if the phenotypic feature was *observed*.
        """
        return self.status

    def is_excluded(self) -> bool:
        """
        Return `True` if presence of the phenotypic feature was *excluded*.
        """
        return not self.status

    @abstractmethod
    def __copy__(self):
        """
        Phenotypic feature must support (shallow) copy to support modification in the perturb step.
        """
        pass

    def __eq__(self, other):
        """
        Two phenotypic features are equal if the `term_id` and `status` attributes are equal.
        """
        if not isinstance(other, PhenotypicFeature):
            return False
        return self.term_id == other.term_id and self.status == other.status

    def __str__(self):
        return f'PhenotypicFeature(term_id={self.term_id}, status={self.status})'
    # TODO - add additional attributes?

    def __hash__(self):
        return hash((self.term_id, self.status))


class Phenotyped(metaclass=ABCMeta):

    @property
    @abstractmethod
    def phenotypic_features(self) -> typing.List[PhenotypicFeature]:
        pass

    @phenotypic_features.setter
    @abstractmethod
    def phenotypic_features(self, value: typing.List[PhenotypicFeature]):
        pass


class Identified(metaclass=ABCMeta):

    @property
    @abstractmethod
    def identifier(self) -> str:
        pass


class Sample(Phenotyped, Identified, metaclass=ABCMeta):

    @abstractmethod
    def __copy__(self):
        """
        Sample must support (shallow) copy to support modification in the perturb step.
        """
        pass

    def __str__(self):
        return f'Sample(identifier="{self.identifier}", n_features={len(self.phenotypic_features)})'
