from powerml import QuestionFilter
import json


def read_data(data_filename, suffix='jsonl'):
    data = []
    with open(f'{data_filename}.{suffix}') as data_file:
        for line in data_file:
            line = json.loads(line)
            data.append(line)
    return data


def write_data(data, data_filename, suffix='jsonl'):
    with open(f'{data_filename}.{suffix}', 'w') as data_file:
        for line in data:
            json.dump(line, data_file)
            data_file.write(f'\n')


def get_data_length(data):
    return sum([len(datum['questions']) for datum in data])


def testQuestionFilter(data, data_filename):
    print(f'Unfiltered Data Length: {get_data_length(data)}')
    filter = QuestionFilter()
    filtered_data, metrics = filter.get_passing(data)
    print(f'Filtered Data Length: {get_data_length(filtered_data)}')
    print(metrics)
    data_filename = f'{data_filename}_filtered'
    write_data(filtered_data, data_filename)


if __name__ == "__main__":
    data_filename = 'data_for_quizlet'
    data = read_data(data_filename)

    num_test = len(data)
    testQuestionFilter(data[:num_test], data_filename)
