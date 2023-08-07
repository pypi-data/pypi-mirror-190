from powerml import MenuFilter
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


def testMenuFilter(data, data_filename):
    print(f'Unfiltered Data Length: {len(data)}')
    filter = MenuFilter()
    filtered_data, metrics = filter.get_passing(data)
    print(f'Filtered Data Length: {len(filtered_data)}')
    print(metrics)
    data_filename = f'{data_filename}_menu_filtered'
    write_data(filtered_data, data_filename)


if __name__ == "__main__":
    data_filename = 'data_from_presto'
    data = read_data(data_filename)

    num_test = len(data)
    testMenuFilter(data[:num_test], data_filename)
