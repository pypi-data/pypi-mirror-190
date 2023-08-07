from powerml import ExtractTopicsModel
import os
import json


def testPowerMLTopicModelTutorial():
    # Use the topic model that is tuned for unblocked
    model = ExtractTopicsModel(model_name="unblocked/extract-topics")
    topics = model.predict(
        "Move invite teammates page to its own base route . per designs: This PR just moves existing views around and adds a new base route (i.e. no new functionality)")
    print(topics)
    assert "onboarding" in topics
    # assert "routes" in topics


def testTrainANewModel():
    def get_examples():
        examples_path = os.path.join(os.path.dirname(__file__),
                                     "examples.json")
        with open(examples_path) as examples_file:
            examples = json.load(examples_file)
        return examples

    def get_topics():
        return ["vscode", "web", "dashboard"]

    # Create a new model to identify a list of desired topics
    model = ExtractTopicsModel(get_topics())
    examples = get_examples()
    model.fit(examples)
    topics = model.predict(
        "Move invite teammates page to its own base route . per designs: This PR just moves existing views around and adds a new base route (i.e. no new functionality)")
    print("topics:", topics)


if __name__ == "__main__":
    # testPowerMLTopicModelTutorial()
    testTrainANewModel()
