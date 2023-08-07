
from powerml import ExtractTopicsModel
import json
import os

topic_string = """sourcemarks
vscode
web
dashboard
kotlin
styles
services
video
messages
threads
mentions
git
github
auth
hub
slack
webhooks
gradle
intercom
adminconsole
ingestion
api
onboarding
discussions
insights
email
teams
notifications
pusher
logging
security
commands
controllers
stores
datastores
test
typescript
react
recommendations
logs
compression
compute
webpack
webextension"""


def testExtractTopicsModel():
    model = ExtractTopicsModel()
    examples = get_examples()
    topics = get_unblocked_topics()
    model.fit(examples, topics)
    topics = model.predict(
        "Move invite teammates page to its own base route . per designs:   This PR just moves existing views around and adds a new base route (i.e. no new functionality)")
    print("topics:", topics)
    assert 'web' in topics

def testBatchExtractTopicsModel():
    model = ExtractTopicsModel()
    examples = get_examples()
    topics = get_unblocked_topics()
    model.fit(examples, topics)
    topics = model.batch_predict([ 
        "Move invite teammates page to its own base route . per designs:   This PR just moves existing views around and adds a new base route (i.e. no new functionality)", 
        "Move invite teammates page to its own base route . per designs:   This PR just moves existing views around and adds a new base route (i.e. no new functionality)"
        ])
    print("topics:", topics)

def get_examples():
    examples_path = os.path.join(os.path.dirname(
        __file__), "unblocked_examples_labels.json")

    with open(examples_path) as examples_file:
        examples = json.load(examples_file)

    return examples


def get_unblocked_topics():
    return topic_string.split("\n")


if __name__ == "__main__":
    testBatchExtractTopicsModel()
