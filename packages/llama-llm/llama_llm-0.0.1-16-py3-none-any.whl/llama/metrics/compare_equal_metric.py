
from llama.metrics.metric import Metric
from llama.specification.base_specification import BaseSpecification
from llama.specification.context import Context

class Match(BaseSpecification):
    a: str = Context("the first string")
    b: str = Context("the second string")

class MatchResult(BaseSpecification):
    similarity: float = Context(
        "a number between 0.0 and 1.0 describing similarity of the input strings.  0.0 is no similarity, and 1.0 is a perfect match."
    )


class CompareEqualMetric(Metric):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_metric_input(self, engine):
        return engine.merge(self.a, self.b, output_spec=Match)

    def get_metric_spec(self):
        return MatchResult

