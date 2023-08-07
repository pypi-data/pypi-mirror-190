from powerml import LLM
from powerml import ContextTemplate


def test_LLM():
    args = ["arg1", "arg2"]
    template = "{{arg1}}\n{{arg2}}"
    context = ContextTemplate(template, args)

    llm = LLM()  # LLM({"powerml.url":"http://localhost:5001"})
    llm.fit(context)
    output = llm.predict(arg1="str111", arg2="str222")
    assert output != ""


def test_LLM_only_input():
    args = ["input"]
    template = "{{input}}"
    context = ContextTemplate(template, args)

    llm = LLM()
    details = llm.fit(context)
    print(details)
    output = llm.predict(input="str111",)
    print(output)
    assert output != ""


def test_LLM_only_input_throw_error():
    args = ["input"]
    template = "{{input}}"
    context = ContextTemplate(template, args)

    llm = LLM()
    llm.fit(context)
    try:
        llm.predict()
    except BaseException:
        assert True
        return
    assert False


def test_LLM_no_args():
    llm = LLM()
    template = "Help me recruit new students to my movie club. Write an ad for a movie club:\n"
    context = ContextTemplate(template, [])
    llm.fit(context)
    llm.predict()


def test_LLM_empty():
    args = ["arg1", "arg2"]
    template = "{{arg1}}\n{{arg2}}"
    context = ContextTemplate(template, args)

    llm = LLM()
    llm.fit(context)
    output = llm.predict(arg2="str222")
    print(output)
    assert output != ""


def test_LLM_Context_Error():
    args = ["arg1", "arg2"]
    template = "{{arg1}}\n{{arg2}}"
    context = ContextTemplate(template, args)

    llm = LLM()
    llm.fit(context)
    try:
        llm.predict(arg2="str222", arg3="hehe")
    except BaseException:
        assert True
        return
    assert False


def run_LLM_against_existing_template():
    llm = LLM(model="sql/v1")
    table_schemas = [
        "CREATE TABLE users ( id SERIAL PRIMARY KEY, first_name TEXT, last_name TEXT);"
    ]
    example_queries = [
        "SELECT * FROM users WHERE id=?;"
    ]
    table_schemas_string = "\n".join(table_schemas)
    example_queries_string = "\n".join(example_queries)
    sql_prompt = "select"
    output = llm.predict(table_schemas=table_schemas_string, examples=example_queries_string, input=sql_prompt)
    assert output != ""


def test_multiple_fit_and_predict_in_series():
    args = ["arg1", "arg2"]
    template = "{{arg1}}\n{{arg2}}"
    context = ContextTemplate(template, args)
    llm = LLM()

    print(context.get_prompt_template())
    llm.fit(context)
    output = llm.predict(arg1="str111", arg2="str222")
    print(output)

    examples = ["example1"]
    context.set_examples(examples)  # we handle how to add examples to fit the prompt (?) # context.extend(examples)
    print(context.get_prompt_template())
    llm.fit(context)
    output = llm.predict(arg1="str111", arg2="str222")
    print(output)


def run_notebook_tasks():
    llm = LLM()
    '''
    Write a prompt to recruit new students to your movie club
    '''
    template = "Help me recruit new students to my movie club. Write an ad for a movie club:\n"
    context = ContextTemplate(template, [])
    llm.fit(context)
    output = llm.predict()
    print("--------------")
    print(output)
    '''
    Adjust the prompt to make the tone of it funny
    '''
    template = "Think of some jokes about movie club, and write an ad for movie club with these puns embedded in the ad:\n"
    context = ContextTemplate(template, [])
    llm.fit(context)
    output = llm.predict()
    print("--------------")
    print(output)
    '''
    Add an example of a funny email
    '''
    funny_email = '''Subject: Join the Movie Club!

Hello everyone!

Are you a buff movie buff? Do you love watching the latest blockbusters and classics? Then join the Movie Club! Every month we get together to watch a movie and discuss it afterwards. We’ve had lively debates about the plot, the characters, and the cinematography. It’s a reel-y great way to make new friends and have a good time.

The Movie Club meets on the first Saturday of every month at 8 PM. We usually meet at the local theater, but sometimes we also rent out a private screening room. Admission is free, but please bring your own snacks and drinks.

If you’re interested in joining us, please reply to this email and we’ll add you to our list.

Looking forward to meeting you!

Sincerely,

[Your Name]'''
    context.set_examples([funny_email])
    llm.fit(context)
    output = llm.predict()
    print("--------------")
    print(output)
    '''
    Add multiple examples
    '''
    emails = [funny_email,
              '''Subject: Request for Additional Resources

Dear [Name],

I hope you are doing well. I am writing to request additional resources to help our team complete our project on time.

We have been working hard on this project and have made considerable progress despite the current resource constraints. However, I believe we could do better with additional resources, such as additional personnel, equipment, or budget.

I would like to discuss this further with you and come up with a plan to ensure the success of this project. Please let me know when a good time would be for us to meet.

I look forward to hearing from you.

Sincerely,
[Your Name]''', '''Subject: Questions about Assignment

Dear Professor [Name],

I am writing to ask a few questions about the assignment you gave us last week. Specifically, I am unsure about the following items:

- What is the page limit for the project?
- What type of citation format should we use?
- Are there any specific sources that you would like us to use?

I would really appreciate if you could clarify these points for me. Thank you for your help.

Sincerely,
[Your Name]''', '''Subject: Meeting Request

Dear [Name],

I hope this email finds you well. I am writing to request a meeting with you to discuss an opportunity that I think would be beneficial to us both.

I recently learned about a new program that I believe could benefit our company. I believe that with the right implementation, this program could increase our productivity and help us reach our goals. I would like to discuss this opportunity with you in more detail.

Would you be available for a meeting next week to discuss this further? I am available any day and can come to your office or arrange a call.

I look forward to your response.

Best,
[Your Name]''']
    context.set_examples(emails)
    llm.fit(context)
    output = llm.predict()
    print("--------------")
    print(output)
    '''
    Write a template for the prompt so you can use it for different tones and for all your extracurriculars
    '''
    template = "Help me recruit new students to {{extracurricular}} by writing a very {{tone}} email:\n"
    context = ContextTemplate(template, ["extracurricular", "tone"])
    context.set_examples(emails)
    llm.fit(context)
    output = llm.predict(extracurricular="my business fraternity", tone="sad")
    print("--------------")
    print(output)
    output = llm.predict(extracurricular="my business fraternity", tone="extremely sad")
    print("--------------")
    print(output)


if __name__ == "__main__":
    test_LLM()
