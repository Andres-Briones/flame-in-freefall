import pytest

from fif import api, psi
from fif.questions import QUESTIONS

pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "tests.parquet").exists(), reason="processed tables not built")


def _empty(data):
    if isinstance(data, dict):
        return all(_empty(v) for v in data.values() if isinstance(v, (list, dict))) if any(
            isinstance(v, (list, dict)) for v in data.values()) else not data
    return not data


@pytest.mark.parametrize("q", QUESTIONS, ids=lambda q: q["question"][:50])
def test_question_returns_a_cited_answer(q):
    result = api.FUNCTIONS[q["function"]](**q["arguments"])
    assert not _empty(result["data"])
    assert result["sources"]
    assert q["answer"]
