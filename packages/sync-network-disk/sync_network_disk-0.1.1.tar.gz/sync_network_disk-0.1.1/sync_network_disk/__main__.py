from __future__ import annotations
import io
import time
import json
import uuid
import http
import sched
import flask
import qrcode
import typing
import pathlib
import argparse
import watchdog
import threading
import dataclasses
import configloaders
import watchdog.events
import watchdog.observers

from .__aligo import Aligo
from .__log import logger as log
from . import __config as config
from .__proxy_aligo import ProxyAligo, AligoIsNone

app = flask.Flask(__name__)
ali = ProxyAligo()
sync_handlers: dict[str, SyncHandler] = {}

class SyncHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, local_folder: str, remote_folder: str) -> None:
        super().__init__()
        self.local_folder = local_folder
        self.remote_folder = ali.get_folder_by_path(remote_folder, create_folder=False)
        if self.remote_folder is None and config.create_folder_if_remote_exist:
            self.remote_folder = ali.get_folder_by_path(remote_folder, create_folder=True)
        self.cooling = False
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.enable = False
        self.bound_event = None
    def end_cooling(self):
        self.cooling = False
        log.info('end cooling')
    def on_deleted(self, event: watchdog.events.FileDeletedEvent):
        path = pathlib.Path(event.src_path)
        file = ali.get_folder_by_path(path.as_posix(), create_folder=False) or ali.get_file_by_path(path.as_posix())
        if file is not None: ali.delete_file(file.file_id)
    def on_moved(self, event: watchdog.events.FileMovedEvent):
        self.on_deleted(event)
        self.on_any_event(watchdog.events.FileCreatedEvent(event.dest_path))
    def sync(self):
        self.cooling = True
        ali.sync_folder(self.local_folder, self.remote_folder.file_id)
        log.info('cooling...')
        self.scheduler.enter(config.cooldown_time, 1, self.end_cooling)
        threading.Thread(target=self.scheduler.run, daemon=True).start()
    def on_any_event(self, event):
        log.info(event)
        if not self.cooling and not isinstance(event, watchdog.events.FileDeletedEvent) and not isinstance(event, watchdog.events.FileMovedEvent):
            self.sync()

def observe(path: str, target: str):
    handler = SyncHandler(path, target)
    observe_handler(handler)

def observe_handler(handler: SyncHandler, event: threading.Event=None, callback: typing.Callable=None, args: list=None):
    observer = watchdog.observers.Observer()
    observer.schedule(handler, handler.local_folder, recursive=True)
    observer.start()
    if event is None:
        event = threading.Event()
    def run():
        while not event.is_set():
            handler.sync()
            time.sleep(config.sync_interval)
    threading.Thread(target=run, daemon=True).start()
    try:
        while not event.is_set() if event else True:
            time.sleep(1)
    except: pass
    observer.stop()
    observer.join()
    event.set()
    if callback is not None:
        callback(*args)

@app.errorhandler(AligoIsNone)
def exception(e):
    return flask.Response(status=http.HTTPStatus.FORBIDDEN)

@app.route('/qrcode/s', methods=['GET'])
def get_qrcode_s() -> str:
    r = ""
    def get_qrcode():
        nonlocal r
        def show(qrcode: str):
            nonlocal r
            r = qrcode
        ali << Aligo(show=show, login_timeout=config.login_timeout)
        r = None
    threading.Thread(target=get_qrcode, daemon=True).start()
    while r == "": pass
    return r

@app.route('/handler', methods=['POST'])
def add_handler():
    local_folder = flask.request.json['local_folder']
    remote_folder = flask.request.json['remote_folder']
    sync_handlers[uuid.uuid4().hex] = SyncHandler(local_folder, remote_folder)
    return flask.Response(status=http.HTTPStatus.OK)

@app.route('/handler', methods=['DELETE'])
def del_handler():
    uid = flask.request.args['uuid']
    if uid in sync_handlers: del sync_handlers[uid]
    return flask.Response(status=http.HTTPStatus.OK)

@app.route('/handler', methods=['PUT'])
def mod_handler():
    uid = flask.request.json['uuid']
    local_folder = flask.request.json['local_folder']
    remote_folder = flask.request.json['remote_folder']
    if uid in sync_handlers:
        sync_handlers[uid] = SyncHandler(local_folder, remote_folder)
    return flask.Response(status=http.HTTPStatus.OK)

@app.route('/handler', methods=['GET'])
def get_handler():
    uid = flask.request.args['uuid']
    if uid in sync_handlers:
        v = sync_handlers[uid]
        return json.dumps({
            'local_folder': v.local_folder, 
            'remote_folder': v.remote_folder.name,
        })
    return flask.Response(status=http.HTTPStatus.NO_CONTENT)

@app.route('/handlers', methods=['GET'])
def get_handlers():
    return json.dumps({k:{
        'local_folder': v.local_folder, 
        'remote_folder': v.remote_folder.name,
    } for k,v in sync_handlers.items()})

@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    s = get_qrcode_s()
    img = qrcode.make(s)
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/jpeg')

@app.route('/user_info', methods=['GET'])
def get_user_info():
    s = get_qrcode_s()
    if s is None:
        return json.dumps(dataclasses.asdict(ali.get_user()))
    else:
        return flask.Response(status=http.HTTPStatus.FORBIDDEN)

@app.route('/handler/<uid>/status', methods=['GET'])
def get_handler_status(uid: str):
    if uid in sync_handlers:
        return json.dumps({
            "enable": sync_handlers[uid].enable
        })
    return flask.Response(status=http.HTTPStatus.NO_CONTENT)

def set_handler_status(handler: SyncHandler, enable: bool):
    if enable is True and handler.enable is False:
        event = threading.Event()
        handler.bound_event = event
        threading.Thread(target=observe_handler, args=(handler, event, set_handler_status, (handler, False)), daemon=True).start()
        handler.enable = True
    elif enable is False and handler.enable is True:
        handler.bound_event.set()
        handler.bound_event = None
        handler.enable = False

@app.route('/handler/<uid>/status', methods=['PUT'])
def mod_handler_status(uid: str):
    enable = flask.request.json['enable']
    if uid in sync_handlers:
        handler = sync_handlers[uid]
        set_handler_status(handler, enable)
    return flask.Response(status=http.HTTPStatus.OK)

def main():
    server_parser = argparse.ArgumentParser(add_help=False)
    server_parser.add_argument('--server', action='store_true')
    configloaders.load_argparse(config.__dict__, server_parser)
    args, _ = server_parser.parse_known_args()
    if args.server:
        app.run(config.host, config.port)
    else:
        parser = argparse.ArgumentParser(parents=[server_parser])
        parser.add_argument('local', type=str, help='Example: ./path')
        parser.add_argument('remote', type=str, help='Example: path')
        args = parser.parse_args()
        ali << Aligo(level=config.log_level)
        observe(args.local, args.remote)

if __name__ == '__main__':
    main()