from llama.specification.specification import Spec

from powerml import PowerML

from docstring_parser import parse

 # TODO: confirm what cue works best for lists
LIST_CUE = '-'
# LIST_CUE = '1.'

SEPARATOR = '\n'

def run(input: Spec, output_spec: Spec):
    prompt = make_prompt(input, output_spec)
    prompt = apply_cue(prompt, output_spec)

    result = PowerML().predict(prompt)

    return parse_cue(result, output_spec)


def make_prompt(input, output_spec):
    #print("Docstring", input.__doc__)
    parsed = parse(input.__doc__)

    prompt = parsed.short_description + SEPARATOR
    for param in parsed.params:
        prompt += param.description + " is " + get_arg(input, param.arg_name) + SEPARATOR

    parsed = parse(output_spec.__doc__)
    prompt += f"{SEPARATOR}Generate {parsed.short_description}{SEPARATOR}"

    return prompt

def apply_cue(input, output_spec):
    parsed = parse(output_spec.__doc__)
    output_names = list(output_spec.__annotations__.keys())
    output_types = list(output_spec.__annotations__.values())
    for i, output_type in enumerate(output_types):
        if output_type == list:
            input += f"{LIST_CUE}"
        else:
            input += f"with {parsed.params[i].description} after '{output_names[i]}:'{SEPARATOR}"
    
    return input

def parse_cue(output, output_spec):
    if len(output_spec.__fields__) == 1:
        output_type = list(output_spec.__annotations__.values())[0]
        if output_type == list:
            output = [el.strip() for el in output.split(LIST_CUE)]
        else:
            output = output_type(output.strip())
        return output
    else:
        output_values = {}
        remainder = output
        for key_cue in reversed(output_spec.__annotations__):
            remainder, _, value_cue = remainder.partition(f"{key_cue}:")
            output_values[key_cue] = value_cue.strip()
        return output_spec.parse_obj(output_values)

def get_arg(input, name):
    value = input.dict().get(name)

    return str(value)