import os, sys, re
import json
import traceback
import asyncio
import logging
import zlib
import openiap
from google.protobuf import any_pb2 
from proto import base_pb2_grpc, base_pb2, queues_pb2
from google.protobuf import json_format

async def onmessage(client, command, rid, message):
    reply = base_pb2.envelope(command=command)
    reply.rid = rid
    try:
        if(command == "getelement"):
            logging.info(f"Server sent getelement {message.xpath}")
            reply.data.Pack(base_pb2.getelement(xpath=f"Did you say {message.xpath} ?"))
        elif(command == "queueevent"):
            data = json.loads(message.data);
        elif(command == "error"):
            reply.command = "noop"
            logging.error(f"{str(message.message)}")
        else:
            reply.command = "error"
            reply.data.Pack(base_pb2.error(message=f"Unknown command {command}"))
            logging.error(f"Got message with unknown command {command}")
    except Exception as e:
        print("runit EXCEPTION!!!!")
        print(repr(e))
        traceback.print_tb(e.__traceback__)
    return reply
async def findme333(client, message, payload):
    data = json.loads(message.data);
    logging.info(f"findme333: {str(data['name'])}")
async def findme222(client, message, payload):
    data = json.loads(message.data);
    try:
        logging.info(f"findme222: {str(data['name'])}")
    except:
        logging.info(f"findme222: {str(data['payload']['name'])}")
        pass
async def pyqueue(client, message, payload):
    print("pyqueue triggered, PopWorkitem")
    # workitem = asyncio.run(self.c.PopWorkitem("pyqueue", True, True))
    workitem = await client.PopWorkitem("pyqueue", True, True)
    print("pyqueue PopWorkitem completed")
    workitem.state = "successful"
    workitem = await client.UpdateWorkitem(workitem)

    try:
        logging.info(f"findme222: {str(payload['name'])}")
    except:
        logging.info(f"findme222: {str(payload['payload']['name'])}")
        pass
async def getnoun(client, msg, payload):
    if("text" in payload):
        text = payload["text"]
    logging.info(f"getnoun: {str(msg.correlationId)} {str(text)}")
    payload["nouns"] = "yes, no"

    if(msg.replyto != "" and msg.replyto != None):
        reply = base_pb2.envelope(command="queuemessage")
        res = json.dumps(payload)
        reply.data.Pack(queues_pb2.queuemessage(queuename=msg.replyto, data=res, striptoken=True, correlationId=msg.correlationId))
        client.queue.put(reply)
    # return payload
async def onconnected(client):
    try:
        user = await client.Signin()
        logging.info(f"Signed in as {user.name}")
        q = await client.RegisterQueue("findme333", findme333)
        logging.info(f"Registered queue {q}")
        q = await client.RegisterQueue("findme222", findme222)
        logging.info(f"Registered queue {q}")
        q = await client.RegisterQueue("pyqueue", pyqueue)
        logging.info(f"Registered queue {q}")
        q = await client.RegisterQueue("getnoun", getnoun)
        logging.info(f"Registered queue {q}")
        
    except (Exception,BaseException) as e:
        print("onconnected!!!!")
        print(repr(e))
        traceback.print_tb(e.__traceback__)
        pass
async def main():
    loglevel = os.environ.get("loglevel", logging.INFO)
    if loglevel==logging.INFO:
        logging.basicConfig(format="%(message)s", level=loglevel)
    else:
        logging.basicConfig(format="%(levelname)s:%(message)s", level=loglevel)
    # c = client.Client("grpc://testuser:testuser@localhost:50051")
    apiurl = os.environ.get("apiurl", "")
    if(apiurl == ""):
        sys.exit(f"apiurl missing")
    c = openiap.Client(apiurl)
    c.onmessage = onmessage
    c.onconnected = onconnected

    while True:
        #try:
            # text = input("COMMAND: ")
            text = await c.ainput("COMMAND: ")
            text = re.sub(r'[^a-zA-Z0-9]', '', text)
            print(f"PROCESSING {text}")
            if text == "f":
                # filename = "/home/allan/Pictures/allan.png"
                id = "63d66fe01465b11939cd0d2d"
                name = "download.png";
                await c.DownloadFile(Id=id)
            elif text == "p":
                workitem = {"name": "Allan", "test":"Hi mom", "age":23, "files": []}
                filepath = "/home/allan/Pictures/allan.png"
                result = await c.PushWorkitem("q2", "find me", workitem, [filepath], compressed=True)
                logging.info(f"Workitem pushed with id {result._id}")

                workitem = await c.PopWorkitem("q2", True, True)
                if(workitem == None):
                    logging.info("No more workitems in queue q2")                    
                else:
                    try:
                        for f in workitem.files:
                            if f.compressed:
                                with open("download.png", "wb") as out_file:
                                    out_file.write(zlib.decompress(f.file))
                            else:
                                with open("download.png", "wb") as out_file:
                                    out_file.write(f.file)
                        logging.info(f"Popped workitem id {workitem._id}")
                        workitem.state = "successful"
                        payload = json.loads(workitem.payload)
                        logging.info(f"payload name {payload.get('name','unnamed')} workitem name {workitem.name}")
                        payload["name"] = "Allan 2222"
                        workitem.payload = json.dumps(payload)
                        workitem = await c.UpdateWorkitem(workitem, ["download.png"], True)
                        logging.info(f"Popped workitem id {workitem._id} now in state {workitem.state}")
                    except (Exception,BaseException) as e:
                         workitem.state = "retry"
                         workitem.errortype = "business" # business / application
                         workitem.errormessage = "".join(traceback.format_exception_only(type(e), e)).strip()
                         workitem.errorsource = "".join(traceback.format_exception(e))
                         await c.UpdateWorkitem(workitem)
                         print("Workitem EXCEPTION!!!!")
                         print(repr(e))
                         traceback.print_tb(e.__traceback__)
                         pass
            elif text == "s":
                signin = await c.Signin()
                logging.info(f"Signed in as {signin.name}")
            elif text == "q":
                await c.QueueMessage("findme222", '{"name":"py find me"}')
            elif text == "pp":
                filepath = "/home/allan/Pictures/allan.png"
                for i in range(1, 5):
                    workitem = {"name": f"item {i}", "test":"Hi mom", "age":23}
                    result = await c.PushWorkitem("pyagent", f"item {i}", workitem, [filepath], compressed=True)
                    logging.info(f"Workitem pushed item {i} with id {result._id}")
                    result = await c.PushWorkitem("nodeagent", f"item {i}", workitem, [filepath], compressed=True)
                    logging.info(f"Workitem pushed item {i} with id {result._id}")
            elif text == "push":
                workitem = {"test":"Hi mom", "age":23}
                result = await c.PushWorkitem("q2", "find me", workitem)
                logging.info(f"Workitem pushed with id {result._id}")
            else:
                xpath = await c.GetElement(text)
                logging.info(xpath)
        # except (Exception,BaseException) as e:
        #     print("MAIN EXCEPTION!!!!")
        #     print(repr(e))
        #     traceback.print_tb(e.__traceback__)
        #     pass
if __name__ == "__main__":
    asyncio.run(main())
