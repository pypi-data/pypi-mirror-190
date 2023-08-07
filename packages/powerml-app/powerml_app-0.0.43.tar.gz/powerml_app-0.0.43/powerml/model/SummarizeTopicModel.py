from typing import List
from powerml import PowerML
from powerml.utils.constants import MAX_TEMPLATE_TOKENS


class SummarizeTopicModel:
    '''
    This model removes summarizes topics given context with relevant documents.
    '''

    def __init__(
            self,
            config={},):
        self.model = PowerML(config, "unblocked/summarize-topics")

    def predict(self, topic: str, documents: List[str],) -> str:
        prompt = self.__get_prompt(topic, documents)
        completion = self.model.predict(prompt)
        return self.__post_process(completion)

    def batch_predict(self, topics_to_docs: List):
        prompts = [self.__get_prompt(topic['name'], topic['documents']) for topic in topics_to_docs]
        completions = []
        while prompts:
            batch = prompts[:self.model.BATCH_MAX]
            completions.extend(self.model.batch_predict(batch))
            prompts = prompts[self.model.BATCH_MAX:]
        return [self.__post_process(completion) for completion in completions]

    def __get_prompt(self, topic: str, documents: List[str],):
        document_string = ""
        for document in documents:
            if len(document_string) + len(document) > MAX_TEMPLATE_TOKENS:
                break
            document_string += document + "\n"
        prompt = {
            "{{documents}}": document_string,
            "{{topic}}": topic,
        }
        return prompt

    def __post_process(self, completion: str):
        return completion.strip()
