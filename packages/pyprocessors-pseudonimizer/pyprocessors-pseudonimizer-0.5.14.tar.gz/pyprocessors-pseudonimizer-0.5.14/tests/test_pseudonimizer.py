import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_pseudonimizer.pseudonimizer import (
    PseudonimizerProcessor,
    PseudonimizerParameters, OPERATOR_IDENTITY_STR
)


def test_normalize():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/afp_ner_fr-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        formatter = PseudonimizerProcessor()
        options = PseudonimizerParameters()
        options.mapping = {
            'wikidata': OPERATOR_IDENTITY_STR,
            'afporganization': json.dumps({
                "type": "mask",
                "masking_char": "X",
                "chars_to_mask": 3,
                "from_end": False,
            })
        }
        anonymizeds = formatter.process([doc], options)
        norm_file = testdir / "data/afp_ner_fr-document-test-anon.json"
        dl = DocumentList(__root__=anonymizeds)
        with norm_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
