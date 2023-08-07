from powerml import SummarizeTopicModel, CreateTopicsModel
import os
import json


def get_examples():
    examples_path = os.path.join(os.path.dirname(
        __file__), "unblocked_examples_labels.json")

    with open(examples_path) as examples_file:
        examples = json.load(examples_file)

    return examples


def testSummarizeTopicModel():
    model = SummarizeTopicModel()
    labeled_data = get_examples()
    documents = []
    for data in labeled_data:
        if "sourcemarks" in data["labels"]:
            documents.append(data["example"])
    summary = model.predict("sourcemarks", documents=documents)
    assert summary != ""

def preprocess_data_into_messages(data):
    data = data.split('\n')
    return [d for d in data if d]


def topicPipeline(use_full_dataset):
    data_path = os.path.join(os.path.dirname(
        __file__), "data_from_unblocked_s3.txt")

    with open(data_path, 'r') as f:
        data = f.read()
    docs = preprocess_data_into_messages(data)
    if not use_full_dataset:
        docs = docs[:20]

    id_to_doc = {}
    for i, doc in enumerate(docs):
        id_to_doc[i] = doc

    model = CreateTopicsModel()
    model.fit(id_to_doc, topic_type='one-word system components')
    topics = model.predict()
    topics = topics[:100]
    model = SummarizeTopicModel()
    new_topics = topics
    args = []
    # Summarize topics
    for index, topic in enumerate(topics):
        name = topic["name"]
        documents = [docs[i] for i in topic["documents"]]
        args.append({'name':name,'documents':documents})
    summary_list = model.batch_predict(args)
    for index,_ in enumerate(new_topics):
        new_topics[index]["summary"] = summary_list[index]
    return new_topics


if __name__ == "__main__":
    testSummarizeTopicModel()
    # topics = topicPipeline(True)

    # def set_default(obj):
    #     if isinstance(obj, set):
    #         return list(obj)
    #     raise TypeError
    # with open('topics_out.json', 'w') as f:
    #     json.dump(topics, f, default=set_default)
    # print(testSummarizeTopicModel())
