import json
from functools import lru_cache
from typing import List, Type, cast, Dict

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText

from .fakerop import FakerOp

OPERATOR_EXAMPLE1 = {
    "type": "mask",
    "masking_char": "*",
    "chars_to_mask": 12,
    "from_end": True,
}
OPERATOR_EXAMPLE1_STR = json.dumps(OPERATOR_EXAMPLE1, indent=2)

OPERATOR_EXAMPLE2 = {
    "type": "replace",
    "new_value": "_ANONYMIZED_"
}
OPERATOR_EXAMPLE2_STR = json.dumps(OPERATOR_EXAMPLE2, indent=2)

OPERATOR_LABEL = {
    "type": "label"
}
OPERATOR_LABEL_STR = json.dumps(OPERATOR_LABEL, indent=2)

OPERATOR_IDENTITY = {
    "type": "identity"
}
OPERATOR_IDENTITY_STR = json.dumps(OPERATOR_IDENTITY, indent=2)

CUSTOM_OPERATORS = {
    "identity": lambda x: x,
}

OPERATOR_FAKER = {
    "type": "faker",
    "provider": "name",
    "locale": "fr_FR"
}
OPERATOR_FAKER_STR = json.dumps(OPERATOR_FAKER, indent=2)


class PseudonimizerParameters(ProcessorParameters):
    mapping: Dict[str, str] = Field(None,
                                    description="List of anonymization/pseudonymization [operators](https://microsoft.github.io/presidio/tutorial/10_simple_anonymization/) like this ones:<br/><li>```" + OPERATOR_EXAMPLE1_STR + "```<li>```" + OPERATOR_EXAMPLE2_STR + "```<li>```" + OPERATOR_FAKER_STR + "```",
                                    extra="key:label,val:json")
    default_operator: str = Field(OPERATOR_LABEL_STR,
                                  description="""Default anonymization/pseudonymization operator to use if no explicit mapping is provided""",
                                  extra="json")
    as_altText: str = Field(
        "pseudonimization",
        description="""If defined generate the pseudonimization as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


def operator_from_annotation(a, definitions):
    default_def = definitions.get(None, None)
    label = a.labelName or a.label
    if label in definitions:
        definition = definitions[label]
        return operator_from_definition(a, definition)
    elif default_def is not None:
        return operator_from_definition(a, default_def)
    return None


def operator_from_definition(a, definition):
    type = definition['type']
    if type == 'label':
        replacement = f"<{a.label or a.labelName}>"
        return OperatorConfig("replace",
                              {"new_value": replacement})
    elif type == "faker":
        definition.pop("type")
        provider = definition.pop("provider")
        fakerop = FakerOp(provider, **definition)
        return OperatorConfig("custom", {"lambda": fakerop.evaluate})
    elif type in CUSTOM_OPERATORS:
        return OperatorConfig("custom", {"lambda": CUSTOM_OPERATORS[type]})
    else:
        return OperatorConfig.from_json(definition)


class PseudonimizerProcessor(ProcessorBase):
    """Pseudonimizer."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: PseudonimizerParameters = cast(PseudonimizerParameters, parameters)
        mapping = frozenset(params.mapping.items()) if params.mapping else None
        definitions = get_definitions(mapping, params.default_operator)
        engine = get_engine()
        operators: Dict[str, OperatorConfig] = {}
        try:
            for document in documents:
                if document.annotations:
                    analyzer_results = []
                    for a in document.annotations:
                        if a.status != "KO":
                            analyzer_results.append(
                                RecognizerResult(entity_type=a.labelName, start=a.start, end=a.end, score=a.score))
                            if a.labelName not in operators:
                                op = operator_from_annotation(a, definitions)
                                if op is not None:
                                    operators[a.labelName] = op
                    result = engine.anonymize(
                        text=document.text,
                        analyzer_results=analyzer_results,
                        operators=operators,
                    )
                    if params.as_altText is not None and len(params.as_altText):
                        document.altTexts = document.altTexts or []
                        altTexts = [
                            alt
                            for alt in document.altTexts
                            if alt.name != params.as_altText
                        ]
                        altTexts.append(AltText(name=params.as_altText, text=result.text))
                        document.altTexts = altTexts
                    else:
                        document.text = result.text
                        document.annotations = None
                        document.sentences = None
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PseudonimizerParameters


@lru_cache(maxsize=None)
def get_engine():
    return AnonymizerEngine()


@lru_cache(maxsize=None)
def get_definitions(mapping_items, default):
    definitions = {None: None}
    if default is not None and default.strip() != "":
        default_def = json.loads(default)
        definitions[None] = default_def
    if mapping_items:
        for pname, pvalue in mapping_items:
            op_def = json.loads(pvalue)
            definitions[pname] = op_def
    return definitions
