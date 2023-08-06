from llama.engine.nodes import (
    CheckMatchNode,
    ValueNode,
    LlamaNode,
    MetricNode,
    GetFieldNode,
    MergeNode,
    Node,
)

from llama.metrics.metric import Metric
from llama.specification.base_specification import BaseSpecification

from tqdm import tqdm

import inspect


class HyperLlamaEngine:
    def __init__(self):
        self.graph = Graph(self)
        self.temperature = 0.0
        self.use_examples = True
        self.input_value = None
        self.log = []

    def get_node(self, input):
        if isinstance(input, type):
            input_node = self.get_input(input)
        elif isinstance(input, BaseSpecification):
            input_node = input._node
            if input_node.graph is None:
                input_value = self.graph.add_node(input_node)
                self.input_value = input
        else:
            assert isinstance(input, Node), type(input)
            input_node = input

        return input_node

    def get_input(self, input_spec):
        input_node = self.get_value_node(input_spec)
        self.graph.add_node(input_node)
        return input_node

    def get_value_node(self, input_spec):
        input_value = ValueNode(input_spec)
        return input_value

    def predict(self, input, output_spec):
        node = self.get_node(input)

        # print("running on input node", node)

        # check for duplicates
        for llama_node in self.graph.nodes:
            if type(llama_node) != LlamaNode:
                continue

            if llama_node.input_spec != node.get_type():
                continue

            if llama_node.output_spec != output_spec:
                continue

            return llama_node

        llama_node = self.graph.add_node(LlamaNode(node.get_type(), output_spec))

        self.graph.connect(node, llama_node)

        return llama_node

    def merge(self, a, b, output_spec):
        node_a = self.get_node(a)
        node_b = self.get_node(b)

        llama_node = self.graph.add_node(
            MergeNode(node_a.get_type(), node_b.get_type(), output_spec)
        )

        self.graph.connect(node_a, llama_node)
        self.graph.connect(node_b, llama_node)

        return llama_node

    def add_metric(
        self, input, metric_spec=None, fit: bool = True, higher_is_better: bool = True
    ):

        if isinstance(input, Metric):
            assert metric_spec is None
            metric_spec = input.get_metric_spec()
            input = input.get_metric_input(self)

        metric_node = self.graph.add_node(
            MetricNode(
                input.get_type(),
                metric_spec,
                fit=fit,
                higher_is_better=higher_is_better,
            )
        )

        self.graph.connect(input, metric_node)

        return metric_node

    def get_field(self, input, field_name):
        get_field_node = self.graph.add_node(GetFieldNode(input.get_type(), field_name))

        self.graph.connect(input, get_field_node)

        return get_field_node

    def check_match(self, a, b):
        check_match_node = self.graph.add_node(CheckMatchNode(a, b))

        self.graph.connect(a, check_match_node)
        self.graph.connect(b, check_match_node)

        return check_match_node

    def fit(self, examples=[]):
        if len(examples) == 0:
            return

        example_groups = self.sort_examples_into_groups(examples)

        for examples in example_groups:
            # find a matching llm to fit
            input_spec = type(examples[0]["input"])
            output_spec = type(examples[0]["output"])

            matching_node = None

            for node in self.graph.nodes:
                #print("checking node", node)
                if type(node) != LlamaNode and type(node) != MetricNode:
                    continue

                if input_spec != node.input_spec:
                    continue

                if output_spec != node.output_spec:
                    continue

                #print("matched node", node)
                matching_node = node

            if matching_node is None:
                raise RuntimeError(
                    "could not find matching node for input_type="
                    + str(input_spec)
                    + ", output_type="
                    + str(output_spec)
                )

            matching_node.fit(examples)

    def sort_examples_into_groups(self, examples):
        groups = {}
        for example in examples:
            key = (type(example["input"]), type(example["output"]))

            if not key in groups:
                groups[key] = []

            groups[key].append(example)

        return groups.values()

    def optimize(self):
        # skip optimization if there are no metrics
        if len(self.get_metric_nodes()) == 0:
            return

        # Generate data at higher tempurature, log it

        for i in tqdm(range(3)):
            self.use_examples = i % 2 == 0
            self.temperature = 0.3 * (i + 1)
            self.execute(node=None)
            self.log_data()

        self.temperature = 0.0
        self.use_examples = True

        # Find best examples according to metrics
        best_results = None
        best_metric_so_far = float("-inf")

        for saved_values in self.log:
            for index, value in saved_values.items():
                node = self.graph.nodes[index]
                if type(node) == MetricNode:
                    field_name = next(iter(node.output_spec.__fields__.keys()))
                    metric_value = value._get_attribute_raw(field_name)

                    if node.higher_is_better:
                        is_best = best_metric_so_far <= metric_value
                    else:
                        is_best = best_metric_so_far > metric_value

                    if is_best:
                        best_results = saved_values
                        best_metric_so_far = metric_value
                        # print("Best metric value", metric_value, saved_values)

        # Fit on best results
        examples = []
        for index, value in best_results.items():
            node = self.graph.nodes[index]
            if type(node) == LlamaNode:
                predecessor = node.get_predecessors()[0]
                examples.append({"input": best_results[predecessor], "output": value})

        # print("Fitting on", examples)
        self.fit(examples)

    def execute(self, node):
        self.values = {}

        nodes = self.get_nodes_to_execute(node)

        self.setup_input(node, nodes)

        # print("Running this program", node, nodes)

        for node in nodes:
            # print("executing node", node.get_index(), node)
            # print("predecessors", node.get_predecessors())
            inputs = self.get_node_inputs(node)
            node.set_inputs(inputs)
            value = node.execute()
            self.values[node.get_index()] = value
            # print("values[" + str(node.get_index()) + "] are", self.values)

    def setup_input(self, output_node, nodes):
        # find an appropriate input node for this program
        node = None
        for program_node in nodes:
            if type(program_node) == ValueNode:
                assert (
                    node is None
                ), "TODO: support input setup for programs with multiple inputs"
                node = program_node

        # print("Setting up input for node", node, node.get_index(), self.input_value)

        node.value = self.input_value
        self.graph.set_input(node)

    def get_nodes_to_execute(self, node):
        # remove notes not used
        visited = set()
        required_nodes = self.get_metric_nodes()

        if not node is None:
            required_nodes += [node]
            visited.add(node.get_index())

        to_visit = list(required_nodes)

        while len(to_visit) > 0:
            current_node = to_visit.pop()

            predecessors = current_node.get_predecessors()
            for predecessor in predecessors:
                if predecessor in visited:
                    continue

                visited.add(predecessor)

                predecessor_node = self.graph.nodes[predecessor]

                required_nodes.append(predecessor_node)

                to_visit.append(predecessor_node)

        # topological sort
        ready = set()
        visited = set()
        scheduled = []

        while len(scheduled) < len(required_nodes):
            for current_node in required_nodes:
                predecessors = current_node.get_predecessors()
                node_is_ready = True
                for predecessor in predecessors:
                    if predecessor not in ready:
                        node_is_ready = False
                        break

                if node_is_ready and not current_node.get_index() in visited:
                    ready.add(current_node.get_index())
                    scheduled.append(current_node)
                    visited.add(current_node.get_index())

        return scheduled

    def get_metric_nodes(self):
        return [node for node in self.graph.nodes if type(node) == MetricNode]

    def get_node_inputs(self, node):
        predecessors = node.get_predecessors()

        return [self.values[predecessor] for predecessor in predecessors]

    def log_data(self):
        self.log.append(self.values)

    def get_value(self, index):
        return self.values[index]

    def metrics(self):
        return self.log

    def make_program(self, input):
        return Program(self, input)

    def model(self, function):
        signature = inspect.signature(function)
        input_spec = next(iter(signature.parameters.values())).annotation
        return self.make_program(function(input_spec))


class Program:
    def __init__(self, engine, output_value):
        self.engine = engine
        self.output_value = output_value

    def __call__(self, input):
        self.engine.input_value = input
        self.engine.graph.update_input_node(input._node)
        return self.output_value


class Graph:
    def __init__(self, engine):
        self.engine = engine
        self.input_node = None
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        # print("Added node", node)
        node.set_graph(self)
        self.nodes.append(node)
        return node

    def set_input(self, node):
        self.input_node = node

    def connect(self, a, b):
        self.edges.append((a.get_index(), b.get_index()))

    def update_input_node(self, node):
        if self.input_node == node:
            return

        if node.graph != self:
            self.add_node(node)

        if self.input_node is not None:
            updated_edges = [
                edge for edge in self.edges if edge[0] == self.input_node.get_index()
            ]
            self.edges = [
                edge for edge in self.edges if edge[0] != self.input_node.get_index()
            ]

            for edge in updated_edges:
                self.edges.append((node.get_index(), edge[1]))

        self.input_node = node
