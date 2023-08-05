import subprocess, sys, os, pathlib, traceback
import asyncio
import openiap
import zipfile, shutil, gzip
def getpackagepath(packagepath, first=True):
    if os.path.isfile( os.path.join(packagepath, "agent.py")): return packagepath
    if os.path.isfile( os.path.join(packagepath, "main.py")): return packagepath
    if os.path.isfile( os.path.join(packagepath, "index.py")): return packagepath
    if(not first): return ""
    if not os.path.exists(packagepath): return ""
    files = os.listdir(packagepath)
    for file in files:
        dir = os.path.join(packagepath, file)
        if not os.path.isfile(dir):
            result = getpackagepath(dir, False)
            if(result != ""): return result
    return ""
def getscriptpath(packagepath):
    if os.path.isfile( os.path.join(packagepath, "agent.py")): return os.path.join("agent.py")
    if os.path.isfile( os.path.join(packagepath, "main.py")): return os.path.join( "main.py")
    if os.path.isfile( os.path.join(packagepath, "index.py")): return os.path.join("index.py")
    return ""
def gitclone(url):
    directory = "package"
    if not os.path.exists(directory):
        subprocess.check_call(["git", "clone", "--recursive", url, directory])
    return directory
def pipinstall(packagepath):
    if os.path.isfile( os.path.join(packagepath, "requirements.txt")):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(packagepath, "requirements.txt")])
def setupenviron():
    # xvfb = subprocess.Popen(['Xvfb', ':99'])
    os.environ["DISPLAY"]=":99"
def runit(packagepath,command):
    os.chdir(packagepath)
    # return subprocess.check_output([sys.executable, command])
    try:
        SCREEN_WIDTH=1920
        SCREEN_HEIGHT=1080
        SCREEN_COLOUR_DEPTH=24
        output = subprocess.check_output([
            "/usr/bin/xvfb-run",
            "-e", "/tmp/xvfb.log",
            f'--server-args=-screen 0 {SCREEN_WIDTH}x{SCREEN_HEIGHT}x{SCREEN_COLOUR_DEPTH} -ac',
            sys.executable, command
        ])
        if(output!=None):
            print(output.decode('utf-8'))
    except Exception as e:
        print("****************** xvfb.log")
        with open("/tmp/xvfb.log", "r") as file:
            content = file.read()
            print(content)
        print("***************************")
        print("runit EXCEPTION!!!!")
        print(repr(e))
        traceback.print_tb(e.__traceback__)
    # SCREEN_WIDTH=1920
    # SCREEN_HEIGHT=1080
    # SCREEN_COLOUR_DEPTH=24
    # print("/usr/bin/xvfb-run")
    # print(f"--server-args=\"-screen 0 {SCREEN_WIDTH}x{SCREEN_HEIGHT}x{SCREEN_COLOUR_DEPTH} -ac\"")
    # print(f"{sys.executable} {command}")
    # return subprocess.check_output(["/usr/bin/xvfb-run", 
    # "-e", "/tmp/xvfb.log", 
    # f"--server-args=\"-screen 0 {SCREEN_WIDTH}x{SCREEN_HEIGHT}x{SCREEN_COLOUR_DEPTH} -ac\"", f"{sys.executable} {command}"])
def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)
async def getpackage(fileid):
    directory = "package"
    c = openiap.Client()
    await c.Signin()
    result = await c.DownloadFile(Id=fileid)
    c.Close()
    if(result.filename == ""):
        raise ValueError("Filename missing or not found")
    if(pathlib.Path(result.filename).suffix == ".zip"):
        with zipfile.ZipFile(result.filename, 'r') as zip_ref:
            zip_ref.extractall(directory)
    elif(pathlib.Path(result.filename).suffix == ".gz"):
        gunzip_shutil(result.filename, directory)
    else:
        shutil.copyfile(result.filename, os.path.join(directory, result.filename))
    return directory
if __name__ == '__main__':
    packagepath = os.environ.get("packagepath", "")
    fileid = os.environ.get("fileid", "")
    gitrepo = os.environ.get("gitrepo", "")
    if(gitrepo != ""):
        packagepath = gitclone(gitrepo)
    if(fileid != ""):
        packagepath = asyncio.run(getpackage(fileid))
        print(packagepath)
    packagepath = getpackagepath(packagepath)
    if(packagepath == ""):
        sys.exit(f"packagepath not found, EXIT!")
    command = getscriptpath(packagepath)
    if command == "":
        sys.exit(f"Failed locating a command to run, EXIT!")
    pipinstall(packagepath)
    setupenviron()
    runit(packagepath, command)
