
from llama.engine.nodes import CheckMatchNode, ValueNode, LlamaNode, MetricNode, GetFieldNode

from llama.specification.base_specification import BaseSpecification

from tqdm import tqdm

class HyperLlamaEngine:
    def __init__(self):
        self.graph = Graph(self)
        self.temperature = 0.0
        self.use_examples = True
        self.log = []

    def get_node(self, input):
        if isinstance(input, type):
            input_node = self.get_input(input)
        elif isinstance(input, BaseSpecification):
            input_node = input._node
            if input_node.graph is None:
                input_value = self.graph.add_node(input_node)
                input_value.value = input
                self.graph.set_input(input_value)

        return input_node

    def get_input(self, input_spec):
        input_node = self.get_value_node(input_spec)
        input_value = self.graph.add_node(input_node)
        self.graph.set_input(input_value)
        return input_value

    def get_value_node(self, input_spec):
        input_value = ValueNode(input_spec)
        return input_value

    def run(self, input, output_spec):
        node = self.get_node(input)

        #print("running on input node", node)

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

    def add_metric(self, input, metric_spec):
        metric_node = self.graph.add_node(MetricNode(input.get_type(), metric_spec))

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

    def fit(self, examples):
        if len(examples) == 0:
            return

        # find a matching llm to fit
        input_spec = type(examples[0]["input"])
        output_spec = type(examples[0]["output"])

        matching_node = None

        for node in self.graph.nodes:
            #print("checking node", node)
            if type(node) != LlamaNode:
                continue

            if input_spec != node.input_spec:
                continue

            if output_spec != node.output_spec:
                continue

            matching_node = node

        return matching_node.fit(examples)

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
                    metric_value = getattr(value, field_name)
                    if best_metric_so_far <= metric_value:
                        best_results = saved_values
                        best_metric_so_far = metric_value
                        #print("Best metric value", metric_value, saved_values)

        # Fit on best results
        examples = []
        for index, value in best_results.items():
            node = self.graph.nodes[index]
            if type(node) == LlamaNode:
                predecessor = node.get_predecessors()[0]
                examples.append({"input" : best_results[predecessor], "output" : value})

        #print("Fitting on", examples)
        self.fit(examples)


    def execute(self, node):
        self.values = {}

        nodes = self.get_nodes_to_execute(node)

        #print("Running this program", node, nodes)

        for node in nodes:
            #print("executing node", node.get_index(), node)
            inputs = self.get_node_inputs(node)
            node.set_inputs(inputs)
            value = node.execute()
            self.values[node.get_index()] = value

    def get_nodes_to_execute(self, node):
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

        return sorted(required_nodes, key=lambda x: x.get_index())

    def get_metric_nodes(self):
        return [node for node in self.graph.nodes if type(node) == MetricNode ]

    def get_node_inputs(self, node):
        predecessors = node.get_predecessors()

        return [self.values[predecessor] for predecessor in predecessors]

    def log_data(self):
        self.log.append(self.values)

    def get_value(self, index):
        return self.values[index]

    def get_metrics(self):
        return self.values

    def make_program(self, input):
        return Program(self, input)

class Program:
    def __init__(self, engine, output_value):
        self.engine = engine
        self.output_value = output_value

    def __call__(self, input):
        self.engine.graph.input_node.value = input
        return self.output_value

class Graph:
    def __init__(self, engine):
        self.engine = engine
        self.input_node = None
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        node.set_graph(self)
        self.nodes.append(node)
        return node

    def set_input(self, node):
        self.input_node = node

    def connect(self, a, b):
        self.edges.append((a.get_index(), b.get_index()))


