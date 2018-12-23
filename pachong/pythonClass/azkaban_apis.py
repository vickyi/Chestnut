#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import datetime,time
import sys, getopt

headers = {'Content-Type': 'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'}
internet_url = "http://azkaban.azkaban.net"
outernet_url = "http://localhost:8888"

def azkaban_authenticate():
    data = {"action":"login","username":"username","password":"password"}
    resp = requests.post(
        internet_url,
        data=data,
        headers=headers)

    session_id = resp.json().get("session.id")
    status = resp.json().get("status")

    return status, session_id

def execute_a_flow(project_name, flow_name, param_date, session_id):

    # see: http://docs.python-requests.org/zh_CN/latest/api.html#requests.Response
    # status, session_id = azkaban_authenticate()
    print("call func: %s, params: [%s=%s], [%s=%s, [%s=%s], [%s=%s]" \
    %("execute_a_flow", \
    "project_name", project_name, \
    "flow_name", flow_name, \
    "param_date", param_date, \
    "session_id", session_id))

    data = {}
    data["session.id"] = session_id
    data["ajax"] = "executeFlow"
    data["project"] = project_name
    data["flow"] = flow_name
    data["flowOverride[param.date]"] = param_date

    url = internet_url + "/executor"

    resp = requests.get(
        url,
        params=data,
        headers=headers)

    return resp.json()


def fetch_jobs_of_a_flow(project_name, flow_name):

    status, session_id = azkaban_authenticate()
    # print("azkaban_authenticate, session_id:" + session_id)
    data = {}
    data["session.id"] = session_id
    data["ajax"] = "fetchflowgraph"
    data["project"] = project_name
    data["flow"] = flow_name
    url = internet_url + "/manager"

    resp = requests.get(
        url,
        data=data,
        headers=headers)

    return resp.json()

def get_running_flow(project_name, flow_name, session_id):

    # see: http://docs.python-requests.org/zh_CN/latest/api.html#requests.Response
    data = {}
    data["session.id"] = session_id
    data["ajax"] = "getRunning"
    data["project"] = project_name
    data["flow"] = flow_name

    url = internet_url + "/executor"

    resp = requests.get(
        url,
        params=data,
        headers=headers)

    execIds = resp.json().get("execIds")
    return execIds

def flush_flow(project, flow, start_date, end_date):
    begin = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    end = datetime.datetime.strptime(end_date,"%Y-%m-%d")

    status, session_id = azkaban_authenticate()

    # see https://stackoverflow.com/questions/466345/converting-string-into-datetime
    dt = begin
    delta = datetime.timedelta(days=1)
    secs = 5
    # resp_json = execute_a_flow(project, flow, begin, session_id)
    execid = 0
    running_date = begin.strftime("%Y-%m-%d")

    while dt <= end:
        dateStr = dt.strftime("%Y-%m-%d")

        execIds = get_running_flow(project, flow, session_id)

        ## 如果当前 flow 的 execid 在 running 的 execIds 中，则程序暂停 2 秒。
        if (execIds is None) or execid not in execIds:
            resp_json = execute_a_flow(project, flow, dateStr, session_id)
            running_date = dateStr
            execid = resp_json.get("execid")
            print("flush_a_flow: %s, dateStr=%s, execid=%s" %(flow, running_date, execid))
            dt += delta
        else:
            print("Azkaban Project=%s, Flow=%s, date=%s, execid=%s is running! please wait for %s seconds..." %(project, flow, running_date, execid, secs))
            time.sleep(secs)

def usage():
    print("Usage: ")
    print("azkaban_apis.py -m <api_methond> -p <azkaban_project> -f <flow> --start_date <date,format:yyyy-MM-dd> --end_date <date,format:yyyy-MM-dd>")
    print("eg1: ")
    print("python azkaban_apis.py -m flush_flow -p flow_test -f flow_test --start_date 2018-12-15 --end_date 2018-12-15")
    print("eg2: ")
    print("python azkaban_apis.py -m flush_flow -p crm -f crm --start_date 2018-12-07 --end_date 2018-12-21")

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:p:f:t:h", ["help", "method=", "project=", "flow=", "datetime=", "start_date=", "end_date="])
    except getopt.GetoptError:
        print("请输入正确的参数，--help 查看命令使用")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-m", "--method"):
            method = arg
        elif opt in ("-p", "--project"):
            project = arg
        elif opt in ("-f", "--flow"):
            flow = arg
        elif opt in ("--start_date"):
            start_date = arg
        elif opt in ("--end_date"):
            end_date = arg
        elif opt in ("-h", "--help"):
            usage()
        else:
            print("unhandled option")
            assert False, "unhandled option"

    # switcher = {
    #     "auth": azkaban_authenticate,
    #     "flush_flow": flush_flow,
    #     "fetch_flow": fetch_jobs_of_a_flow,
    #     None: sys.exit(2)
    # }

    if method == "flush_flow":
        print("call flush flow ...")
        flush_flow(project, flow, start_date, end_date)
    else:
        assert False, "unhandled azkaban api!"
    # method, project, flow, start_date, end_date
    # func = switcher.get(method,switcher[None])()

if __name__ == "__main__":
    main(sys.argv[1:])
