#!/usr/bin/python3

import os
import re
import signal
from threading import Thread
from journal import journal




module_name = "ModuleManager"
work_dir = "/etc/netping_modulemanager"
module_start_list = []
module_kill_list = []

def thrLaunch(command):
    os.system("python3 " + work_dir + "/" + command)
    journal.WriteLog(module_name, "Normal", "notice", command + " is finished!")

def launch():
    for e in module_start_list:
        #launch modules from e['modules']
        for m in e['modules']:
            cmd = "S{:02d}".format(e['priority']) + m
            thr = Thread(target=thrLaunch, args=(cmd,))
            thr.start()
            journal.WriteLog(module_name, "Normal", "notice", cmd + " is running!")
            e['thread'] = thr

def killAll():
    for e in module_kill_list:
        for m in e['modules']:
            cmd = "K{:02d}".format(e['priority']) + m
            os.system("python3 " + work_dir + "/" + cmd)
            journal.WriteLog(module_name, "Normal", "notice", cmd + " is stopped!")

def scandir():
    for _,_,files in os.walk(work_dir):
        for file in files:
            try:
                #for start entry
                args = re.findall(r'S([0-9]+)(\S+)', file)
                args = args[0]
                priority = int(args[0])
                module = args[1]

                #search exist in start list
                i = 0
                updated = False
                for e in module_start_list:
                    if e['priority'] == priority:
                        e['modules'].append(module)
                        updated = True
                        break
                    elif e['priority'] > priority:
                        value = { 'priority' : priority,
                                    'modules' : [ module ] }

                        module_start_list.insert(i, value)
                        updated = True
                        break

                if not updated:
                    value = { 'priority' : priority,
                                    'modules' : [ module ] }
                    module_start_list.append(value)
            except:
                try:
                    #for kill entry
                    args = re.findall(r'K([0-9]+)(\S+)', file)
                    args = args[0]
                    priority = int(args[0])
                    module = args[1]

                    #search exist in kill list
                    i = 0
                    updated = False
                    for e in module_kill_list:
                        if e['priority'] == priority:
                            e['modules'].append(module)
                            updated = True
                            break
                        elif e['priority'] > priority:
                            value = { 'priority' : priority,
                                        'modules' : [ module ] }

                            module_kill_list.insert(i, value)
                            updated = True
                            break

                    if not updated:
                        value = { 'priority' : priority,
                                        'modules' : [ module ] }
                        module_kill_list.append(value)

                except:
                    print("Bad files in " + work_dir + " directory!")
                    return -1

    return 0

def receiveSignal(signalNumber, frame):
    killAll()
    raise SystemExit(0)

def registerSignals():
    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)

def main():
    registerSignals()
    if scandir() == 0:
        launch()


if __name__ == "__main__":
    main()
