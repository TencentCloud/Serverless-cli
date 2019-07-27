'''
    Powered by Dfounderliu
    Email: dfounderliu@tencent.com

    Help Information
'''

import click

REGIONS = ['ap-beijing', 'ap-chengdu', 'ap-guangzhou', 'ap-hongkong', 'ap-mumbai', 'ap-shanghai']
REGIONS_STR = click.style("%s" % (", ".join(REGIONS)), fg='green')

RUNTIME = ["python3.6", "python2.7", "go1", "php5", "php7", "nodejs6.10", "nodejs8.9"]
RUNTIME_STR = click.style("%s" % (", ".join(RUNTIME)), fg='green')


class CommonHelp():
    # Common Help Message

    NAME = "Function name."
    NAMESPACE = "Namespace name."
    HELP_MESSAGE = "Show the help and exit."

    EVENTS_CMQ = "CMQ event."
    EVENTS_CMQ_NOTIFICATION = "Generates an CMQ Topic notification event."


    EVENTS_CKAFKA = "Ckafka event."
    EVENTS_CKAFKA_CONSUME = "Generates an ckafka consuming event."


    EVENTS_APIGATEWAY = "API Gateway event."
    EVENTS_APIGATEWAY_PROXY = "Generates an API Gateway proxy event."


    EVENTS_TIMER = "Timer event."
    EVENTS_TIMER_TIMEUP = "Generates an Timer event."


    EVENTS_COS = "COS Event."
    EVENTS_COS_PUT = "Generates an COS Put event."
    EVENTS_COS_POST = "Generates an COS Post event."
    EVENTS_COS_DELETE = "Generates an COS Delete event."


    INVOKE_ENV_VARS = 'JSON file contains function environment variables.'
    INVOKE_DEBUG_PORT = 'The port exposed for debugging. If specified, local container will start with debug mode.'
    INVOKE_DEBUGGER_PATH = 'The debugger path in host. If specified, the debugger will mounted into the function container.'
    INVOKE_DEBUG_ARGS = 'Additional args to be passed the debugger.'
    INVOKE_DOCKER_VOLUME_BASEDIR = 'The basedir where SCF template locate in.'
    INVOKE_DOCKER_NETWORK =  'Specifies the name or id of an existing docker network which containers should connect to, along with the default bridge network.'
    INVOKE_LOG_FILE = 'Path of logfile where send runtime logs to file.'
    INVOKE_SKIP_PULL_IMAGE = 'Specify whether CLI skip pulling or update docker images.'
    INVOKE_REGION = "The function region. Including %s" % REGIONS_STR

class DeleteHelp():
    # Delete Help Message

    SHORT_HELP = "Delete a SCF function."

    NAME = CommonHelp.NAME
    NAMESPACE = CommonHelp.NAMESPACE

    FORCED = "Force delete function without ask."
    REGION = "Region name. Including %s" % REGIONS_STR


class DeployHelp():
    # Deploy Help Message

    SHORT_HELP = "Deploy a SCF function."

    NAME = CommonHelp.NAME
    NAMESPACE = CommonHelp.NAMESPACE

    COS_BUCKET = "COS Bucket name."
    TEMPLATE_FILE = "SCF function template file."
    REGION = "The function will be deployed in this region. Including %s" % REGIONS_STR
    FORCED = "The function will be forced to update when it already exists. The default is False."
    SKIP_EVENT = "Triggers will continue with the previous setup and won't cover them this time."


class InitHelp():
    # Init Help Message

    SHORT_HELP = "Initialize a SCF function with the template"

    NAME = CommonHelp.NAME
    NAMESPACE = CommonHelp.NAMESPACE

    LOCATION = "Template location (git, mercurial, http(s), zip, path)"
    RUNTIME = "Runtime of this funtion. Including %s" % RUNTIME_STR
    OUTPUT_DIR = "The path where will output the initialized app into"
    NO_INPUT = "Disable prompting and accept default values defined template config"


class ConfigureHelp():
    # Configure Help Message

    SHORT_HELP = "Configure your account parameters."

    SECRET_ID = "TencentCloudAPI  SecretId"
    SECRET_KEY = "TencentCloudAPI  SecretKey"
    REGION = "TencentCloudAPI  Region"
    APPID = "TencentCloudAPI  Region"

    SET_SHORT_HELP = "Set your account parameters."
    SET_SECRET_ID = SECRET_ID
    SET_SECRET_KEY = SECRET_KEY
    SET_REGION = REGION
    SET_APPID = APPID

    GET_SHORT_HELP = "Get your account parameters."
    GET_SECRET_ID = SECRET_ID
    GET_SECRET_KEY = SECRET_KEY
    GET_REGION = REGION
    GET_APPID = APPID

class NativeHelp():
    # Native Help Message

    SHORT_HELP = "Run your SCF function natively for quick development."

    INVOKE_SHORT_HELP = "Execute the SCF function in a environment natively."
    INVOKE_EVENT = 'The source of the file for the simulated test event, the file content must be in JSON format.'
    INVOKE_NO_ENENT = "Without the source of the file for the simulated test. The default is False."
    INVOKE_ENV_VARS = "The environment variable configuration when the function is running, you need to specify the environment variable configuration file, the content must be in JSON format."
    INVOKE_TEMPLATE = "The path or file name of the configuration file. The default is template.yaml."
    INVKOE_DEBUG_PORT = 'The port exposed when the function is running. After the port is specified, the local runtime will start in debug mode and expose the specified port.'
    INVOKE_DEBUG_ARGS = 'The debugger startup parameters in this machine. After the parameter is specified, the specified parameters will be passed when the debugger starts.'
    INVOKE_QUIET = 'Only display what function return.'

class ValidateHelp():
    # Validate Help Message

    SHORT_HELP = "Validate a SCF template."

    TEMPLATE_FILE = "The SCF template file for Deploy."


class LogsHelp():
    # Logs Help Message

    SHORT_HELP = "Fetch logs of SCF function from service."

    NAME = CommonHelp.NAME
    NAMESPACE = CommonHelp.NAMESPACE

    REGION = "Specify the area where the function is located (e.g. ap-guangzhou)."
    COUNT = "The count of logs,the maximum value is 10000 and the minimum value is 1."
    START_TIME = "Get the log after the specified start time."
    END_TIMEE = "Get the log before the specified start time."
    DURATION = "The duration between starttime and current time (unit:second)."
    FAILED = "Get the log of the failed call."
    TAIL = "Get the latest real-time logs."


class LocalHelp():
    # Local Help Message

    SHORT_HELP = "Run SCF function locally."

    INVOKE_SHORT_HELP = "Execute SCF function in a docker environment locally."
    INVOKE_EVENT = 'The source of the file for the simulated test event, the file content must be in JSON format.'
    INVOKE_NO_ENENT = "Without the source of the file for the simulated test. The default is False."
    INVOKE_QUIET = 'Only display what function return.'


class ListHelp():
    # List Help Message
    SHORT_HELP = "Show the SCF function list."

    NAMESPACE = CommonHelp.NAMESPACE

    REGION = "The function region. Including %s" % REGIONS_STR