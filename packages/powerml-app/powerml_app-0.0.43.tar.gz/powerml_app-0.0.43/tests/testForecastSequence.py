from powerml import ForecastSequenceModel


def testForecastSequence():
    powerml = ForecastSequenceModel()
    examples = [{
        "release_date": "2018-07-31",
        "title": "Asian Boss Girl",
        "revenue": [10, 24, 36, 47, 66, 47, 55, 60, 25, 64]}]
    powerml.fit(examples)
    autocompletion = powerml.predict("Freakonomics Radio")
    print(autocompletion)
    return autocompletion


if __name__ == "__main__":
    testForecastSequence()
