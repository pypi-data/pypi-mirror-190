import typing

from c2s2.base.model import TermId
from c2s2.base.model.simple import SimpleSample, SimplePhenotypicFeature


def get_simple_samples() -> typing.List[SimpleSample]:
    """
    Prepare 20 simulated samples with phenotypic features sampled from 4 HPO organ system branches: cardiac,
    neurological, renal, and skeletal. There are 5 samples per branch.

    :return: a list of 20 simulated samples.
    """
    return [
        # Cardiac
        _make_sample("cardiac_1", ['HP:0002647', 'HP:0001631', 'HP:0001640', 'HP:0001638', 'HP:0011675', 'HP:0001635']),
        _make_sample("cardiac_2", ['HP:0045017', 'HP:0011723', 'HP:0001635', 'HP:0001662', 'HP:0001638', 'HP:0031657']),
        _make_sample("cardiac_3", ['HP:0010954', 'HP:0031664', 'HP:0012819', 'HP:0005170', 'HP:0001961', 'HP:0031861', 'HP:0001649', 'HP:0001635', 'HP:0031670', 'HP:0045017']),
        _make_sample("cardiac_4", ['HP:0001639', 'HP:0031668', 'HP:0011550', 'HP:0001961', 'HP:0001644', 'HP:0004383', 'HP:0001695', 'HP:0001640', 'HP:0012722']),
        _make_sample("cardiac_5", ['HP:0001631', 'HP:0004942', 'HP:0001678', 'HP:0031653', 'HP:0005162', 'HP:0001961', 'HP:0031664']),

        # Neurological
        _make_sample("neurological_1", ['HP:0001270', 'HP:0000717', 'HP:0001263', 'HP:0020221', 'HP:0000709', 'HP:0002376', 'HP:0010864', 'HP:0001290']),
        _make_sample("neurological_2", ['HP:0002353', 'HP:0001263', 'HP:0000750', 'HP:0000297']),
        _make_sample("neurological_3", ['HP:0010819', 'HP:0002194', 'HP:0003808', 'HP:0002015', 'HP:0000750', 'HP:0001270']),
        _make_sample("neurological_4", ['HP:0002376', 'HP:0002076', 'HP:0007281', 'HP:0012758', 'HP:0006829', 'HP:0002315', 'HP:0025373']),
        _make_sample("neurological_5", ['HP:0007193', 'HP:0000750', 'HP:0001290', 'HP:0002187', 'HP:0001270', 'HP:0006852', 'HP:0010819']),

        # Renal
        _make_sample("renal_1", ['HP:0032417', 'HP:0000384', 'HP:0005564', 'HP:0000126']),
        _make_sample("renal_2", ['HP:0031263', 'HP:0000105', 'HP:0025418', 'HP:0000075']),
        _make_sample("renal_3", ['HP:0005580', 'HP:0000095', 'HP:0004724', 'HP:0032950', 'HP:0000105']),
        _make_sample("renal_4", ['HP:0012582', 'HP:0008776', 'HP:0000077', 'HP:0100581', 'HP:0032599', 'HP:0000835', 'HP:0031264']),
        _make_sample("renal_5", ['HP:0032620', 'HP:0031264', 'HP:0033130', 'HP:0008776', 'HP:0005584', 'HP:0008341', 'HP:0033261', 'HP:0000091', 'HP:0012210']),

        # Skeletal
        _make_sample("skeletal_1", ['HP:0003025', 'HP:0006028', 'HP:0005871', 'HP:0030294']),
        _make_sample("skeletal_2", ['HP:0003923', 'HP:0003915', 'HP:0002834', 'HP:0003917', 'HP:0030309', 'HP:0003922']),
        _make_sample("skeletal_3", ['HP:0004016', 'HP:0004026', 'HP:0004019', 'HP:0004021', 'HP:0004018']),
        _make_sample("skeletal_4", ['HP:0004026', 'HP:0009809', 'HP:0003951', 'HP:0003922']),
        _make_sample("skeletal_5", ['HP:0003910', 'HP:0005092', 'HP:0004979', 'HP:0004980']),
    ]


def _make_sample(identifier: str, features: typing.Sequence[str]) -> SimpleSample:
    phenotypic_features = [SimplePhenotypicFeature(term_id=TermId.of(feature), status=True) for feature in features]
    return SimpleSample(identifier=identifier, phenotypic_features=phenotypic_features)

