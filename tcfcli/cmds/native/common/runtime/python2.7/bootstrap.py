#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
if sys.version_info[0] != 2 or sys.version_info[1] < 7:
    print("The version of python({}) don't match the Runtime version".format(str(sys.version_info)))
    print("If you install python2.7,please try cmd `scf configure set --python2-path Your_python2.7_path`")
    print("You can use cmd `which python` to show your python path in Linux OS")
    print("You can use cmd `where python` to show your python path in Windows Os")
    sys.exit(233)
import imp
import json
import logging
import traceback
from decimal import Decimal
import runtime

init_handler_fault = 'function initialization failed'
max_ret_msg_len = 6*1024*1024 #byte
max_ret_msg_len_exceed_error = 'body size is too long'
module_save = list(sys.modules.keys())

class CustomIO(object):
    def __init__(self, fd):
        self._fd = fd

    def __getattr__(self, attr):
        return getattr(self._fd, attr)

    def write(self, msg):
        if 'unicode' in dir(__builtins__) and type(msg) == unicode:
            msg = msg.encode('utf8')
        runtime.console_log(str(msg))
        self._fd.flush()

    def writelines(self, msgs):
        for msg in msgs:
            if 'unicode' in dir(__builtins__) and type(msg) == unicode:
                msg = msg.encode('utf8')
            runtime.console_log(str(msg))
        self._fd.flush()

def main():
    sys.stdout = CustomIO(sys.stdout)
    sys.stderr = CustomIO(sys.stderr)

    # log to stdout for capturing
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(handler)

    if 0 != runtime.init():
        print('runtime init failed')
        return
    runtime.log('init succ')

    clean_env()

    http_handler, event_handler = None, None
    while True:
        invoke_info = runtime.wait_for_invoke()
        mode, sockfd, event, context = invoke_info.cmd, invoke_info.sockfd, invoke_info.event, invoke_info.context
        #将用户的项目目录放入sys.path,防止用户引用目录下自定义的包模块报错
        try:
            file_path = (context.rsplit(':', 1)[0]+'.py')
            file_dir_path = os.path.dirname(file_path)
            sys.path.append(file_dir_path)
        except Exception as e:
            print (e)
        if mode == 'RELOAD':
            runtime.log('get reload request: %s' % context)
            http_handler, event_handler = init_handler(*(context.split(":")[-2:]))
            runtime.log('handlers reloaded')
            continue

        if event or context:
            try:
                event = eval(event)
                context = eval(context)
            except Exception as ex:
                runtime.report_running()
                runtime.report_fail('eval event[%s] or context[%s] failed\n%s'%(event, context, str(ex)), 0, 1)
                continue

        for env in context['environ'].split(';'):
            if not env:
                continue
            k, v = env.split('=', 1)
            os.environ[k] = v

        runtime.log('request[%s] invoked' % context.get('request_id'))

        if not http_handler and not event_handler:
            runtime.report_running()
            runtime.report_fail(init_handler_fault, 0, 2)
            continue

        if mode == 'HTTP':
            http_handler.handle(sockfd)
        elif mode == 'EVENT':
            event_handler.handle(event, context)
        else:
            runtime.log('recv unknown task type: %s' % mode)

        runtime.log('process finished')

def init_handler(file, func):
    try:
        func_handler = get_func_handler(file, func)
    except Exception as ex:
        runtime.log('get user function[%s:%s] failed' % (file, func))
        runtime.log(str(ex))
        global init_handler_fault
        init_handler_fault = str(ex)
        return None, None

    return HttpHandler(func_handler), EventHandler(func_handler)

def get_func_handler(mname, fname):
    need_del_module = []
    try:
        for item in sys.modules:
            if item not in module_save:
                need_del_module.append(item)
        for item in need_del_module:
            del sys.modules[item]
    except Exception as ex:
        runtime.log("del old module err" + str(ex))

    # change the current working directory
    current_path = os.path.dirname(mname+".py")
    os.chdir(current_path)
    runtime.log('working directory: %s' % os.getcwd())

    module = imp.load_source("", mname+".py")
    return getattr(module, fname)

class HttpHandler(object):
    def __init__(self, handler):
        self.real_handler = handler

    def handle(self, fd):
        pass

class EventHandler(object):
    def __init__(self, handler):
        self.real_handler = handler

    def handle(self, event, context):
        try:
            runtime.report_running()
            ret = self.real_handler(event, context)
            if type(ret) == Decimal:
                ret = str(ret)
            ret = json.dumps(ret, ensure_ascii=False)
            if len(ret) > max_ret_msg_len:
                runtime.report_fail(max_ret_msg_len_exceed_error, 0, 1)
            else:
                runtime.report_done(ret, 0)
        except Exception as ex:
            stack_trace = traceback.format_exc().splitlines()
            # erase current frame
            del stack_trace[1]
            del stack_trace[1]
            runtime.report_fail('\n'.join(stack_trace), 0, 2)

def clean_env():
    env_to_delete = ['SOCKETPATH', 'CONTAINERID']
    for k in os.environ.keys():
        if k.startswith('KUBERNETES'):
            env_to_delete.append(k)

    for k in env_to_delete:
        del os.environ[k]

if __name__ == '__main__':
    main()
