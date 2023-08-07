import requests


def testStagingOpenai():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer cb01626747049cb05e1132c4f88b412c5ee8d169',
    }
    json_data = {
        'prompt': {
            '{{topics_in_list}}': '[llama, alpaca, cheeseburger]',
            '{{topic_type}}': 'burgers',
        },
        'model': 'unblocked/filter-topics',
        "stop": "",
        "temperature": 0.7,
    }
    response = requests.post(
        url="https://api.staging.powerml.co/v1/completions",
        headers=headers,
        json=json_data)
    print(response.text)
    assert response.status_code == 200


def testStagingLlama():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer cb01626747049cb05e1132c4f88b412c5ee8d169',
    }
    json_data = {
        'prompt': 'hello world',
        'model': 'llama',
    }
    response = requests.post(
        url="https://api.staging.powerml.co/v1/completions",
        headers=headers,
        json=json_data)
    assert response.status_code == 200


if __name__ == "__main__":
    testStagingLlama()
    testStagingOpenai()
