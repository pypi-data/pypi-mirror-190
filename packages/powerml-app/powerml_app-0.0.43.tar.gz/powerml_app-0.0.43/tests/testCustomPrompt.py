from powerml import PowerML
from powerml.utils.config import get_config


def testCustomModel(model: PowerML,):
    # Call the model in staging
    table_schemas = [
        "CREATE TABLE users ( id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT);"
    ]
    example_queries = [
        "SELECT * FROM users WHERE id=?"
    ]
    prompt = {
        "{{input}}": "select * from ",
        "{{examples}}": "\nEND".join(example_queries),
        "{{table_schemas}}": "\n".join(table_schemas)
    }
    output = model.predict(
        prompt,
        max_tokens=256,
        stop=['\\\\nEND', '\\nEND', '\nEND', ';'],
        temperature=0.7,)
    print(output)


def getStagingModel(model_name):
    # config hack, make sure your config file is configured properly to run this script
    cfg = get_config()
    key = cfg['powerml_staging.key']
    url = cfg['powerml_staging.url']
    config = {"powerml":
              {"key": key,
               "url": url
               }}
    model = PowerML(config, model=model_name)
    return model


def getProductionModel(model_name):
    # config = {"powerml": {"url":"https://api.powerml.co"}}
    model = PowerML(model=model_name)
    return model


if __name__ == "__main__":
    # model = getStagingModel()
    model = getProductionModel("a59a0400f4349c4191e1ee87691a73731fc8b0d4af2ef43c70a08d85853be396")
    testCustomModel(model)
