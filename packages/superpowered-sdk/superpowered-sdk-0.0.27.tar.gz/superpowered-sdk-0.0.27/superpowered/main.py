# TODO: make this more performant by using asyncio and aiohttp
# TODO: use deque for chat history since the order is reversed in time

# import aiohttp
# import asyncio
import base64
import requests
import random
import string

# declare global variables
global HEADERS
global models
global incantations
global knowledge_bases

HEADERS = None
models = {}
incantations = {}
knowledge_bases = {}


BASE_URL = 'https://58shnvgnlf.execute-api.us-east-1.amazonaws.com/sandbox/'


def get_models():
    url = BASE_URL + 'models'
    resp = requests.get(url, headers=HEADERS)
    resp = _format_http_response(resp)
    for model in resp['body']:
        m = Model(
            model_id=model['id'],
            model_spec=model['model_spec'],
            supp_id = model['supp_id'],
            description=model['description']
        )
        models[model['id']] = m


def get_incantations():
    url = BASE_URL + 'incantations'
    resp = requests.get(url, headers=HEADERS)
    resp = _format_http_response(resp)
    for incantation in resp['body']:
        inc = Incantation(
            incantation_id=incantation['id'],
            title=incantation['title'],
            text=incantation['text'],
            supp_id=incantation['supp_id'],
            description=incantation['description']
        )
        incantations[incantation['id']] = inc


def get_knowledge_bases():
    url = BASE_URL + 'knowledge_bases'
    resp = requests.get(url, headers=HEADERS)
    resp = _format_http_response(resp)
    for knowledge_base in resp['body']:
        kb = KnowledgeBase(
            title=knowledge_base['title'],
            kb_id=knowledge_base['id'],
            supp_id = knowledge_base['supp_id'],
            description=knowledge_base['description']
        )
        knowledge_bases[knowledge_base['id']] = kb


def init(api_key_id: str, api_key_secret: str, verbose: bool = False):
    global HEADERS
    global models
    global incantations
    global knowledge_bases

    token = base64.b64encode((f'{api_key_id}:{api_key_secret}').encode('utf-8')).decode('utf-8')
    HEADERS = {'Authorization': f'Bearer {token}'}

    # get the current state with models and incantations
    get_models()
    get_incantations()
    get_knowledge_bases()

    if verbose:
        print ("All models:", [model.title for model in models.values()])
        print ("All incantations:", [incantation.title for incantation in incantations.values()])
        print ("All knowledge bases:", [knowledge_base.title for knowledge_base in knowledge_bases.values()])


# exceptions
class NoApiKeyError(Exception):
    def __init__(self):
        super().__init__('No API key has been set. Please run check that your API key is correct and then run `superpowered.init(api_key)` before continuing')


def _format_http_response(resp: requests.Response):
    if resp.status_code != 200:
        if resp.status_code == 204:
            return {
                'http_code': resp.status_code,
                'body': None
            }
        else:
            #print ("Error:", resp.status_code)
            raise Exception(resp.status_code, resp.json())
    return {
        'http_code': resp.status_code,
        'body': resp.json()
    }


class Incantation:
    def __init__(self, title: str, text: str, supp_id: str = None, description: str = None, incantation_id: str = None):
        self.incantation_id = incantation_id
        self.title = title
        self.text = text
        self.supp_id = supp_id
        self.description = description
        self.is_deployed = self.incantation_id is not None

    def create(self):
        if self.is_deployed:
            raise Exception('This incantation has already been deployed: ' + self.incantation_id)
        url = BASE_URL + 'incantations'
        payload = {
            'title': self.title,
            'text': self.text,
        }
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        self.incantation_id = resp['body']['id']
        self.is_deployed = True
        incantations[resp['body']['id']] = self
        return resp['body']

    def update(self):
        if not self.is_deployed:
            raise Exception('This incantation has not been deployed yet. Please run `incantation.create()` before running `incantation.update()')
        url = BASE_URL + f'incantations/{self.incantation_id}'
        payload = {}
        if self.title is not None:
            payload['title'] = self.title
        if self.text is not None:
            payload['text'] = self.text
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.patch(url, headers=HEADERS, json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'incantations/{self.incantation_id}'
        _format_http_response(requests.delete(url, headers=HEADERS))
        del incantations[self.incantation_id]


class Model:
    def __init__(self, model_spec: dict, supp_id: str = None, description: str = None, model_id: str = None):
        self.model_id = model_id
        self.model_spec = model_spec
        self.title = model_spec['model_title']
        self.supp_id = supp_id
        self.description = description
        self.is_deployed = self.model_id is not None
        self.model_instances = self.get_instances()
        #print(locals())

    def create(self):
        if self.is_deployed:
            raise Exception('This model has already been deployed: ' + self.model_id)
        url = BASE_URL + 'models'
        payload = {
            'model_spec': self.model_spec,
        }
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description

        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        self.model_id = resp['body']['id']
        self.is_deployed = True
        models[resp['body']['id']] = self
        return resp['body']

    def update(self):
        if not self.is_deployed:
            raise Exception('This model has not been deployed yet. Please run `model.create()` before running `model.update()')
        url = BASE_URL + f'models/{self.model_id}'
        payload = {}
        if self.model_spec is not None:
            payload['model_spec'] = self.model_spec
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.patch(url, headers=HEADERS, json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'models/{self.model_id}'
        _format_http_response(requests.delete(url, headers=HEADERS))
        del models[self.model_id]

    def get_instances(self):
        url = BASE_URL + f'models/{self.model_id}/instances'
        resp = _format_http_response(requests.get(url, headers=HEADERS))
        instances = {}
        for instance in resp['body']:
            inst = ModelInstance(
                ai_name=instance['ai_name'],
                model_id=instance['model_id'],
                supp_id=instance['supp_id'],
                description=instance['description'],
                instance_id=instance['id'],
            )
            instances[instance['id']] = inst
        return instances

    # convenience method
    def create_instance(self, ai_name: str = "AI", knowledge_bases: list = None):
        instance_obj = ModelInstance(model_id=self.model_id, ai_name=ai_name, knowledge_bases=knowledge_bases)
        resp_body = instance_obj.create()
        return instance_obj

    # convenience method for non-conversational use case - TODO: this is not an efficient way to do this
    def run(self, prompt: str) -> str:
        # create a new instance
        instance_obj = self.create_instance()
        instance_id = instance_obj.instance_id

        # get the response
        url = BASE_URL + f'models/{self.model_id}/instances/{instance_id}/get_response'
        human_input = [{"prefix": "", "content": prompt}]
        payload = {
            'human_input': human_input
        }
        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        return resp['body']['model_response']['content']

class ModelInstance:
    def __init__(self, ai_name: str, knowledge_bases: list = None, model_id: str = None, supp_id: str = None, description: str = None, instance_id = None):
        self.ai_name = ai_name
        self.knowledge_bases = knowledge_bases # list of knowledge base ids
        self.model_id = model_id
        self.supp_id = supp_id
        self.description = description
        self.instance_id = instance_id
        self.chat_history = []
        self.get_chat_history()
        self.is_deployed = self.instance_id is not None

    def get_chat_history(self):
        # get chat history interactions with pagination
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}/chat_history'
        response = _format_http_response(requests.get(url, headers=HEADERS))
        self.chat_history.extend(response['body']['interactions'])
        while 'next_page_token' in response:
            response = _format_http_response(requests.get(url, headers=HEADERS, params={'next_page_token': response['next_page_token']}))
            self.chat_history.extend(response['body']['interactions'])

    def create(self):
        if self.is_deployed:
            raise Exception('This model instance has already been deployed: ' + self.instance_id)
        url = BASE_URL + f'models/{self.model_id}/instances'
        payload = {'ai_name': self.ai_name}
        if self.knowledge_bases is not None:
            payload['knowledge_bases'] = self.knowledge_bases
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        self.instance_id = resp['body']['id']
        self.is_deployed = True
        models[self.model_id].model_instances[self.instance_id] = self
        return resp['body']

    def update(self):
        if not self.is_deployed:
            raise Exception('This model instance has not been deployed yet. Please run `model_instance.create()` before running `model_instance.update()')
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}'
        payload = {}
        if self.knowledge_bases is not None:
            payload['knowledge_bases'] = self.knowledge_bases
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.patch(url, headers=HEADERS, json=payload))
        return resp['body']

    def delete(self):
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}'
        resp = _format_http_response(requests.delete(url, headers=HEADERS))
        return resp['body']

    def respond(self, human_input: list):
        url = BASE_URL + f'models/{self.model_id}/instances/{self.instance_id}/get_response'
        payload = {
            'human_input': human_input
        }
        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        self.chat_history.insert(0, resp['body']['interaction'])
        return resp['body']


class KnowledgeBase:
    def __init__(self, title: str, supp_id: str = None, description: str = None, kb_id: str = None):
        self.title = title
        self.supp_id = supp_id
        self.description = description
        self.kb_id = kb_id
        self.is_deployed = self.kb_id is not None

    def create(self):
        if self.is_deployed:
            raise Exception('This knowledge base has already been deployed: ' + self.kb_id)
        url = BASE_URL + 'knowledge_bases'
        payload = {
            'title': self.title
        }
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        self.kb_id = resp['body']['id']
        self.is_deployed = True
        knowledge_bases[self.kb_id] = self
        return resp['body']

    def add_file(self, content: str, title: str = None, link_to_source: str = None, supp_id: str = None, description: str = None):
        kb_file = KnowledgeBaseFile(kb_id=self.kb_id, content=content, title=title, link_to_source=link_to_source, supp_id=supp_id, description=description)
        resp_body = kb_file.create()
        return resp_body

    def get_files(self):
        url = BASE_URL + f'knowledge_bases/{self.kb_id}/files'
        resp = _format_http_response(requests.get(url, headers=HEADERS))
        files = {}
        for file in resp['body']:
            kb_file = KnowledgeBaseFile(
                kb_id=file['id'],
                content=file['content'],
                title=file['title'],
                link_to_source=file['link_to_source'],
                supp_id=file['supp_id'],
                description=file['description'],
            )
            files[file['id']] = kb_file
        return files


class KnowledgeBaseFile:
    def __init__(self, kb_id: str, content: str, title: str = None, link_to_source: str = None, supp_id: str = None, description: str = None):
        self.kb_id = kb_id
        self.content = content # content is a string
        self.title = title
        self.link_to_source = link_to_source
        self.supp_id = supp_id
        self.description = description

    def create(self):
        url = BASE_URL + f'knowledge_bases/{self.kb_id}/files'
        payload = {
            'content': self.content
        }
        if self.title is not None:
            payload['title'] = self.title
        if self.link_to_source is not None:
            payload['link_to_source'] = self.link_to_source
        if self.supp_id is not None:
            payload['supp_id'] = self.supp_id
        if self.description is not None:
            payload['description'] = self.description
        resp = _format_http_response(requests.post(url, headers=HEADERS, json=payload))
        return resp['body']


# use this to handle different formats of model_spec
def model_spec_preprocessing(model_spec: dict):
    # if incantation_names is in the model_spec, replace it with incantation_ids
    if "incantation_names" in model_spec and "incantation_ids" not in model_spec:
        incantation_names = model_spec["incantation_names"]
        incantation_ids = []
        for incantation_name in incantation_names:
            incantation_ids.append(get_incantation(incantation_name).incantation_id)
        model_spec["incantation_ids"] = incantation_ids
        del model_spec["incantation_names"] 
    return model_spec

# create_incantation() is a convenience function that creates an Incantation object and then calls its create() method
def create_incantation(title: str, text: str):
    incantation_obj = Incantation(title=title, text=text)
    body_resp = incantation_obj.create()
    return incantation_obj

# get_incantation() is a convenience function that returns an Incantation object for an existing incantation, given its title
def get_incantation(incantation_title: str):
    # create incantation name to id map - incantations is a dict of incantation objects keyed on incantation_id
    incantation_from_title = {}
    for incantation_id in incantations.keys():
        incantation = incantations[incantation_id] # get the Incantation object
        title = incantation.title
        if title not in incantation_from_title:
            incantation_from_title[title] = incantation
        else:
            raise Exception('Duplicate incantation title: ' + title)
    
    if incantation_title in incantation_from_title:
        return incantation_from_title[incantation_title]
    else:
        raise Exception('Incantation title not found: ' + incantation_title)

# update_incantation() is a convenience function that updates an existing incantation, given its title
def update_incantation(incantation_title: str, new_text: str = None, new_title: str = None):
    incantation_obj = get_incantation(incantation_title)
    if new_title is not None:
        incantation_obj.title = new_title
    if new_text is not None:
        incantation_obj.text = new_text
    body_resp = incantation_obj.update()
    return incantation_obj

# create_model() is a convenience function that creates a Model object and then calls its create() method
def create_model(model_spec: dict = {}, verbose: bool = False):
    if model_spec == {}:
        model_spec = {
            "incantation_names": [],
            "title": "Untitled model",
        }
    model_spec = model_spec_preprocessing(model_spec)
    if verbose: print ("Model spec:\n", model_spec)
    model_obj = Model(model_spec=model_spec)
    body_resp = model_obj.create()
    return model_obj

# get_model() is a convenience function that returns a Model object for an existing model, given its title
def get_model(model_title: str):
    # create model name to id map - models is a dict of model objects keyed on model_id
    model_from_title = {}
    for model_id in models.keys():
        model = models[model_id] # get the Model object
        title = model.title
        if title not in model_from_title:
            model_from_title[title] = model
        else:
            pass #raise Exception('Duplicate model title: ' + title)
    
    if model_title in model_from_title:
        return model_from_title[model_title]
    else:
        raise Exception('Model title not found: ' + model_title)

# update_model() is a convenience function that updates an existing model, given its title and a new model_spec
def update_model(model_title: str, new_model_spec: dict):
    new_model_spec = model_spec_preprocessing(new_model_spec)
    model_obj = get_model(model_title)
    current_model_spec = model_obj.model_spec
    
    # just update the keys that are in the new_model_spec
    for key in new_model_spec.keys():
        current_model_spec[key] = new_model_spec[key]
    model_obj.model_spec = current_model_spec
    resp_body = model_obj.update()
    return model_obj

# create_knowledge_base() is a convenience function that creates a KnowledgeBase object and then calls its create() method
def create_knowledge_base(title: str, supp_id: str = None, description: str = None):
    kb = KnowledgeBase(title, supp_id, description)
    resp = kb.create()
    return kb

# get_knowledge_base() is a convenience function that returns a KnowledgeBase object for an existing knowledge base, given its title
def get_knowledge_base(title: str):
    # create knowledge base name to id map - knowledge_bases is a dict of knowledge base objects keyed on knowledge_base_id
    kb_from_title = {}
    for kb_id in knowledge_bases.keys():
        kb = knowledge_bases[kb_id] # get the KnowledgeBase object
        title = kb.title
        if title not in kb_from_title:
            kb_from_title[title] = kb
        else:
            raise Exception('Duplicate knowledge base title: ' + title)
    
    if title in kb_from_title:
        return kb_from_title[title]
    else:
        raise Exception('Knowledge base title not found: ' + title)


# list_incantations() is a convenience function that returns a dictionary of all Incantation objects for an account
def list_incantations(verbose=False):
    if verbose:
        print ("\nIncantations:")
        for incantation_obj in incantations.values():
            print (f"id: {incantation_obj.incantation_id}\ntitle: {incantation_obj.title}\ntext: {incantation_obj.text}\n")
    return incantations

# list_models() is a convenience function that returns a dictionary of all Model objects for an account
def list_models(verbose=False):
    if verbose:
        print ("\nModels:")
        for model_obj in models.values():
            print (f"id: {model_obj.model_id}\ntitle: {model_obj.title}\nmodel_spec: {model_obj.model_spec}\n")
    return models

# list_instances() is a convenience function that returns a dictionary of ModelInstance objects for an existing model, given its title
def list_instances(model_title: str, verbose=False):
    model = get_model(model_title)
    instances = model.get_instances()
    if verbose:
        print ("\nModel instances:")
        for instance_obj in instances.values():
            print (f"id: {instance_obj.instance_id}\nai name: {instance_obj.ai_name}\nlast chat: {instance_obj.chat_history[:1]}\n")
    return instances

# list_knowledge_bases() is a convenience function that returns a dictionary of all KnowledgeBase objects for an account
def list_knowledge_bases(verbose=False):
    if verbose:
        print ("\nKnowledge bases:")
        for kb_obj in knowledge_bases.values():
            print (f"id: {kb_obj.kb_id}\ntitle: {kb_obj.title}\n")
    return knowledge_bases

# list_files() is a convenience function that returns a dictionary of File objects for an existing knowledge base, given its title
def list_files_in_kb(kb_title: str, verbose=False):
    kb = get_knowledge_base(kb_title)
    files = kb.get_files()
    if verbose:
        print ("\nFiles:")
        for file_obj in files.values():
            print (f"title: {file_obj.title}\ncontent: {file_obj.content[:100]}\n\n")
    return files

# add a file to a knowledge base
def add_file_to_kb(kb_title: str, file_path: str, file_type: str = None):
    kb = get_knowledge_base(kb_title)
    if file_type is None:
        file_type = file_path.split(".")[-1]
    
    if file_type == "txt":
        with open(file_path, 'r') as f:
            # read the file and convert it to a string
            content = f.read()
    else:
        raise Exception("File type not supported: " + file_type)
    
    # make the title a random string
    title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    kb.add_file(content=content, title=title)