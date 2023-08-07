from powerml import TopicGenerator, SQLGenerator, MenuGenerator, PrestoGenerator, EmailGenerator, QuestionGenerator, ForecastGenerator
from powerml.utils.generator import create_schema
import json


def read_data_txt(data_filename, suffix='txt'):
    with open(f'{data_filename}.{suffix}') as data_file:
        data = data_file.read()
    data = data.split('\n')
    return [datum for datum in data if datum]


def read_data_jsonl(data_filename, suffix='jsonl'):
    data = []
    with open(f'{data_filename}.{suffix}') as data_file:
        for line in data_file:
            line = json.loads(line)
            data.append(line)
    return data


def write_data_txt(data, data_filename, suffix='txt'):
    with open(f'{data_filename}.{suffix}', 'w') as data_file:
        for line in data:
            data_file.write(f'{line}\n')


def write_data_jsonl(data, data_filename, suffix='jsonl'):
    with open(f'{data_filename}.{suffix}', 'w') as data_file:
        for line in data:
            json.dump(line, data_file)
            data_file.write(f'\n')


def get_data_length(data):
    return sum([len(datum['questions']) for datum in data])


def run_generators(generators):
    for generator_type in generators:
        print(f'{generator_type}Generator:')
        generator, data = generators[generator_type]
        generated_data, metrics = generator.get_rare(data)
        if generator_type == 'Question':
            print(f'Generated Data Length: {get_data_length(generated_data)}')
        else:
            print(f'Generated Data Length: {len(generated_data)}')
        print(metrics)
        data_filename = f'{generator_type.lower()}_generated'
        if generator_type in ['Topic', 'SQL']:
            write_data_txt(generated_data, data_filename)
        else:  # generator_type in ['Menu', 'Presto', 'Email', 'Question', 'Forecast']
            write_data_jsonl(generated_data, data_filename)


def testGenerators():
    num_test = 1
    topic_data_filename = 'data_from_unblocked_s3'
    topic_data = read_data_txt(topic_data_filename)
    sql_data_filename = 'data_from_hex'
    sql_data = read_data_txt(sql_data_filename)
    sql_schema = create_schema(sql_data)
    menu_data_filename = 'data_from_presto'
    menu_data = read_data_jsonl(menu_data_filename)
    email_data_filename = 'data_for_stensul'
    email_data = read_data_jsonl(email_data_filename)
    question_data_filename = 'data_for_quizlet'
    question_data = read_data_jsonl(question_data_filename)
    forecast_data_filename = 'data_from_inferencio'
    forecast_data = read_data_jsonl(forecast_data_filename)
    generators = {
        'Topic': (TopicGenerator(), topic_data[:num_test]),
        'SQL': (SQLGenerator(sql_schema), sql_data[:num_test]),
        'Menu': (MenuGenerator(), menu_data[:num_test]),
        'Presto': (PrestoGenerator(), menu_data[:num_test]),
        'Email': (EmailGenerator(), email_data[:num_test]),
        'Question': (QuestionGenerator(), question_data[:num_test]),
        'Forecast': (ForecastGenerator(), forecast_data[:num_test]),
    }
    run_generators(generators)


if __name__ == "__main__":
    testGenerators()
