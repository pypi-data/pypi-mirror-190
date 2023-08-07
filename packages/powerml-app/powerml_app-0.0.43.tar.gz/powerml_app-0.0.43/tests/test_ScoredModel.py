from powerml import ScoredModel


def testScoredModel():
    model = ScoredModel()
    examples = [
        {
            'title': 'HAUGESUND Spring mattress, medium firm/dark beige, Queen',
            'customer': 'IKEA',
            'product_type': 'mattress',
            'product_name': 'haugesund',
            'product_info_from_db': 'spring; medium firm; colors: dark beige, light beige; sizes: twin, queen',
            'seo_score': 93,
        },
        {
            'title': 'MORGEDAL Foam mattress, firm/dark gray, Twin - IKEA',
            'customer': 'IKEA',
            'product_type': 'mattress',
            'product_name': 'morgedal',
            'product_info_from_db': 'foam firm; colors: light gray, dark gray; sizes: twin, full',
            'seo_score': 99,
        },
    ]

    model.fit(
        examples,
        generate_key='title',
        score_key='seo_score',
        metadata_keys=['customer', 'product_type', 'product_name', 'product_info_from_db'],
        higher_is_better=True,
    )
    output = model.predict({
        'customer': 'IKEA',
        'product_type': 'mattress',
        'product_name': 'hesstun',
        'product_info_from_db': 'eurotop; firm; colors: gray, white; sizes: full, queen',
    }
    )
    print(output)


if __name__ == "__main__":
    testScoredModel()
