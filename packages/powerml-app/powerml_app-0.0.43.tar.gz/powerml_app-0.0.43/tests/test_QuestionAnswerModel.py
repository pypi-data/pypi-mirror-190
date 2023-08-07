from powerml import QuestionAnswerModel


def testQuestionAnswerModel():
    model = QuestionAnswerModel()

    note = "Greek Philosophy"
    examples = [{'note': note, 'questions': [{'Q': "Who said 'The only true wisdom is in knowing you know nothing.'", 'A': 'Socrates'}, {
        'Q': "Who said 'I am the wisest man alive, for I know one thing, and that is that I know nothing.'", 'A': 'Socrates'}]}]
    model.fit(examples)
    num_questions = 1
    result = model.predict(note, num_questions)
    print()
    print(result)
    assert result is not None


if __name__ == "__main__":
    testQuestionAnswerModel()
