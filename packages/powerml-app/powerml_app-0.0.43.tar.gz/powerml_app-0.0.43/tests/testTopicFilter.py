from powerml import TopicFilter


def read_data(data_filename, suffix='txt'):
    with open(f'{data_filename}.{suffix}') as data_file:
        data = data_file.read()
    data = data.split('\n')
    return [datum for datum in data if datum]


def write_data(data, data_filename, suffix='txt'):
    with open(f'{data_filename}.{suffix}', 'w') as data_file:
        for line in data:
            data_file.write(f'{line}\n')


def testTopicFilter(data, data_filename):
    print(f'Unfiltered Data Length: {len(data)}')
    filter = TopicFilter()
    filtered_data, metrics = filter.get_passing(data)
    print(f'Filtered Data Length: {len(filtered_data)}')
    print(metrics)
    data_filename = f'{data_filename}_filtered'
    write_data(filtered_data, data_filename)


if __name__ == "__main__":
    data_filename = 'data_from_unblocked_s3'
    data = read_data(data_filename)

    num_test = len(data)
    testTopicFilter(data[:num_test], data_filename)
