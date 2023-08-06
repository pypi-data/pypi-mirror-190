import logging
# import multiprocessing as mp
# import os
# import os.path as osp
# import signal
import argparse
import threading
import time
import queue
from typing import List, Optional, Dict, Union

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from serial import Serial

from arizon_usb_apiserver import Config as SensorConfig
from arizon_usb_apiserver import Sensor

app = FastAPI()

LOGGER: Optional[logging.Logger] = None
CONFIG: Optional[SensorConfig] = None
FORCE_DATA_QUEUE: Optional[queue.Queue] = None
START_EVENT: Optional[threading.Event] = None


def make_response(status_code, **kwargs):
    data = {'code': status_code, 'timestamp': time.time()}
    data.update(**kwargs)
    json_compatible_data = jsonable_encoder(data)
    resp = JSONResponse(content=json_compatible_data, status_code=status_code)
    return resp


@app.get("/")
def root():
    return RedirectResponse(url='/docs')


@app.get("/v1/arizon/status")
def get_status():
    if START_EVENT.is_set():
        return make_response(200, message="Force data collection is running", status=True)
    else:
        return make_response(200, message="Force data collection is stopped", status=False)


@app.get("/v1/arizon/force")
def get_force():
    res = []
    for _ in range(FORCE_DATA_QUEUE.qsize()):
        if not FORCE_DATA_QUEUE.empty():
            res.append(FORCE_DATA_QUEUE.get())
    return make_response(200, data=res)


@app.delete("/v1/arizon/force")
def clean_cached_force():
    global FORCE_DATA_QUEUE
    for _ in range(FORCE_DATA_QUEUE.qsize()):
        if not FORCE_DATA_QUEUE.empty():
            FORCE_DATA_QUEUE.get(block=False)
    return make_response(200, message="Force data queue cleaned")


@app.put("/v1/arizon/force")
def toggle_force(flag: bool):
    global START_EVENT
    if flag:
        START_EVENT.set()
    else:
        START_EVENT.clear()
    return make_response(200, message="Force data collection {}".format("started" if flag else "stopped"), status=flag)


def update_arizon_sensor_thread():
    global CONFIG, LOGGER, FORCE_DATA_QUEUE, START_EVENT

    while True:
        START_EVENT.wait()

        conn = Serial("COM2", 115200)
        sensor = Sensor(conn)
        sensor.reset()
        while True:
            data = sensor.read_once()
            if data is None:
                continue
            while FORCE_DATA_QUEUE.full():
                FORCE_DATA_QUEUE.get(block=False)
            FORCE_DATA_QUEUE.put(
                {
                    "addr": data[0],
                    "f": data[1],
                    "ts": time.time()
                },
                block=False
            )
            if not START_EVENT.is_set():
                conn.close()
                break


def portal(cfg: SensorConfig):
    # Recording parameters
    global CONFIG, LOGGER, FORCE_DATA_QUEUE, START_EVENT

    FORCE_DATA_QUEUE = queue.Queue(maxsize=1024)
    CONFIG = cfg
    START_EVENT = threading.Event()

    # setting global parameters
    logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger("arizon.portal")
    # Prepare system
    LOGGER.info(f"arizon sensor service listen at {cfg.api_port}")
    LOGGER.info(f"arizon sensor config {cfg}")
    # Start threads
    threading.Thread(target=update_arizon_sensor_thread, daemon=True).start()

    try:
        # app.run(host='0.0.0.0', port=api_port)
        uvicorn.run(app=app, port=cfg.api_port)
    except KeyboardInterrupt:
        LOGGER.info(f"portal() got KeyboardInterrupt")
        return

def main(args):
    portal(SensorConfig(args.config))

def entry_point(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./arizon_config.yaml")
    run_args = parser.parse_args(argv[1:])
    main(run_args)

if __name__ == '__main__':
    import sys
    entry_point(sys.argv)
