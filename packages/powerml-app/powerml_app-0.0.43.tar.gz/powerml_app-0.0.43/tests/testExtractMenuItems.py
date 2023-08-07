from powerml import ExtractMenuItemsModel


def testExtractMenuItems():
    model = ExtractMenuItemsModel()
    examples = [{
        "conversation": """CX: Can I get a #11 combo? Medium.
AI: What drink would you like? Sure Would you like to add an order of cinnamon churros?
CX: Coke.
AI: What else?
CX: Would you like to add an order of Cinnamon Churros? No, thank you. Ohh, I'll take a number. 12.
AI: Would you like medium or macho? What drink would you like?
CX: Medium. I see.
AI: Anything else?
CX: No.
AI: I have 1 #11 meal with del combo burrito, medium crinkle cut fries and medium coke. and 1 #12 meal with classic grilled chicken burrito, medium crinkle cut fries and medium hi c fruit punch. .. correct?
CX: Yes.""",
        "order": """
    1x #11 Del Combo Burrito Meal
       Del Combo Burrito
       Medium Crinkle Cut Fries
       Medium Drink
          Coke
    1x #12 Classic Grilled Chicken Burrito Meal
       Classic Grilled Chicken Burrito
       Medium Crinkle Cut Fries
       Medium Drink
          HI C Fruit Punch""", }]
    model.fit(examples)
    items = model.predict("1 Chicken Burrito")
    print(items)


if __name__ == "__main__":
    testExtractMenuItems()
