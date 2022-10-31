import json
import ruamel.yaml as yaml
import requests
import os
from app.plugins import get_current_plugin
from app.plugins import logger

def get_urls(user=None):
    pipeline_urls = []
    if 'PIPELINES_URL' in os.environ:
        pipeline_urls = [os.getenv('PIPELINES_URL')]

    if user is not None:
        ds = get_current_plugin().get_user_data_store(user)
        urls = ds.get_string('pipelines_url', "")
        if urls:
            pipeline_urls += urls.split(',')

    return pipeline_urls

def get_json(user=None):
    pipeline_urls = get_urls(user)

    pipelines = []
    for url in pipeline_urls:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            pipeline = yaml.safe_load(response.text)
            pipelines.extend(pipeline['pipelines'])

    return pipelines

