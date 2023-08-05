#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from dataclasses import dataclass
from gnss_collector.engine.steps import ORMSteps, Logger
from tasktools.taskloop import TaskLoop
import httpx
import json
import os
import sys
from typing import List, Dict, Union, overload, Any, Tuple
from networktools.messages import MSGException, MessageLog
from rich import print
from data_rdb import Rethink_DBS
from rethinkdb import RethinkDB
from networktools.time import timestamp, now
from networktools.library import my_random_string

ORM_URL = os.getenv("ORM_SERVICE_HOST",'http://10.54.217.99:8888')
SLEEP = 0.0001

rdb = RethinkDB()

def rdbnow():
    return rdb.iso8601(now().isoformat())

def load_stations(url):
    u = httpx.get(f"{url}/stations")
    print("URL para obtener estaciones",u)
    while u.status_code != httpx.codes.OK:
        u = httpx.get(f"{url}/stations")
    return json.loads(u.content)

@dataclass
class TestStations:
    changes:Dict[str, bool]
    stations:Dict[str, Dict[str,Any]]
    assigned_tasks: Dict[str,str]
    status_tasks:Dict[str, Dict[str,str]]
    ids:List[str]
    uin:int=4

    def manage_db_loop(self, queue_log):
        args = [ORMSteps.DISTRIBUTE, queue_log]
        task_name = "db_loop_task"
        task = TaskLoop(self.db_loop, args, {}, name=task_name)
        task.create()
        self.status_tasks["db_loop"] = task_name
        

    def load_stations(self):
        u = load_stations(ORM_URL)  # ok
        for m in u:
            keys = ['id', 'code', 'db', 'dblist', 'ecef_x', 'ecef_y', 'protocol_host',
                    'ecef_z', 'port', 'protocol', 'host', 'dbname',"dbdata"]
            try:
                station = dict(
                    id=m['id'],
                    code=m['code'],
                    name=m['name'],
                    port=m["port"],
                    ecef_x=m["position"]['ecef']["x"],
                    ecef_y=m["position"]['ecef']['y'],
                    ecef_z=m["position"]['ecef']['z'],
                    protocol=m['protocol'],
                    protocol_host=m['protocol_host'],
                    position=m["position"],
                    dbdata=m["dbdata"],
                    on_db=True
                )
                (ids, sta) = self.add_station(**station)
                # print(station)
            except Exception as exc:
                raise exc

    def set_id(self, lista):
        """
        Defines a new id for stations, check if exists
        """
        while (ids := my_random_string(self.uin)) not in lista:
            lista.append(ids)
            break
        return ids

    def set_ids(self):
        """
        Defines a new id for stations, check if exists
        """
        return self.set_id(self.ids)

    def add_station(self, **sta):
        """
        Add station to list for data adquisition
        """
        print("ADD STATION", sta["code"])
        try:
            keys = ['id',
                    'code',
                    'name',
                    'ecef_x',
                    'ecef_y',
                    'ecef_z',
                    'host',
                    'port',
                    'interface_port',
                    'db',
                    'dblist',
                    'protocol',
                    'protocol_host',
                    'on_db',
                    'position',
                    "dbdata",
                    'ipt']

            ids = self.set_ids()

            # if ids in self.enqueued:
            #     self.enqueued.remove(ids)
            # self.enqueued.add(ids)

            station = dict(ids=ids)

            for k in keys:
                if k in sta.keys():
                    if k == 'protocol':
                        station[k] = sta.get(k, 'None').upper()
                    else:
                        station[k] = sta.get(k, None)
                else:
                    if k == 'host':
                        station[k] = 'localhost'
                    elif k == 'port' or k == 'interface_port':
                        station[k] = 0
                    elif k in  [f'ecef_{v}' for v in ("x", "y", "z")]:
                        station[k] = 0
                    else:
                        station[k] = None
            self.stations.update({station["code"]: station})
            return (ids, sta)
        except Exception as ex:
            raise ex

    def update_station(self, ids, mode="UPDATE", **station):
        print(f"{ids} |Actualizando -> {mode}", station)
        code = station["code"]
        self.stations[code].update(**station)
        return station
        

    async def db_loop(
            self, 
            control:ORMSteps, 
            queue_log: asyncio.Queue, 
            *args,
            **kwargs
    ) -> Tuple[
        Tuple[ORMSteps, asyncio.Queue], 
        Dict[str, Any]
    ]:
        """
        Control for new stations or update conection credentials
        """
        messages = []
        keys = ['id', 'code', 'db', 'dblist', 'ecef_x', 'ecef_y', 'protocol_host',
                'ecef_z', 'port', 'protocol', 'host', 'dbname',"dbdata"]
        exc = MSGException()
        coroname = 'db_loop'
        if control == ORMSteps.DISTRIBUTE:
            control = ORMSteps.EXECUTE
        if control == ORMSteps.EXECUTE:
            """
            Needs:
            - list of stations
            - assignation of stations 
            - check for new stations
            - drop if not listed in new list of databases
            """
            # Obtener las estaciones
            ids_stations = {station.get("code"):ids for ids, station in self.stations.items()}
            base_stations = [station for station in self.stations.values()]
            codes = [station.get("code") for station in base_stations]
            set_codes = set(codes)
            address = {
                station.get("code"):(station.get("host"),station.get("port")) 
                for station in base_stations
            }
            # obtain all ids assigned
            # assigned_tasks  = set()      # 
            # if self.assigned_tasks:
            #     assigned_tasks = reduce(
            #         lambda a,b: a|b, 
            #         [set(ids_set.values()) for ipt, ids_set in
            #          self.assigned_tasks.items()])
            # assigned_ids = set(filter(lambda e:e,[self.stations.get(ids, {}).get("code") for
            #                 ids in assigned_tasks]))


            try:
                stations = load_stations(ORM_URL)

            except Exception as e:
                print("Error al obtener lista", e, control)
                raise e
            try:
                new_codes = set()
                print("Stations", len(self.stations))
                for m in stations:
                    station = dict(**m, on_db=True)
                    code = station["code"]
                    new_codes.add(code)
                    if code not in self.stations:
                        """
                        add new station to list, and send by queue to assignator
                        """
                        ids, station = self.add_station(**station)
                        message = f"New station added to collector {station}"
                        level = Logger.INFO
                        messages.append(MessageLog(rdbnow(),coroname,
                                                   level, message,
                                                   exc))
                        #self.queue_process.put(ids)
                        #print("self.queue", self.queue_process)
                        self.changes[ids] = True
                    else:
                        """
                        if there is in codes, but check address data
                        is the important information for this use case
                        """
                        base_address = address.get(code)
                        if base_address:
                            now_address = (station["host"],
                                           station["port"])
                            ids = ids_stations.get(code)
                            if now_address != base_address:
                                print("Check address", code, base_address)

                                """
                                If new info is correct, the connection
                                will raise and check for new info
                                (check control)
                                """

                                print(f"Cambiando direccion a {code} -> {now_address}")
                                station = self.update_station(ids, **station)
                                self.changes[ids] = True

                # drop deactivated codes
                dropped = set_codes - new_codes
                ids_drop = [ids_stations.get(code) for code in
                            dropped]
                for ids in ids_drop:
                    self.changes[ids] = True
                    if ids in self.stations:
                        station = self.stations.get(ids)
                        del self.stations[ids]
                        for ipt, task_set in self.assigned_tasks.items():
                            if ids in task_set.values():
                                for ico, nids in task_set.items():
                                    if ids == nids:
                                        message = f"Station {station} with ids {ids},"+\
                                            "ico {ico}, ipt {ipt}  dropped"
                                        level = Logger.INFO
                                        messages.append(MessageLog(rdbnow(), coroname, level, message, exc))
                                        
                                        self.unset_sta_assigned(ipt,
                                                                ico, 
                                                                ids)
            except Exception as e:
                exc = MSGException(*sys.exc_info())                
                message = f"At db_loop the session is disconnected"
                level = Logger.ERROR
                messages.append(MessageLog(rdbnow(),coroname, level, message, exc))
                control = ORMSteps.DISTRIBUTE

        if messages:
            for msg in messages:
                await queue_log.put(("db_loop", msg.rdb))                

        await asyncio.sleep(15)
        return (control, queue_log), kwargs


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    queue_log = asyncio.Queue()
    changes = {}
    stations = {}
    assigned_tasks = {}
    status_tasks = {}
    ids = []
    test = TestStations(changes, stations, assigned_tasks,
                        status_tasks, ids)
    test.manage_db_loop(queue_log)
    try:
        loop.run_forever()
    except Exception as exc:
        deactive_server(server_name)
        engine.exception("Detener log")
        print("Error al inicializar loop, error: $s" % (exc))
        raise exc
