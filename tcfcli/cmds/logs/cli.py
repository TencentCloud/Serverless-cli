import click
import time
from datetime import datetime
from datetime import timedelta
import tcfcli.common.base_infor as infor
from tcfcli.common.user_exceptions import *
from tcfcli.cmds.native.common.invoke_context import InvokeContext
from tcfcli.cmds.local.common.options import invoke_common_options
from tcfcli.common.user_exceptions import InvalidEnvParameters
from tcfcli.common.scf_client.scf_log_client import ScfLogClient
from tcfcli.help.message import LogsHelp as help

TM_FORMAT = '%Y-%m-%d %H:%M:%S'
REGIONS = infor.REGIONS


@click.command(short_help=help.SHORT_HELP)
@click.option('-n', '--name', help=help.NAME)
@click.option('-ns', '--namespace', default="default", help=help.NAMESPACE)
@click.option('--region', default=None, help=help.REGION)
@click.option('-c', '--count', type=int, help=help.COUNT)
@click.option('-s', '--start-time', type=str, default=None, help=help.START_TIME)
@click.option('-e', '--end-time', type=str, default=None, help=help.END_TIMEE)
@click.option('-d', '--duration', type=int, default=None, help=help.DURATION)
@click.option('-f', '--failed', is_flag=True, default=False, help=help.FAILED)
@click.option('-t', '--tail', is_flag=True, default=False, help=help.TAIL)
def logs(name, namespace, region, count, start_time, end_time, duration, failed, tail):
    """
    \b
    Scf cli can use the logs command to view historical or real-time logs generated by cloud functions.
    \b
    Common usage:
        \b
        * Fetch logs using the function's name
          $ scf logs -n(--name) function
        \b
        * Specify a namespace, the default value is 'default'
          $ scf logs -n function -ns(--namespace) nodefault
        \b
        * Specific time range using the -s (--starttime) and -e (--endtime) options
          $ scf logs -n function -s xxxx-xx-xx 00:00:00 -e xxxx-xx-xx 00:00:10
        \b
        * Specify a duration between starttime and current time(unit:second)
          $ scf logs -n function -d(--duration)  10
        \b
        * Fetch logs that was exceptional
          $ scf logs -n function  -f(--failed)
        \b
        * Specify region of service
          $ scf logs -n function --region ap-guangzhou
    """

    if region and region not in REGIONS:
        raise ArgsException("The region must in %s." % (", ".join(REGIONS)))
    else:
        if name is None:
            raise InvalidEnvParameters("Function name is unspecif")

        if duration and (start_time or end_time):
            raise InvalidEnvParameters("Duration is conflict with (start_time, end_time)")

        if tail:
            start = datetime.now()
            end = start + timedelta(days=1)
            if count:
                end = start
                start = end - timedelta(days=1)
        else:
            start, end = _align_time(start_time, end_time, duration)
        client = ScfLogClient(name, namespace, region, failed)
        if tail and count:
            client.fetch_log_tail_c(start.strftime(TM_FORMAT),
                                    end.strftime(TM_FORMAT), count, tail)
            return
        if not count:
            count = 10000  # cloudapi limit
        client.fetch_log(start.strftime(TM_FORMAT), end.strftime(TM_FORMAT), count, tail)


def _align_time(_start, _end, _offset):
    start = end = None
    if _start:
        start = datetime.strptime(_start, TM_FORMAT)

    if _end:
        end = datetime.strptime(_end, TM_FORMAT)

    if _offset:
        end = datetime.now()
        start = end - timedelta(seconds=_offset)
    elif start and end:
        pass
    elif (not start) and (not end):
        end = datetime.now()
        start = end - timedelta(seconds=60)
    elif not start:
        raise InvalidEnvParameters("start-time name is unspecified")
    else:
        raise InvalidEnvParameters("end-time name is unspecified")

    if start >= end:
        raise InvalidEnvParameters("endtime must be greater than starttime")
    return start, end
