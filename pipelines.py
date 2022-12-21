import json
import ruamel.yaml as yaml
import requests
import urllib.parse
import os

def get_urls(user=None):
    pipeline_urls = []
    if 'PIPELINES_URL' in os.environ:
        pipeline_urls = [os.getenv('PIPELINES_URL')]

    if user is not None:
        from app.plugins import get_current_plugin
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
            try:
                pipeline = yaml.safe_load(response.text)
                pipelines.extend(pipeline['pipelines'])
            except (Exception) as e:
                from app.plugins import logger
                logger.error("Error parsing yaml:" + str(e))
                pass

    return pipelines

def get_nexturl(pipeline):
    #Set the open function, will alert and abort if inputs not available
    function = 'pipeline_run';
    if "inputs" in pipeline and "task" in pipeline["inputs"]:
        function = 'pipeline_task';
    elif "inputs" in pipeline and "project" in pipeline["inputs"]:
        function = 'pipeline_project';

    #Construct the next= url
    tag = pipeline["tag"]
    image = pipeline["image"]
    branch = ""
    requirements = ""
    # - Source repository and repo checkout dest dir
    if ':' in pipeline["source"]:
        #Provided a full repo URL
        repo = pipeline["source"]
        target = tag #Use the tag as the dest dir
        # - Entrypoint path
        path = os.path.join(target, pipeline["entrypoint"])
        # - Requirements file (optional)
        if "requirements" in pipeline:
            requirements = "&requirements" + pipeline["requirements"]
    else:
        repo = os.getenv('PIPELINE_REPO', "https://github.com/auscalabledronecloud/pipelines-jupyter")
        target = 'pipelines'
        # - Entrypoint path
        #(NOTE: can be confusing, but assumes entrypoint relative to source subdir)
        path = os.path.join("pipelines", pipeline["source"], pipeline["entrypoint"])
        # - Requirements file (optional)
        if "requirements" in pipeline:
            #Same with requirements, assumes relative to source subdir
            requirements = "&requirements" + os.path.join(pipeline["source"], pipeline["requirements"])
    # - Branch (optional)
    if "branch" in pipeline:
        branch = "&branch=" + pipeline["branch"]
    #branch = "&branch=" + (pipeline["branch"] if "branch" in p else "main") #Seems to require branch

    #Encode urlpath, then re-encode entire next url
    #(NOTE: need to replace PROJECTS and TASKS with data in js)
    #from app.plugins import logger
    urlpath = f'asdc/redirect?projects=PROJECTS&tasks=TASKS&path={path}'
    urlpath = urllib.parse.quote_plus(urlpath)
    nexturl = f"/user-redirect/{image}/git-pull?repo={repo}{branch}&targetpath={target}{requirements}&urlpath={urlpath}"
    #logger.info("NEXTURL0: " + str(nexturl))
    nexturl = urllib.parse.quote_plus(nexturl)
    #logger.info("NEXTURL1: " + str(nexturl))
    print("NEXTURL: ", nexturl)
    return nexturl

def get_fullurl(pipeline, username):
    import os
    host = os.environ.get('WO_HOST')
    nexturl = get_nexturl(pipeline)
    image = pipeline['image']
    fullurl = f'https://jupyter.{host}/hub/spawn/{username}/{image}?profile={image}&next={nexturl}'
    #Fix for react bug, it decodes the url when rendering so encode again to counter this
    fullurl = urllib.parse.quote_plus(fullurl)
    return fullurl

