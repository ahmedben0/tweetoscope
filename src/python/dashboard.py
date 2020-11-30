from kafka import KafkaConsumer
from utils import *
import configparser
import sys
import time 
from os import system, name 
from tabulate import tabulate

def clear(): 
    ### source : https://www.geeksforgeeks.org/clear-screen-python/
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')


def dict_to_str(d) :
    if "type" in d.keys() :
        if d["type"] == "alert" :
            s = ""
            if "T_obs" in d.keys() :
                s += f'T_obs : {d["T_obs"]} | '
            if "cid" in d.keys() : 
                s += f'cid : {d["cid"]} - '
            if "msg" in d.keys() :
                s += f'msg : {d["msg"]} - '
            if "n_tot" in d.keys() :
                s += f'n_tot : {d["n_tot"]}'
            return s

    return str(d)


class DynamicPrintDashboard:
    def __init__(self, consumerProperties, K_hottest = 20, topic = "alert") :
        self.consumer = KafkaConsumer(**consumerProperties)
        self.consumer.subscribe(topic)
        self.hottestTweets = []
        self.K = max(K_hottest,1) ## 0 is not allowed

    def display(self) :
        clear()
        l = []
        h = []
        for _, m in enumerate(self.hottestTweets) :
            l.append(list(m.values())[1:])
            if not h :
                h = list(m.keys())[1:]
        print(tabulate(l, headers=h, tablefmt='fancy_grid'))

    def addToList(self, new_msg) :
        self.hottestTweets.append(new_msg)
        ## tweets with the highest predicted popularities !
        self.hottestTweets = sorted(self.hottestTweets, key = lambda msg: msg["n_tot"], reverse=True)

        if len(self.hottestTweets) > self.K :
            self.hottestTweets = self.hottestTweets[:self.K]


    def run(self) :
        for message in self.consumer:
            _, new_msg = msg_deserializer(message)
            self.addToList(new_msg)
            self.display()



## read config file
config = configparser.ConfigParser(strict=False)
## the script is executed from the folder "src"
config.read('./configs/collector.ini')


consumerProperties = { "bootstrap_servers":[config["kafka"]["brokers"]],
                       "auto_offset_reset":"earliest",
                       "group_id":"myOwnPrivatePythonGroup"}


dashboard = DynamicPrintDashboard(consumerProperties)
dashboard.run()