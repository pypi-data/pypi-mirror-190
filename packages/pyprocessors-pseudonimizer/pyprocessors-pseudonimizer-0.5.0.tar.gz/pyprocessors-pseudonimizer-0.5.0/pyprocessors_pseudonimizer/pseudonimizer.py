from functools import lru_cache
from typing import List, Type, cast, Dict

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText


class PseudonimizerParameters(ProcessorParameters):
    as_altText: str = Field(
        "pseudonimization",
        description="""If defined generate the pseudonimization as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


class PseudonimizerProcessor(ProcessorBase):
    """Pseudonimizer."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: PseudonimizerParameters = cast(PseudonimizerParameters, parameters)
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
                                replacement = f"<{a.label or a.labelName}>"
                                operators[a.labelName] = OperatorConfig("replace",
                                                                        {"new_value": replacement})
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
