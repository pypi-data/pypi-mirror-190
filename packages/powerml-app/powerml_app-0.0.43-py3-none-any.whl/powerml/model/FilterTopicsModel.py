from powerml import PowerML
from powerml.utils.constants import MAX_TEMPLATE_TOKENS
import re
from tqdm import tqdm
import sys
import os


class FilterTopicsModel:
    '''
    This model removes topics that are not in the
    topic_type category.
    '''

    def __init__(
            self,
            config={},):
        self.model = PowerML(config, "unblocked/filter-topics")
        self.memo_filtered_topics = {}
        self.topics = []
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def fit(self, topics, topic_type):
        """
        Parameters
        ----------
        topics : list[str]
            A list of potential topics to be filtered
        topic_type : str
            A broad categorization of the context that should be used to get the topics (e.g. "tech", "finance")
        """
        self.topic_type = topic_type
        self.topics = topics
        # Subdivide topics array
        # Iterate over each string in topics, appending to a working array
        # until there are too many characters, then add to the topics_array
        self.topics_array_split = []
        curr = []
        for topic in self.topics:
            if self.__count_tokens(f"{curr}") > MAX_TEMPLATE_TOKENS:
                self.topics_array_split.append(curr)
                curr = []
            else:
                curr.append(topic)
        if len(curr) > 0:
            self.topics_array_split.append(curr)

    def predict(self):
        """
        Returns
        ----------
        lst : A subset of the topics that are relevant to the topic area.
        """
        # If get_topics has been called on the same messages array
        # Then use the previous results
        hash_docs = hash(frozenset(self.topics))
        if hash_docs in self.memo_filtered_topics:
            return self.memo_filtered_topics[hash_docs]
        print("Filtering topics...")
        filtered_top_topics = []
        for i in tqdm(range(len(self.topics_array_split)), ncols=0):
            not_topics = self.__filter_top_topics(self.topics_array_split[i])
            filtered_top_topics.extend(list(
                set(self.topics_array_split[i]) - set(not_topics)))

        self.memo_filtered_topics[hash_docs] = filtered_top_topics
        return filtered_top_topics

    def __filter_top_topics(self, topics_in_list):
        prompt = {
            "{{topics_in_list}}": f"{topics_in_list}", "{{topic_type}}": self.topic_type}
        output = self.model.predict(
            prompt, max_tokens=500, temperature=0.7,)
        output = self.__parse_output(output)
        return output

    def __parse_output(self, output):
        list_pattern = re.compile(r"\d+\.\s")
        # include enumerated list prompt
        items = list_pattern.sub("", f'1. {output}')
        parsed = []
        for i in items.split('\n'):
            ii = i.split(',')
            stripped = [iii.strip().replace('.', '') for iii in ii if iii]
            parsed.extend(stripped)
        return parsed

    def __count_tokens(self, string):
        return len(string) // 4
