from powerml import CreateTopicsModel, ExtractTopicsModel, FilterTopicsModel
import random


def preprocess_data_into_messages(data):
    data = data.split('\n')
    return [d for d in data if d]


def get_formatted_examples():
    examples = [
        {
            "example": "Move invite teammates page to its own base route . per designs: This PR just moves existing views around and adds a new base route (i.e. no new functionality)", "labels": ["web"]}, {
            "example": "parse authorization query string. Adding support for authorization query string. Positive cases for local test are broken so I couldn't validate this 100% but it has limited impact and no one is using assets so we won't need to disable prod deploys", "labels": [
                "auth", "test"]}, {
                    "example": "Add slack channel selection on load. A few problems needed to be solved: State changes are not causing re-renders on dropdown. Need to make loading text sticky on bottom of list.", "labels": [
                        "slack", "dashboard"]}, {
                            "example": "Update relative DateTime helper. per feedback from Ben, make relative time ago helper show X <time> ago up to a year, then show MM YYYY show full date in title:", "labels": ["none"]}, {
                                "example": "Admin web changes New Config page for global config. The Team and Person pages are also updated.", "labels": [
                                    "adminconsole", "web"]}]
    return examples


if __name__ == "__main__":
    # Can be found at
    # https://s3.console.aws.amazon.com/s3/object/power-unblocks?region=us-west-2&prefix=scm-slack-notion/score/unblocked_unlabeled_examples.txt
    with open('data_from_unblocked_s3.txt', 'r') as f:
        data = f.read()
    data = preprocess_data_into_messages(data)

    # Get topics from data
    model = CreateTopicsModel()
    model.fit(data, topic_type='one-word system components')
    topics_with_scores = model.predict()
    print(topics_with_scores)
    topics = [topic["name"] for topic in topics_with_scores]

    # Filter Topics
    model = FilterTopicsModel()
    model.fit(topics=topics, topic_type="technical system-level topics")
    filtered_topics = model.predict()
    print(filtered_topics)

    # Extract Topics
    topic_model = ExtractTopicsModel()
    topic_model.fit(get_formatted_examples(), filtered_topics)

    new_example = "Move invite teammates page to its own base route . per designs:   This PR just moves existing views around and adds a new base route (i.e. no new functionality)"
    new_example_topics = topic_model.predict(new_example)
    print(new_example_topics)
