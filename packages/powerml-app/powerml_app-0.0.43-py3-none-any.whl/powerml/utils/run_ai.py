from typing import Optional
import requests
import logging
from powerml.utils.config import get_config
import backoff
from powerml.utils.constants import N_LOGPROBS

logger = logging.getLogger(__name__)


def query_powerml(prompt,
                  stop="",
                  model="llama",
                  max_tokens=128,
                  temperature=0,
                  config={},
                  allowed_tokens=None,
                  ):
    text, _ = query_powerml_with_probability(prompt=prompt,
                                             stop=stop,
                                             model=model,
                                             max_tokens=max_tokens,
                                             temperature=temperature,
                                             config=config,
                                             allowed_tokens=allowed_tokens)
    return text


def query_powerml_with_probability(prompt,
                                   stop="",
                                   model="llama",
                                   max_tokens=128,
                                   temperature=0,
                                   config={},
                                   allowed_tokens=None,
                                   ):
    key, url = get_url_and_key(config)
    params = {
        "prompt": prompt,
        "model": model,
        "max_tokens": max_tokens,
        "stop": stop,
        "temperature": temperature,
    }
    if allowed_tokens is not None:
        params["allowed_tokens"] = allowed_tokens
    resp = powerml_completions(params, url, key)
    resp = resp.json()
    if 'error' in resp:
        raise Exception(str(resp))
    text = resp['choices'][0]['text']
    return text, resp['probability']


def batch_query_powerml(prompt,
                        stop="",
                        model="llama",
                        max_tokens=128,
                        temperature=0,
                        config={},
                        ):
    key, url = get_url_and_key(config)
    params = {
        "prompt": prompt,
        "model": model,
        "max_tokens": max_tokens,
        "stop": stop,
        "temperature": temperature,
    }
    resp = powerml_completions(params, url, key)
    resp = resp.json()
    if 'error' in resp:
        raise Exception(str(resp))
    text = [chosen['text'] for chosen in resp['choices']]
    return text


def mutation_powerml_train(dataset: str, name: Optional[str], model: str, is_public: bool, config={},):
    key, url = get_url_and_key(config)
    params = {
        "dataset": dataset,
        "model": model,
        "public": is_public,
    }
    if name is not None:
        params['name'] = name
    return powerml_train(params, url, key)


def query_openai(prompt,
                 stop="",
                 model="llama",
                 max_tokens=128,
                 temperature=0,
                 key="",
                 allowed_tokens=None,
                 ):
    text, _ = query_openai_with_logprobs(
        prompt, stop, model, max_tokens, temperature, key, allowed_tokens)
    return text


def batch_query_openai(prompt,
                       stop="",
                       model="llama",
                       max_tokens=128,
                       temperature=0,
                       key="",
                       allowed_tokens=None,
                       ):
    text, _ = batch_query_openai_with_logprobs(
        prompt, stop, model, max_tokens, temperature, key, allowed_tokens)
    return text


def query_openai_with_logprobs(prompt,
                               stop="",
                               model="llama",
                               max_tokens=128,
                               temperature=0,
                               key="",
                               allowed_tokens=None,
                               n_logprobs=N_LOGPROBS,
                               ):
    resp = query_openai_helper(
        prompt, stop, model, max_tokens, temperature, key, allowed_tokens, n_logprobs)
    text = resp['choices'][0]['text']
    logprobs = resp['choices'][0]['logprobs']
    return text, logprobs


def batch_query_openai_with_logprobs(prompt,
                                     stop="",
                                     model="llama",
                                     max_tokens=128,
                                     temperature=0,
                                     key="",
                                     allowed_tokens=None,
                                     ):
    resp = query_openai_helper(
        prompt, stop, model, max_tokens, temperature, key, allowed_tokens)
    text = [chosen['text'] for chosen in resp['choices']]
    logprobs = resp['choices'][0]['logprobs']
    return text, logprobs


def query_openai_helper(prompt,
                        stop="",
                        model="llama",
                        max_tokens=128,
                        temperature=0,
                        key="",
                        allowed_tokens=None,
                        n_logprobs=None,
                        ):
    if key == "":
        cfg = get_config()
        key = cfg['openai.key']
    params = {
        "prompt": prompt,
        "model": model,
        "max_tokens": max_tokens,
        "stop": stop,
        "temperature": temperature,
        "logprobs": n_logprobs,
    }
    if allowed_tokens is not None:
        params["allowed_tokens"] = allowed_tokens
    resp = openai_completions(params, key)
    resp = resp.json()
    if 'error' in resp:
        raise Exception(str(resp))
    return resp


def get_url_and_key(config):
    cfg = get_config(config)
    key = cfg['powerml.key']
    if 'powerml.url' in cfg:
        url = cfg['powerml.url']
    else:
        url = 'https://api.powerml.co'
    return (key, url)


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=20)
def powerml_completions(params, url, key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
    }
    response = requests.post(
        url=url + "/v1/completions",
        headers=headers,
        json=params)
    if response.status_code == 429:
        raise requests.exceptions.RequestException
    elif response.status_code != 200:
        try:
            description = response.json()
        except BaseException:
            description = response.status_code
        finally:
            raise Exception(f"API error {description}")
    return response


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=20)
def openai_completions(params, key):
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json", }
    response = requests.post(
        url="https://api.openai.com/v1/completions",
        headers=headers,
        json=params)
    if response.status_code == 429:
        raise requests.exceptions.RequestException
    return response


def powerml_train(params, url, key):
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json", }
    response = requests.post(
        headers=headers,
        url=url + "/v1/train",
        json=params)
    if response.status_code != 200:
        try:
            description = response.json()
        except BaseException:
            description = response.status_code
        finally:
            raise Exception(f"API error {description}")
    description = response.json()
    if 'model' not in description:
        raise Exception(f"API error {description}")
    return response
