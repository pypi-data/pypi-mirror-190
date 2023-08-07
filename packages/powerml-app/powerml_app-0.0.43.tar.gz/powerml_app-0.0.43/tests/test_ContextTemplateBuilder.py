from powerml import ContextTemplate
from powerml import LLM
from powerml import ContextTemplateBuilder
import json


def test_context_template_builder_examples():
    builder = ContextTemplateBuilder()
    builder.add_question("What is the scientific name of this animal?")
    examples = [
        {"input": "Cheetah", "output": "Acinonyx Jubatus"},
        {"input": "Ray-finned fishes", "output": "Actinopterygii"},
        {"input": "Vulture", "output": "Aegypius Monachus"},
        {"input": "Impala", "output": "Aepyceros Melampus"},
        {"input": "Red-eyed tree frog", "output": "Agalychnis callidryas"},
        {"input": "Giant panda", "output": "Ailuropoda melanoleuca"},
        {"input": "American moose", "output": "Alces americanus"},
        {"input": "Marine iguana", "output": "Amblyrhynchus cristatus"},
    ]
    builder.add_input_output_examples(examples)
    context = builder.generate_context_template()
    assert context.template == '''What is the scientific name of this animal? Cheetah
Acinonyx Jubatus

What is the scientific name of this animal? Ray-finned fishes
Actinopterygii

What is the scientific name of this animal? Vulture
Aegypius Monachus

What is the scientific name of this animal? Impala
Aepyceros Melampus

What is the scientific name of this animal? Red-eyed tree frog
Agalychnis callidryas

What is the scientific name of this animal? Giant panda
Ailuropoda melanoleuca

What is the scientific name of this animal? American moose
Alces americanus

What is the scientific name of this animal? Marine iguana
Amblyrhynchus cristatus

What is the scientific name of this animal? {{input}}'''


def run_context_template_builder_examples():
    builder = ContextTemplateBuilder()
    builder.add_question("What is the scientific name of this animal?")
    examples = [
        {"input": "Cheetah", "output": "Acinonyx Jubatus"},
        {"input": "Ray-finned fishes", "output": "Actinopterygii"},
        {"input": "Vulture", "output": "Aegypius Monachus"},
        {"input": "Impala", "output": "Aepyceros Melampus"},
        {"input": "Red-eyed tree frog", "output": "Agalychnis callidryas"},
        {"input": "Giant panda", "output": "Ailuropoda melanoleuca"},
        {"input": "American moose", "output": "Alces americanus"},
        {"input": "Marine iguana", "output": "Amblyrhynchus cristatus"},
    ]
    builder.add_input_output_examples(examples)
    context = builder.generate_context_template()
    print(context.template)
    '''
    What is the scientific name of this animal? Cheetah:
    Acinonyx Jubatus
    What is the scientific name of this animal? {{input}}:
    '''
    llm = LLM()
    details = llm.fit(context)
    print(details)
    output = llm.predict(input="Dog")
    print(output)
    '''
    Canis lupus familiaris
    '''
    assert output.strip() == "Canis lupus familiaris"


def test_context_template_builder_oneshot():
    builder = ContextTemplateBuilder()
    builder.add_question("What is the scientific name of this animal? ")
    builder.add_instruction("Respond only with the scientific name.")
    context = builder.generate_context_template()
    assert context.template == 'What is the scientific name of this animal?  Respond only with the scientific name. {{input}}'


def test_context_template_builder_base():
    builder = ContextTemplateBuilder()
    context = builder.generate_context_template()
    assert (context.template) == '{{input}}'

# def test_context_template_builder_sql():
#     data_filename = 'data_for_quizlet'
#     data = read_data(data_filename)
#     builder = ContextTemplateBuilder()
#     builder.add_question("What is the scientific name of this animal?")
#     builder.add_instruction("Respond only with the scientific name.")
#     context = builder.generate_context_template()
#     print(context.template)
#     '''
#     What is the scientific name of this animal? Respond only with the scientific name. {{input}}:
#     '''


def read_data(data_filename, suffix='jsonl'):
    data = []
    with open(f'{data_filename}.{suffix}') as data_file:
        for line in data_file:
            line = json.loads(line)
            data.append(line)
    return data


if __name__ == "__main__":
    test_context_template_builder_examples()
    test_context_template_builder_oneshot()
    test_context_template_builder_base()
