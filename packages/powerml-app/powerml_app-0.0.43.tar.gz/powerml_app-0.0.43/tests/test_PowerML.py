from powerml import PowerML


def testPowerMLFitAndPredict():
    powerml = PowerML()

    data = ["item2", "item3"]
    model_details = powerml.fit(data)
    assert model_details is not None

    response = powerml.predict("test")
    assert response != ""


def testPowerMLPredictNoConfig():
    powerml = PowerML()
    testPrompt = "hello there"
    response = powerml.predict(prompt=testPrompt)
    assert response != ""


if __name__ == "__main__":
    testPowerMLFitAndPredict()
