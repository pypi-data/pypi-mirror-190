#!/usr/bin/env python
# stdlib
from viztracer import VizTracer
from viztracer import get_tracer
import sys
import re
import time
import json
import asyncio
import uvloop
import functools
import concurrent.futures
import multiprocessing as mp
from pathlib import Path
from multiprocessing import Manager, Queue
from multiprocessing.managers import BaseManager
from loky import get_reusable_executor

# contrib
import click
from rich import print

# gnss libs
from networktools.environment import get_env_variable
from networktools.colorprint import gprint, bprint, rprint
from networktools.ssh import clean_port
from networktools.time import timestamp, now
from networktools.messages import MSGException, MessageLog

# tasktools loop async
from tasktools.assignator import TaskAssignator

# deprecate socket service
from gnsocket.gn_socket import GNCSocket
from gnsocket.socket_server import GNCSocketServer

# own module
from gnss_collector import Engine, deactive_server, Logger, rdbnow
from gnss_collector.scripts import EnvData

# desde la misma carpeta
# fn que maneja excepción en socket


def socket_exception(ex, gs, idc):
    bprint("Excepción en socket")
    bprint(gs)
    rprint("Id socket client -> %s" % idc)
    raise ex


def get_conf_data(conf):
    keys_ = {'cll_group', 'est_by_proc', 'tsleep', 'workers',
             'gsof_timeout', 'rdb_host', 'rdb_port', 'cll_status',
             'socket_ip', 'socket_port', 'log_path', 'dbdata', 'server_name'}
    keys = set(map(str.upper, keys_))
    json_file = re.compile("\.json$")
    dbdata = {}
    if json_file.search(conf):
        file_path = Path(conf)
        if file_path.exists():
            with open(file_path, 'r') as f:
                dbdata = json.load(f)
            if all(filter(lambda k: k in dbdata, keys)):
                return dbdata
            else:
                print("A tu archivo le falta una llave, revisa si tiene %s" % keys)
        else:
            print("Tu archivo json no existe en la ruta especificada: %s" % file_path)
            print("Debe ser así:")
            this_path = Path(__file__).parent
            example_path = this_path/"collector_example.json"
            if example_path.exists():
                with open(example_path, 'r') as f:
                    print("{")
                    [print(k, ":", v) for k, v in json.load(f).items()]
                    print("}")
            else:
                print(
                    "El archivo de ejemplo no existe, lo siento, escribe a dpineda@uchile.cl consultando")
    else:
        print("Tu archivo json debe tener una extensión json y una ruta correcta: pusiste  <%s>" % conf)
        print("Archivo json debe ser así:")
        this_path = Path(__file__).parent
        example_path = this_path/"collector_example.json"
        if example_path.exists():
            with open(example_path, 'r') as f:
                print("{")
                [print("    %s:\"%s\"," % (k, v))
                 for k, v in json.load(f).items()]
                print("}")
        else:
            print(
                "El archivo de ejemplo no existe, lo siento, escribe a dpineda@uchile.cl consultando")
    return dbdata


def start_collector(env, conf="collector_example.json"):
    exc = MSGException()
    new_loop = uvloop.new_event_loop()
    asyncio.set_event_loop(new_loop)
    mp.set_start_method('spawn')
    data = {}
    if env:
        env_data = EnvData()
        data = env_data.json
        print("Data", data)
        clean_port(env_data.COLLECTOR_SOCKET_PORT)
    else:
        data = get_conf_data(conf)
        clean_port(data.get("COLLECTOR_SOCKET_PORT"))
    workers = data.get("COLLECTOR_WORKERS")
    address = [data.get(k)
               for k in ("COLLECTOR_SOCKET_IP", "COLLECTOR_SOCKET_PORT")]
    server_name = data.get("SERVER_NAME")
    print("Workers", workers)
    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
        # with get_reusable_executor(max_workers=workers) as executor:
        loop = asyncio.get_event_loop()
        manager = Manager()
        # terminal->network
        queue_process = manager.Queue()
        # terminal->network
        queue_ans_process = manager.Queue()
        # terminal->network
        # Manager dict to share betwen process
        stations = manager.dict()
        wait = manager.dict()
        dbtype = manager.dict()
        protocol = manager.dict()
        protocols = manager.dict()
        dbtypes = manager.dict()
        status_sta = manager.dict()
        instances = manager.dict()
        db_instances_sta = manager.dict()
        status_conn = manager.dict()
        db_data = manager.dict()
        db_instances = manager.dict()
        dump_list = manager.dict()
        tasks = manager.dict()
        proc_tasks = manager.dict()
        sta_init = manager.dict()
        db_init = manager.dict()
        db_connect = manager.dict()
        assigned_tasks = manager.dict()
        inc_msg = manager.dict()
        status_tasks = manager.dict()
        free_ids = manager.dict()
        changes = manager.dict()  # check for changes, change control
        # value
        sleep_time = 1
        ids = manager.list()
        idd = manager.list()
        ipt = manager.list()
        idm = manager.list()
        ico = manager.list()
        idc = manager.dict()
        ##
        locker = manager.Lock()
        # create scheduler subclass
        queue_n2t = manager.Queue()
        # network->terminal
        queue_t2n = manager.Queue()
        queue_log = manager.Queue()
        queue_db = manager.Queue()
        args = []
        kwargs = {
            "server": data.get("server_name".upper()),
            "log_path": data.get("log_path".upper()),
            'dt_criteria': 4,
            "timeout": 15,
            "raise_timeout": False,
            'dbdata': data.get("dbdata".upper())
        }
        queue_list = [queue_n2t,
                      queue_t2n,
                      queue_process,
                      queue_ans_process,
                      queue_db,
                      queue_log]
        print("Pre engine kwargs", kwargs)
        engine = Engine(
            queue_list,
            sleep_time,
            data.get("est_by_proc".upper()),
            stations,
            dbtype,
            protocol,
            status_sta,
            db_instances_sta,
            status_conn,
            db_data,
            dump_list,
            proc_tasks,
            assigned_tasks,
            free_ids,
            wait,
            inc_msg,
            ids,
            idd,
            ipt,
            idm,
            ico,
            changes,
            data.get("gsof_timeout".upper()),
            sta_init,
            db_init,
            db_connect,
            status_tasks,
            data.get("nproc".upper()),
            idc,
            data.get("rdb_address".upper()),
            8,
            args,
            kwargs
        )
        NIPT = workers-2
        gprint(f"Number of process {NIPT}")
        # activate new assignator
        cll_status = data.get("cll_status".upper())
        cll_group = data.get("cll_group".upper())
        assignator = TaskAssignator(
            engine,
            queue_process,
            queue_ans_process,
            assigned_tasks,
            cll_status,
            cll_group,
            locker)
        message = f"Assignator created"

        queue_log.put({"run_collector": [MessageLog(
            rdbnow(), "run_collector", message, Logger.INFO, exc).rdb]})

        try:
            print("Obteniendo lista inicial de estaciones")
            engine.load_stations()
            engine.load_databases()
        except Exception as e:
            print("Falla en cargar datos desde db %s" % e)
            raise e
        tasks = []

        #################
        #  Here there are in use 2 process
        ###################

        print("Está corriendo loop?", loop.is_running())

        try:
            # this includes log tasks
            loop.run_in_executor(
                executor,
                engine.msg_network_task
            )
            message = f"Msg network task running at one process"

            queue_log.put(
                {
                    "run_collector": [
                        MessageLog(rdbnow(), "run_collector", message,
                                   Logger.INFO, exc).rdb
                    ]
                }
            )
            print("Está corriendo loop on msg networktask?", loop.is_running())
        except Exception as ex:
            print("Falla encargar networktask")
            raise ex

        print("Log path", data.get("LOG_PATH"))
        socket_path = str(
            Path(data.get("LOG_PATH", "gus_log"))/"gnsocket_server")
        print("Socket path", socket_path, type(socket_path))

        opts = {
            "timeout": 10,
            "raise_timeout": False,
            'server': server_name,
        }

        print("Socket opts", opts)
        opts["log_path"] = socket_path
        print("Iniciando socket server", address)
        # server_socket = GNCSocketServer(
        #     queue_n2t, queue_t2n, address=address,
        #     callback_exception=socket_exception, **opts)
        # try:
        #     loop.run_in_executor(
        #         executor,
        #         server_socket.socket_task
        #     )
        # except Exception as ex:
        #     print("Falla en cargar socket task")
        #     raise ex

        ######

        ######

        SK = list(engine.stations.keys())
        tasks = []
        LSK = len(SK)

        # Inicializa Assignator

        loop.run_in_executor(executor, assignator.new_process_task)
        # run specific process for DATABASE SAVING

        loop.run_in_executor(executor, engine.db_task)

        ####
        # Here we use the another (the rest) of the processors
        ####
        # NIPT = 1 # for test
        print(now(), "run_collector",
              f"Asignando tareas 'manage_tasks' -> {NIPT}")
        main_tasks = []
        for i in range(NIPT):
            try:
                # time.sleep(tsleep)
                ipt = engine.set_ipt(ipt=f"IPT_{i}")  # engine.set_ipt()
                # se inicializa lista de proc_task
                engine.proc_tasks[ipt] = []
                try:
                    tipt = loop.run_in_executor(
                        executor,
                        functools.partial(
                            engine.manage_tasks,
                            ipt))
                    message = f"Creation of process {ipt} for manage" +\
                        f"tasks, Task {i}/{NIPT} -> {ipt}"
                    main_tasks.append(tipt)

                    print("STARTIN PROCESS TASK::", message)
                    queue_log.put(
                        {"run_collector": [
                            MessageLog(
                                rdbnow(),
                                "run_collector",
                                message,
                                Logger.INFO,
                                exc).rdb
                        ]
                        }
                    )
                    gprint(f"ID {i}/{NIPT} ipt-> {tipt}")
                except Exception as exc:
                    print("Error al activar nueva cpu")
                    print(exc)
                    raise exc
            except Exception as exc:
                print("Error al cargar en executor %s erro: $s" % (ipt, exc))
                raise exc
        try:
            loop.run_until_complete(asyncio,gather(*main_tasks))
        except Exception as exc:
            deactive_server(server_name)
            engine.exception("Detener log")
            print("Error al inicializar loop, error: $s" % (exc))
            raise exc

        print("Done")


@click.command()
@click.option("--name",
              default="collector",
              show_default=True,
              help="Nombre de la instancia collector a crear")
@click.option("--env_vars/--no-env_vars",
              default=True,
              show_default=True,
              type=bool,
              help="Para mostrar el nombre de las variables de ambiente")
@click.option("--env/--no-env",
              default=True,
              show_default=True,
              type=bool,
              required=True,
              help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--conf",
              default="JSON FILE",
              show_default=True,
              help="Archivo json con los parámetros de database, debe contener las llaves {dbuser, dbpass, dbname, dbhost, dbport}")
@click.option("--profile/--no-profile",
              default=False,
              show_default=True,
              type=bool,
              required=False,
              help="Generar tracing profile para debug")
def run_collector(name, env_vars, env, conf, profile):
    print(f"Iniciando servicio COLLECTOR para {name.upper()}")
    if env and env_vars:
        envvar = EnvData()
        envvar.show()

    if profile:
        tracing_file = Path.home() / "profile.json"
        tracer_entries = 1000000
        with VizTracer(
                output_file=str(tracing_file),
                tracer_entries=10_000_000,
                log_async=True,
                **get_tracer().init_kwargs) as tracer:
            start_collector(env, conf)
    else:
        start_collector(env, conf)


if __name__ == "__main__":
    run_collector()
