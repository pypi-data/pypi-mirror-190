from powerml import AutocompleteSQLModel


def testAutocompleteSQLModel():
    powerml = AutocompleteSQLModel()

    powerml.fit(
        table_schemas=[
            "CREATE TABLE users ( id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT);"
        ],
        example_queries=[
            "SELECT * FROM users WHERE id=?;"
        ])

    autocompletion = powerml.predict("select * from ")
    assert autocompletion != ""


if __name__ == "__main__":
    testAutocompleteSQLModel()
