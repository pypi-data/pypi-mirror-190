from powerml.utils.run_ai import batch_query_openai, batch_query_powerml
import time


def testBatch():
    for i in range(20):
        print("iteration: ", i)
        start = time.time()
        prompts = ["hi", "dog", "cat"]
        results = batch_query_openai(prompts,
                                     model="text-davinci-003",
                                     max_tokens=128,
                                     temperature=0.7,
                                     )
        print(results)
        print("seconds elapsed: ", time.time() - start)


def testPowerMLBatch():
    prompts = ["hi", "dog", "cat"]
    result = batch_query_powerml(
        prompt=prompts,
        stop="",
        model="text-davinci-003",
        max_tokens=128,
        temperature=0,
    )
    print(result)


def testPowerMLBatchComplexPrompt():
    prompts = [
        {
            "{{examples}}": "hi",
            "{{topics}}": "ho",
            "{{input}}": "hee",
        },
        {
            "{{examples}}": "hello",
            "{{topics}}": "how",
            "{{input}}": "are",
        },]
    result = batch_query_powerml(
        prompt=prompts,
        stop="",
        model="unblocked/extract-topics/v2",
        max_tokens=128,
        temperature=0,
    )
    print(result)


def testPowerMLBatchComplexPrompt2():
    prompts = [
        {
            "{{examples}}": "hi",
            "{{topic_type}}": "r",
            # "c":"x",
        },
    ]
    result = batch_query_powerml(
        prompt=prompts,
        stop="",
        model="unblocked/create-topics/v3",
        max_tokens=128,
        temperature=0,
    )
    print(result)


if __name__ == "__main__":
    testPowerMLBatchComplexPrompt2()
