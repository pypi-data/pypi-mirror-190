from powerml import PowerML
import logging

logger = logging.getLogger(__name__)


class WriteEmailModel:
    def __init__(self, config={}, max_output_tokens=512, temperature=0.7):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config, "stensul/email-copy/v2")
        self.temperature = temperature

    def fit(self, examples):
        """
        Parameters
        ----------
        examples : list
            Takes a list of dictionaries where each dictionary has keys:
                subject: <subject>
                email: <email>
        """
        self.examples = examples

    def predict(self, subject: str):
        """
        Parameters
        ----------
        subject : str
            The company for which the email is being generated.
        """
        example_string = ''
        if hasattr(self, 'examples'):
            example_string = "\n\n".join(
                [f"company: {example['subject']}\n\nemail: {example['email']}" for example in self.examples])
        prompt = {
            "{{examples}}": example_string,
            "{{input}}": subject
        }
        output = self.model.predict(
            prompt,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )
        return self.__post_process(output)

    def __post_process(self, output):
        return output.strip()
