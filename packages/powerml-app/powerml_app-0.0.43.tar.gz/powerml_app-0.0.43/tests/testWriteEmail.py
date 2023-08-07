from powerml import WriteEmailModel


def testWriteEmailModel():
    model = WriteEmailModel()
    examples = [{"subject": "Xfinity", "email":
                 """Peace of mind.
Redefined.

Our xFi Complete gives you peace of mind to do everything you love online with Unlimited Data and helps keep your devices safe and secure from cyberthreats at home and on the go.

Switch to xFi Complete for $11 more a month and you can upgrade your modem after three years for a better, more reliable connection for your home.

Upgrade now

Unleash the full potential
of worry-free WiFi

Unlimited data | Everyone in your home can work, game, and stream 24/7.	 	Equipment upgrades | You can upgrade your gateway after three years at no extra cost for a better, more reliable connection for your home.
Advanced Security at home | Xfinity keeps your devices safe and secure from cyber threats at home.	 	Wall-to-wall coverage | Our network evaluation helps ensure the most coverage at home, with an xFi Pod included if recommended.

Learn more

You may be eligible
to save on your Xfinity Internet and mobile services

Apply now

Shop deals	Account	Xfinity Stores""",
                 }]
    details = model.fit(examples)
    print(details)
    email = model.predict("Toys'r'Us")
    print(email)


if __name__ == "__main__":
    testWriteEmailModel()
