import json
import time
from powerml import CreateTopicsModel
import os
from itertools import islice


def preprocess_data_into_messages(data):
    data = data.split('\n')
    return [d for d in data if d]


def testCreateTopicsModel():
    run_CreateTopicsModel(False, )


def fullCreateTopicsModel():
    run_CreateTopicsModel(True, )


def run_CreateTopicsModel(use_full_dataset):
    data_path = os.path.join(os.path.dirname(
        __file__), "data_from_unblocked_s3.txt")

    with open(data_path, 'r') as f:
        data = f.read()
    docs = preprocess_data_into_messages(data)
    print(len(docs))
    if not use_full_dataset:
        docs = docs[:20]

    id_to_doc = {}
    for i, doc in enumerate(docs):
        id_to_doc[i] = doc

    model = CreateTopicsModel(sample_size=1)

    # Main function
    model.fit(id_to_doc, topic_type='one-word system components')
    start = time.time()
    topics = model.predict()
    print("time elapsed: ", time.time() - start)
    assert len(topics) > 0
    return topics


def run_chunked_CreateTopicsModel():
    data_path = os.path.join(os.path.dirname(
        __file__), "data_from_unblocked_s3.txt")

    with open(data_path, 'r') as f:
        data = f.read()
    docs = preprocess_data_into_messages(data)

    topics_array = []

    id_to_doc = {}
    for i, doc in enumerate(docs):
        id_to_doc[i] = doc

    def chunks(data, SIZE=100):
        it = iter(data)
        for i in range(0, len(data), SIZE):
            yield {k: data[k] for k in islice(it, SIZE)}

    for chunk in chunks(id_to_doc):
        model = CreateTopicsModel()
        # Main function
        model.fit(chunk, topic_type='one-word system components')
        topics = model.predict()
        assert len(topics) > 0
        topics_array.append(topics)

    topics = [item for sub_list in topics_array for item in sub_list]
    deduped_topics = CreateTopicsModel.deduplicate_topics_with_keywords(topics)

    return deduped_topics


def measure_perf(topics_no_batch, topics_batch):
    print("total topics with batch: ", len(topics_no_batch))
    print("top 100: ", [topic['name'] for topic in topics_no_batch])
    print("cutoff: ", topics_no_batch[100]['score'])

    print("total topics with batch: ", len(topics_batch))
    print("top 100: ", [topic['name'] for topic in topics_batch])
    print("cutoff: ", topics_batch[100]['score'])

    print("topics in the no batch that are missing: ", set(
        [topic['name'] for topic in topics_no_batch]) - set([topic['name'] for topic in topics_batch]))
    print("topics in the batch that are missing: ", set(
        [topic['name'] for topic in topics_batch]) - set([topic['name'] for topic in topics_no_batch]))


if __name__ == "__main__":
    topics_no_batch = run_CreateTopicsModel(True)
    print(topics_no_batch)
    # Serializing json
    json_object = json.dumps(topics_no_batch, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
