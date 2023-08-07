from powerml.utils.config import get_config


def testConfigure():
    config = get_config()
    assert config is not None
    config = get_config({"powerml": {"key": "test"}})
    assert config['powerml.key'] == "test"


if __name__ == "__main__":
    testConfigure()
