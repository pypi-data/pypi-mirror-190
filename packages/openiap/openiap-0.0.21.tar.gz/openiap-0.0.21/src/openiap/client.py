from urllib.parse import urlparse
from queue import Queue
import traceback
#import queue
import gzip
import os
import json
import sys
from datetime import datetime
# from concurrent import futures
import asyncio
import random
import time
import logging
import functools
import threading

import grpc
from proto.base_pb2_grpc import grpcServiceStub
from proto.base_pb2 import envelope
from proto import base_pb2
from proto import queues_pb2
from proto import workitems_pb2

def synchronize_async_helper(to_await):
    async_response = []

    async def run_and_capture_result():
        r = await to_await
        async_response.append(r)

    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    coroutine = run_and_capture_result()
    loop.run_until_complete(coroutine)
    return async_response[0]

class Client():
    async def ainput(self, string: str) -> str:
        await asyncio.get_event_loop().run_in_executor(
                None, lambda s=string: sys.stdout.write(s+' '))
        return await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline)
    def __init__(self, url = ""):
        self.url = url
        if(self.url == None or self.url == ""): 
            self.url = os.environ.get("apiurl", "")
            self.jwt = os.environ.get("jwt", "")
            if(self.jwt == ""):
                uri = urlparse(self.url)
                if(uri.username == None or uri.username == "" or uri.password == None or uri.password == ""):
                    raise ValueError("No jwt environment variable and no credentials in url")
        if(self.url == None or self.url == ""): self.url = "grpc://grpc.app.openiap.io:443"
        self.connected = False
        self.loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(self.loop)
        self.streams = {}
        self.pending = {}
        self.messagequeues = {}
        self.queue = Queue()
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        threading.Thread(target=self.__server_pinger, daemon=True).start()
        # self.send_queue = queue.SimpleQueue() # or Queue if using Python before 3.7
        # threading.Thread(target=self.__server_pinger, args=(queue,)).start()

        # uri = urlparse(self.url)
        # if(uri.username != None and uri.username != "" and uri.password != None and uri.password != ""):
        #     self.__login_event = threading.Event()
        #     threading.Thread(target=self.__Signin, args=(uri.username, uri.password,)).start()
        #     self.__login_event.wait(timeout=None)
    def uniqueid(self):
        self.seed = random.getrandbits(32)
        while True:
            yield self.seed
            self.seed += 1
    def __Unpack(self, message):
        if(message.command == "getelement"):
            msg = base_pb2.getelement()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "signinreply"):
            msg = base_pb2.signinreply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "registerqueuereply"):
            msg = queues_pb2.registerqueuereply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "queuemessagereply"):
            msg = queues_pb2.queuemessagereply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "queueevent"):
            msg = queues_pb2.queueevent()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "pushworkitemreply"):
            msg = workitems_pb2.pushworkitemreply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "popworkitemreply"):
            msg = workitems_pb2.popworkitemreply()
            if(message.data.value != None and message.data.value != "" and message.data.value != b""):
                msg.ParseFromString(message.data.value);
                return msg
            else:
                return None
        elif(message.command == "updateworkitemreply"):
            msg = workitems_pb2.updateworkitemreply()
            if(message.data.value != None and message.data.value != "" and message.data.value != b""):
                msg.ParseFromString(message.data.value);
                return msg
            else:
                return None                
        elif(message.command == "pong"):
            msg = base_pb2.pong()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "ping"):
            msg = base_pb2.ping()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "error"):
            msg = base_pb2.error()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "download"):
            msg = base_pb2.download()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "downloadreply"):
            msg = base_pb2.downloadreply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "stream"):
            msg = base_pb2.stream()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "beginstream"):
            msg = base_pb2.beginstream()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "endstream"):
            msg = base_pb2.endstream()
            msg.ParseFromString(message.data.value);
            return msg
        else:
            logging.error(f"Got unknown {message.command} message")
            return None
    def __connect_and_listen(self, itr):
        try:
            uri = urlparse(self.url)
            if(uri.port == 443 or uri.port == "443"):
                logging.info(f"Connecting to {uri.hostname}:{uri.port} using ssl credentials")
                credentials = grpc.ssl_channel_credentials()
                self.chan = grpc.secure_channel(f"{uri.hostname}:{uri.port}", credentials, options=(('grpc.ssl_target_name_override', uri.hostname),))
            else:
                logging.info(f"Connecting to {uri.hostname}:{uri.port}")
                self.chan = grpc.insecure_channel(f"{uri.hostname}:{uri.port}")
            fut = grpc.channel_ready_future(self.chan)
            while not fut.done():
                logging.debug("channel is not ready")
                time.sleep(1)
            self.connected = True
            logging.info(f"Connected to {uri.hostname}:{uri.port}")
            asyncio.run_coroutine_threadsafe(self.onconnected(self), self.loop)
            logging.debug(f"Create stub and connect streams")
            stub = grpcServiceStub(self.chan)
            for message in stub.SetupStream(itr):
                logging.debug(f"RCV[{message.id}][{message.rid}][{message.command}]")
                self.__parse_message(message)
        except Exception as e:
            if(self.connected == True):
                self.connected = False
                print(repr(e))
                traceback.print_tb(e.__traceback__)
            pass
        logging.debug(f"Close channels")
        for id in self.pending:
            err = ValueError("Channel closed")
            self.loop.call_soon_threadsafe(self.pending[id].set_exception, err)
        for id in self.pending:
            err = ValueError("Channel closed")
            self.loop.call_soon_threadsafe(self.pending[id].set_exception, err)
        self.chan.close()
    def Close(self):
        if(self.connected == True):
            self.connected = False
            self.chan.close()
    async def onmessage(self, client, command, rid, message):
        logging.info(f"Got {command} message event")
    async def onconnected(self, client):
        logging.info(f"Connected")
        # uri = urlparse(self.url)
        # if(uri.username != None and uri.username != "" and uri.password != None and uri.password != ""):
        #     await self.__Signin(uri.username, uri.password)
    def __parse_message(self, message:envelope):
        msg = self.__Unpack(message)
        if(message.rid in self.streams and message.command in ["beginstream", "stream", "endstream"]):
            # if(message.command == "beginstream"):
            # elif(message.command == "endstream"):
            if(message.command == "stream"):
                # self.streams[message.rid] += msg.data
                self.streams[message.rid].extend(msg.data)
        elif(message.rid in self.pending):
            if(message.command == "error"):
                #raise ValueError(msg.message)
                self.loop.call_soon_threadsafe(self.pending[message.rid].set_exception, ValueError(f"SERVER ERROR {msg.message}\n{msg.stack}" ))
            else:
                self.loop.call_soon_threadsafe(self.pending[message.rid].set_result, msg)
            self.pending.pop(message.rid, None)
        else:
            if(message.command == "queueevent" and msg.queuename in self.messagequeues):
                # asyncio.run(self.messagequeues[msg.queuename](self, msg))
                # self.loop.run_in_executor(self.messagequeues[msg.queuename](self, msg))
                # self.loop.call_soon_threadsafe(self.messagequeues[msg.queuename](self, msg))
                # print(f"recevied {message.command}")
                payload = json.loads(msg.data)
                if("payload" in payload):
                    payload = payload["payload"]
                payload = asyncio.run_coroutine_threadsafe(self.messagequeues[msg.queuename](self, msg, payload), self.loop)
                # payload = synchronize_async_helper(self.messagequeues[msg.queuename](self, msg, payload))
                # if(payload != None):
                #     reply = base_pb2.envelope(command="queuemessage")
                #     res = json.dumps(payload)
                #     reply.data.Pack(queues_pb2.queuemessage(queuename=msg.replyto, data=res, striptoken=True, correlationId=msg.correlationId))
                #     self.queue.put(reply)
                # print(f"processed {message.command}")
            elif(message.command == "ping" or message.command == "pong" or message.command == "queuemessagereply"):
                pass
                #time.sleep(1)
            else:
                # self.trigger("message", message.command, message.id, msg)
                # reply = asyncio.run(self.onmessage(self, message.command, message.id, msg))
                # reply = yield asyncio.run_coroutine_threadsafe(self.onmessage(self, message.command, message.id, msg), self.loop)
                # reply = self.loop.run_in_executor(None, self.onmessage, self, message.command, message.id, msg)
                asyncio.run_coroutine_threadsafe(self.onmessage(self, message.command, message.id, msg))
                # reply = synchronize_async_helper(self.onmessage(self, message.command, message.id, msg))
                # if(reply != None):
                #     if(reply.command != "noop"):
                #         self.Send(reply, message.id)
    def __server_pinger(self):
        count = 0
        while True:
            time.sleep(5)
            if(self.connected):
                message = envelope(command="ping")
                self.queue.put(message)
            time.sleep(25)
            count += 1
    def __request_iterator(self, connectonid):
        logging.debug(f"Waiting for message for connecton id {connectonid}")
        message = self.queue.get()
        if(connectonid != self.connectonid):
            self.queue.put(message)
            return None
        logging.debug(f"Process sending message for connecton id {connectonid}")
        if(message.id == None or message.id == ""): message.id = str(next(self.uniqueid()))
        logging.debug(f"SND[{message.id}][{message.rid}][{message.command}]")
        return(message)

    def __listen_for_messages(self):
        while True:
            self.connectonid = str(next(self.uniqueid()))
            count = 0
            logging.debug(f"Estabilish connecton id {self.connectonid}")
            self.__connect_and_listen(
                iter(functools.partial(self.__request_iterator, self.connectonid), None)
            )
            self.connected = False
            count += 1
            logging.debug(f"Reconnect number {count}")
            time.sleep(2)
    def __SetStream(self, rid):
        # self.streams[rid] = b""
        self.streams[rid] = bytearray(0)
    def __RPC(self, request, id=None):
        if(id == None): id = str(next(self.uniqueid()))
        request.id = id
        future = asyncio.Future()
        self.pending[id] = future
        self.queue.put(request)
        return future
    def Send(self, request, rid):
        if(rid == None or rid == ""): raise ValueError("RID is mandatory")
        id = str(next(self.uniqueid()))
        request.id = id
        request.rid = rid
        self.queue.put(request)
    async def Signin(self, username=None, password=None, ping=True):
        request = base_pb2.envelope(command="signin")
        if(username == None and password==None):
            jwt = os.environ.get("jwt", "")
            if jwt != "":
                username=jwt
            else:
                uri = urlparse(self.url)
                if(uri.username != None and uri.username != "" and uri.password != None and uri.password != ""):
                    username=uri.username
                    password=uri.password
        if(password== None or password == ""):
            request.data.Pack(base_pb2.signin(jwt=username, ping=ping))
        else:
            request.data.Pack(base_pb2.signin(username=username, password=password, ping=ping))
        result = await self.__RPC(request)
        self.jwt = result.jwt
        self.user = result.user
        return result.user
    async def DownloadFile(self, Id=None, Filename=None):
        request = base_pb2.envelope(command="download")
        request.data.Pack(base_pb2.download(filename=Filename,id=Id))
        rid = str(next(self.uniqueid()))
        self.__SetStream(rid)
        promise = self.__RPC(request, rid)
        result = await promise
        if(result.filename != None and result.filename != ""):
            with open(result.filename, "wb") as out_file:
                out_file.write(self.streams[rid])
        return result
    async def GetElement(self, xpath):
        request = base_pb2.envelope(command="getelement")
        request.data.Pack(base_pb2.getelement(xpath=xpath))
        result = await self.__RPC(request)
        return result.xpath
    async def RegisterQueue(self, queuename, callback):
        request = base_pb2.envelope(command="registerqueue")
        request.data.Pack(queues_pb2.registerqueue(queuename=queuename))
        result = await self.__RPC(request)
        self.messagequeues[result.queuename] = callback
        return result.queuename
    async def QueueMessage(self, queuename, payload, correlationId=None, striptoken=True):
        request = base_pb2.envelope(command="queuemessage")
        data = {payload: payload}
        request.data.Pack(queues_pb2.queuemessage(queuename=queuename, data=data, striptoken=striptoken, correlationId=correlationId))
        return self.__RPC(request)
    async def PushWorkitem(self, wiq:str, name:str, payload:dict, files: any = None, wiqid:str = None, nextrun: datetime = None, priority: int = 2, compressed: bool = False):
        request = base_pb2.envelope(command="pushworkitem")
        _files = []
        if(files != None):
            for filepath in files:
                filename = os.path.basename(filepath)
                if compressed == True:
                    with open(filepath, mode="rb") as content:
                        _files.append({"filename":filename, "compressed": compressed, "file": gzip.compress(content.read())})
                else:
                    with open(filepath, mode="rb") as content:
                        _files.append({"filename":filename, "compressed": compressed, "file": content.read()})
        q = workitems_pb2.pushworkitem(wiq=wiq,name=name, files=_files, wiqid=wiqid, nextrun=nextrun, priority=priority )
        q.payload = json.dumps(payload)
        request.data.Pack(q)
        result = await self.__RPC(request)
        return result.workitem;
    async def PopWorkitem(self, wiq:str,includefiles:bool=False,compressed:bool=False):
        request = base_pb2.envelope(command="popworkitem")
        request.data.Pack(workitems_pb2.popworkitem(wiq=wiq,includefiles=includefiles,compressed=compressed))
        result = await self.__RPC(request)
        if(result == None): return None
        return result.workitem;
    async def UpdateWorkitem(self, workitem, files: any = None, compressed:bool=False):
        request = base_pb2.envelope(command="updateworkitem")
        _files = []
        for f in workitem.files:
            workitem.files.remove(f)
        if(files != None):
            for filepath in files:
                filename = os.path.basename(filepath)
                if compressed == True:
                    with open(filepath, mode="rb") as content:
                        _files.append({"filename":filename, "compressed": compressed, "file": gzip.compress(content.read())})
                else:
                    with open(filepath, mode="rb") as content:
                        _files.append({"filename":filename, "compressed": compressed, "file": content.read()})
        uwi = workitems_pb2.updateworkitem(workitem = workitem, files = _files);
        request.data.Pack(uwi)
        result = await self.__RPC(request)
        if(result == None): return None
        return result.workitem;
