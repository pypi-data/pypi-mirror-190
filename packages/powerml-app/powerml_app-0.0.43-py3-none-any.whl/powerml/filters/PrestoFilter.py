from powerml import MenuFilter
from powerml.utils.run_ai import query_powerml
from powerml.utils.constants import FILTER_MODEL, SHORT_CONVO_TURNS, MAX_STRING_LENGTH
import re
import logging

logger = logging.getLogger(__name__)


class PrestoFilter(MenuFilter):
    '''
    This is a class that can be used to filter noise from Presto data for ExtractMenuItemsModels.
    '''

    def __init__(self):
        super().__init__('order for the conversation')
        self.filters = {**self.general_filters,
                        'No Item': self.__does_customer_order_any_item,
                        'Multiple Item': self.__does_customer_order_this_item,
                        'Short Convo': self.__remove_short_conversations,
                        'Monologue': lambda conversations: self.__filter_regex(r"(CX|AI)", conversations),
                        }

    def __make_conversation_prompt(self, conversation):
        prompt = "This is a conversation where a customer orders the following items:\n"

        prompt += conversation["completion"]

        prompt += "\n\nConversation:\n"
        prompt += conversation["prompt"] + "\n"

        return prompt

    def __make_yes_no_question_prompt(self, example, question):
        prompt = self.__make_conversation_prompt(example)

        prompt += question + " Answer Yes or No. Answer:"

        if "is_yes" in example:
            if example["is_yes"]:
                prompt += " Yes\n\n"
            else:
                prompt += " No\n\n"

        return prompt

    def __trim_end(self, string):
        if len(string) > MAX_STRING_LENGTH:
            return string[-MAX_STRING_LENGTH:]

        return string

    def __answer_yes_no_question(self, prompt, allowed_tokens):
        logger.debug("Question: " + self.__trim_end(prompt))

        if allowed_tokens is None:
            result = query_powerml(prompt, model=FILTER_MODEL, max_tokens=1)
        else:
            result = query_powerml(prompt, model=FILTER_MODEL, max_tokens=1, allowed_tokens=[" No", " Yes"] + allowed_tokens)

        logger.debug("Answer: " + result)

        if result.lower().strip().find("yes") == 0:
            return True

        return False

    def __filter_question(self, question, conversations, examples, allowed_tokens=[]):
        filtered_conversations = []

        for conversation in conversations:
            prompt = ""

            for example in examples:
                prompt += self.__make_yes_no_question_prompt(example, question)

            prompt += self.__make_yes_no_question_prompt(
                conversation, question)

            answer = self.__answer_yes_no_question(prompt, allowed_tokens)

            if answer:
                filtered_conversations.append(conversation)

        logger.debug("Passing filter " + str(len(filtered_conversations)) + " / " +
                     str(len(conversations)) + " - " + question)

        return filtered_conversations

    def __does_customer_order_any_item(self, conversations):
        examples = [{"prompt": "AI1: <welcome>\nAI2: Can I get you an iced drink today?\nCX: Yeah.\nAI2: Got it.\nAI1: What can we make fresh for your today?\nCX: I want a Bean & Cheese Burrito with Green sauce.\nAI1: Got it.\nAI2: Can I get a Bean & Cheese Burrito with green sauce?\nAI1: Sure.\nAI2: Got it..",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": True},
                    {"prompt": "AI1: <welcome>\nCX1: I'm sorry, I'm not sure what you're saying.\nAI1: Can I get you an icked cold drink today?\nCX1: I'm sorry. I'm not sure what you're asking.\nAI1: Can I order you an icked cold drink today.\nCX1: I'm sorry I'm not sure what you're talking about.\nAI1: Can I please get you an icked cold drink.\nCX1: I'm not sure what you're trying to say.\nAI1: Can I have an icked cold drink.",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": False},
                    {"prompt": "\nCX: Hello.\nAI (reading back): <welcome>\nCX: I'm sorry.\nAI: Order when ready.\nCX: I'm sorry. I'm sorry.\nAI: Okay.\nCX: I'm sorry, I'm sorry.\nAI: I'm sorry.\nCX: I'm sorry I'm sorry.\nAI: You're sorry?\nCX: I'm sorry. You're sorry?\nAI: I'm sorry. I'm so sorry.\nCX: I'm so sorry.\nAI: I'm so sorry.\nCX (reading back): I'm sorry",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": False}]

        return self.__filter_question("Does the customer order any item?", conversations, examples, None)

    def __does_customer_order_this_item(self, conversations):
        examples = [{"prompt": "\nCX: <welcome>\nAI: Ohh.. Like it?.\nCX: Yeah.\nAI: Okay, I'll have a large French fry.\nCX: Okay, I'll have a medium French fry.\nAI: Okay, I have it.\nCX: Can I get a large French fry?\nAI: Okay, I have that.\nCX: Can I get an iced cold drink?\nAI: Okay, I'll get you a large Sprite.\nCX: Okay, I have it. What else?\nAI: What else?\nCX: What's that?\n",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": False},
                    {"prompt": "\nCX: I'm sorry, I don't understand.\nAI: What would you like?\nCX: The Del Taco.\nAI: What would you prefer?\nCX: The Del Tako.\nAI: What would you rather have?\nCX: The Del Tato.\nAI: What would you have?\nCX: The Del Tac.\nAI: What would you order?\nCX: The Del Tacoo.\nAI: What would you want?\nCX: The Del Tacu.\nAI: What would you choose?\nCX: The Del Tacuu.\nAI: What",
                     "completion": "1x The Del Taco",
                     "is_yes": True},
                    {"prompt": "CX: Can I get you a Sprite?\nAI: Sure, I'll have a Sprite.\nCX: Can I get you Sprite?\nAI: Sure.\nCX: Can I get Sprite?\nAI: Sure..\nCX: Can I get Spray?\nAI: Sure..",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": False},
                    {"prompt": "AI1: <welcome>\nAI2: Can I get you an iced drink today?\nCX: Yeah.\nAI2: Got it.\nAI1: What can we make fresh for your today?\nCX: I want a Bean & Cheese Burrito with Green sauce.\nAI1: Got it.\nAI2: Can I get a Bean & Cheese Burrito with green sauce?\nAI1: Sure.\nAI2: Got it..",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": True},
                    {"prompt": "CX: <welcome>\nAI: Hi, can I help you?\nCX: Yes, I'd like to talk to a live person.\nAI: Okay, I'll be right back.",
                     "completion": "1x Bean & Cheese Burrito with Green Sauce",
                     "is_yes": False}]

        return self.__filter_question("Does the customer order only the one item?", conversations, examples, None)

    def __remove_short_conversations(self, conversations):

        filtered_conversations = []

        for conversation in conversations:
            turns = conversation["prompt"].count(":")

            if turns > SHORT_CONVO_TURNS:
                filtered_conversations.append(conversation)

        logger.debug("Passing filter " + str(len(filtered_conversations)) + " / " +
                     str(len(conversations)) + " - too short")

        return filtered_conversations

    def __filter_regex(self, regex, conversations):
        filtered_conversations = []

        for conversation in conversations:
            match = re.search(regex, conversation["prompt"])

            if match:
                filtered_conversations.append(conversation)

        logger.debug("Passing regex filter " + str(len(filtered_conversations)) + " / " +
                     str(len(conversations)) + " - " + regex)

        return filtered_conversations
