'''
    Copy right 2023.
'''

import sys
import argparse
import subprocess
import os
import requests
import json
import shutil
import platform
import stat
import uuid
import traceback
from urllib.parse import urlencode
from . import http

verbose = False

def get_python_link_name(pydll_path, os_name):
    if os_name == "linux":
        for so in os.listdir(pydll_path):
            if so.startswith("libpython") and not so.endswith(".so") and so.find(".so") != -1:
                basename = os.path.basename(so[3:so.find(".so")])
                full_path = os.path.join(pydll_path, so)
                return basename, full_path
    return None, None

def format_size(size):

    units = ["Byte", "KB", "MB", "GB", "PB"]
    for i, unit in enumerate(units):
        ref = 1024 ** (i + 1)
        if size < ref:
            div = 1024 ** i
            if i == 0:
                return f"{size} {unit}"
            else:
                return f"{size / div:.2f} {unit}"
    return f"{size} Bytes"

class ChangeCWD:
    def __init__(self, dir):
        self.dir = os.path.abspath(dir)
        self.old = os.path.abspath(os.getcwd())
    
    def __enter__(self):
        os.chdir(self.dir)
        if verbose:
            print(f"Enter {self.dir}")

    def __exit__(self, *args, **kwargs):
        os.chdir(self.old)
        if verbose:
            print(f"Leave {self.dir}, Enter {self.old}")


class Cmd:
    def __init__(self, actions):
        self.parser    = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest="cmd")
        self.actions   = actions

    def add_cmd(self, name : str, help : str = None)->argparse._ActionsContainer:
        return self.subparser.add_parser(name, help=help)

    def help(self):
        self.parser.print_help()

    def hello(self):
        print(
        "      ___                       ___                 \n"+
        "     /\\__\\          ___        /\\__\\          ___   \n"+
        "    /:/  /         /\\  \\      /:/ _/_        /\\  \\  \n"+
        "   /:/__/          \\:\\  \\    /:/ /\\__\\       \\:\\  \\ \n"+
        "  /::\\__\\____      /::\\__\\  /:/ /:/ _/_      /::\\__\\\n"+
        " /:/\\:::::\\__\\  __/:/\\/__/ /:/_/:/ /\\__\\  __/:/\\/__/       Welcome to KIWI World ! Enjoy One-Click Magic!\n"+
        " \\/_|:|~~|~    /\\/:/  /    \\:\\/:/ /:/  / /\\/:/  /  \n"+
        "    |:|  |     \\::/__/      \\::/_/:/  /  \\::/__/                     https://www.zifuture.com\n"+
        "    |:|  |      \\:\\__\\       \\:\\/:/  /    \\:\\__\\    \n"+
        "    |:|  |       \\/__/        \\::/  /      \\/__/    \n"+
        "     \\|__|                     \\/__/                \n"
        "\n"
        "You can use 'kiwi --help' to show the more message."
        )

    def run(self, args, addi_args):
        args = self.parser.parse_args(args)
        if args.cmd is None:
            self.hello()
            return False

        return self.actions.private_run_cmd(args, addi_args)


class Config:
    def __init__(self):
        self.SERVER      = "https://www.zifuture.com/api"
        self.CACHE_ROOT  = os.path.expanduser('~/.cache/kiwi')
        self.CACHE_FILE  = os.path.join(self.CACHE_ROOT, "config.json")
        self.OS_NAME     = platform.system().lower()
        self.PY_VERSION  = ".".join(sys.version.split(".")[:2])
        self.KIWI_ROOT   = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
        self.CWD         = os.path.abspath(os.path.curdir)
        self.PYLIB_DIR   = os.path.join(sys.exec_prefix, "lib")
        self.PYLIB_NAME, self.PYLIB_PATH = get_python_link_name(self.PYLIB_DIR, self.OS_NAME)
        self.DATA_DIR    = os.path.join(self.CACHE_ROOT, "data")
        self.PKG_DIR     = os.path.join(self.CACHE_ROOT, "pkg")
        self.LIB_DIR     = os.path.join(self.CACHE_ROOT, "lib")
        self.CODE_DIR    = os.path.join(self.CACHE_ROOT, "code")
        os.makedirs(self.CACHE_ROOT, exist_ok=True)
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.PKG_DIR,  exist_ok=True)
        os.makedirs(self.LIB_DIR,  exist_ok=True)
        os.makedirs(self.CODE_DIR, exist_ok=True)
        
        self.ACCESS_TOKEN = ""
        self.dynamic_keys = [
            "DATA_DIR", "CODE_DIR", "PKG_DIR", "ACCESS_TOKEN", "SERVER"
        ]
        self.setup()

    def get_dict(self):
        return {
            "SERVER"     : self.SERVER,
            "CACHE_ROOT" : self.CACHE_ROOT,
            "CACHE_FILE" : self.CACHE_FILE,
            "OS_NAME" : self.OS_NAME,
            "PY_VERSION" : self.PY_VERSION,
            "KIWI_ROOT" : self.KIWI_ROOT,
            "CWD" :       self.CWD,
            "PYLIB_DIR" : self.PYLIB_DIR,
            "PYLIB_NAME" : self.PYLIB_NAME,
            "PYLIB_PATH" : self.PYLIB_PATH,
            "DATA_DIR" : self.DATA_DIR,
            "PKG_DIR" : self.PKG_DIR,
            "LIB_DIR" : self.LIB_DIR,
            "CODE_DIR" : self.CODE_DIR,
            "ACCESS_TOKEN" : self.ACCESS_TOKEN
        }

    def load(self):
        if not os.path.exists(self.CACHE_FILE):
            return

        with open(self.CACHE_FILE, "r") as f:
            cfg = json.load(f)
        
        if not isinstance(cfg, dict):
            raise RuntimeError("Config must dict.")
        
        for key in cfg:
            if key in self.dynamic_keys:
                if cfg[key] is not None:
                    setattr(self, key, cfg[key])
            else:
                print(f"Unknow config name {key}")

    def save(self):
        with open(self.CACHE_FILE, "w") as f:
            json.dump({key:getattr(self, key) for key in self.dynamic_keys}, f, indent=4)

    def setup(self):
        if os.path.exists(self.CACHE_FILE):
            self.load()
        else:
            self.save()

    def __repr__(self):
        sb  = ["Config:"]
        dic = self.get_dict()
        for key in dic:
            val = dic[key]
            sb.append(f"   {key} = {val}")
        return "\n".join(sb)


class Actions:
    def __init__(self, app):
        self.app = app
        self.cfg : Config = app.cfg

    def private_run_cmd(self, args, _addi_args):
        
        cmd = args.cmd
        if not hasattr(self, cmd):
            return False

        del args.__dict__["cmd"]
        return getattr(self, cmd)(args, _addi_args)

    def __rmtree(self, dir):
        dir = dir.strip()
        if dir == "." or dir == ".." or dir == "/":
            if verbose:
                print(f"Can not remove directory [{dir}]")
            return

        if os.path.exists(dir):
            if verbose:
                print(f"Remove directory: {dir}")

            shutil.rmtree(dir)

    def __run_py(self, file, args):
        if verbose:
            print(f"Run python script file: {file} at {os.getcwd()}")

        try:
            code_dir = os.path.realpath(os.path.dirname(file))
            union_name = str(uuid.uuid1()).replace("-", "")
            code_name  = f"___tempcode_{union_name}"
            temp_code_file = os.path.join(code_dir, f"{code_name}.py")
            shutil.copyfile(file, temp_code_file)
            sys.path.insert(0, code_dir)
            m = __import__(code_name, globals(), locals(), ["*"])
            os.remove(temp_code_file)
            return getattr(m, "run")(self.app, args)
        except Exception as e:
            traceback.print_exc()
            return False

    def __run_bash(self, file):
        if verbose:
            print(f"Run bash script file: {file} at {os.getcwd()}")

        try:
            code_dir = os.path.realpath(os.path.dirname(file))
            temp_code_file = os.path.join(code_dir, "___tempcode.sh")
            shutil.copyfile(file, temp_code_file)
            code = os.system(f'bash \"{temp_code_file}\"')
            os.remove(temp_code_file)
            return code == 0
        except Exception as e:
            traceback.print_exc()
            return False

    def __run_link(self, file):
        if not os.path.exists(file):
            return False

        try:
            dir = os.path.realpath(os.path.dirname(file))
            with ChangeCWD(dir):
                if verbose:
                    print(f"Run link script file: {file} at {os.getcwd()}")

                dic = self.cfg.get_dict()
                for name in dic:
                    os.environ[name] = dic[name]

                for i, line in enumerate(open(file, "r").readlines()):
                    line = line.replace("\n", "")
                    opts = line.split(" ", maxsplit=1)
                    if len(opts) != 2: continue

                    op    = opts[0]
                    param = opts[1]
                    if op == "link":
                        ps = param.split(" ")
                        if len(ps) == 2:
                            fa = os.path.abspath(ps[0])
                            fb = os.path.abspath(ps[1])
                            if verbose:
                                print(f"Run link command: ln -s \"{fa}\" \"{fb}\"")

                            if os.system(f"ln -s \"{fa}\" \"{fb}\"") != 0:
                                print(f"Failed to run command: ln -s \"{fa}\" \"{fb}\"")
                                return False
                        elif len(ps) == 1:
                            fa = os.path.abspath(ps[0])
                            p  = ps[0].rfind(".so")
                            if p == -1:
                                print(f"Can not process this command: {line}")
                                return

                            fb = os.path.abspath(ps[0][:p+3])
                            if verbose:
                                print(f"Run link command: ln -s \"{fa}\" \"{fb}\"")

                            if os.system(f"ln -s \"{fa}\" \"{fb}\"") != 0:
                                print(f"Failed to run command: ln -s \"{fa}\" \"{fb}\"")
                                return False
                        else:
                            print(f"Invalid command in line: {i}, {line}")
                            return False

                    elif op == "cmd":
                        if verbose:
                            print(f"Run command: {param}")

                        if os.system(param) != 0:
                            print(f"Invalid command: {param}")
                            return False
            if verbose:
                print(f"Remove {file}")
            os.remove(file)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def config(self, args : argparse.Namespace, addi_args):

        if args.key is None and args.value is None:
            print(self.cfg)
            return False

        if args.value is None:
            print(getattr(self.cfg, args.key))
            return False
        
        if args.key not in self.cfg.dynamic_keys:
            print(f"Unsupport config name {args.key}")
            return False

        setattr(self.cfg, args.key, args.value)
        self.cfg.save()
        print("Success!")
        return True

    def auth(self, args : argparse.Namespace, addi_args):
        setattr(self.cfg, "ACCESS_TOKEN", args.token)
        self.cfg.save()
        print("Success!")
        return True

    def get(self, args : argparse.Namespace, addi_args):
        repo = args.repo
        if repo.find("/") == -1:
            print(f"Invalid repo name: {repo}")
            return False

        owner, proj = repo.split("/")
        file = os.path.join(self.cfg.CODE_DIR, repo + ".zip")
        fileurl = f"{self.cfg.SERVER}/public/repo/zip/{repo}?accessToken={self.cfg.ACCESS_TOKEN}"
        md5url  = f"{self.cfg.SERVER}/public/repo/shortinfo/{repo}?accessToken={self.cfg.ACCESS_TOKEN}"
        if not http.require_file_and_check_md5(fileurl, md5url, file, f"Getting {repo}", args.update, verbose)[0]:
            print(f"Failed to get repo {repo}.")
            return False

        if args.save is not None:
            proj = args.save

        self.__rmtree(proj)
        http.extract_zip_to(file, proj, verbose)

        if not args.disable_run:
            with ChangeCWD(proj):
                auto_config_file = ".kiwi/auto.py"
                if os.path.exists(auto_config_file):
                    self.__run_py(auto_config_file, args)

                auto_config_file = ".kiwi/auto.sh"
                if os.path.exists(auto_config_file):
                    self.__run_bash(auto_config_file)
        return True

    def getd(self, args : argparse.Namespace, addi_args):
        data = args.data
        if data.find("/") == -1:
            print(f"Invalid data name: {data}")
            return False

        owner, dname = data.split("/")

        file = os.path.join(self.cfg.DATA_DIR, data + ".zip")
        fileurl = f"{self.cfg.SERVER}/public/data/download/{data}?accessToken={self.cfg.ACCESS_TOKEN}"
        md5url  = f"{self.cfg.SERVER}/public/data/shortinfo/{data}?accessToken={self.cfg.ACCESS_TOKEN}"
        ok, info = http.require_file_and_check_md5(fileurl, md5url, file, f"Getting {data}", args.update, verbose)
        if not ok:
            print(f"Failed to install data {data}.")
            return False

        if info["type"] == "PythonScript":
            if not args.disable_run:
                return self.__run_py(file, args)
            else:
                print(f"Script run denied: {file}")
                return False
        elif info["type"] == "BashScript":
            if not args.disable_run:
                return self.__run_bash(file)
            else:
                print(f"Script run denied: {file}")
                return False
        else:
            if args.save is not None:
                dname = args.save

            self.__rmtree(dname)
            http.extract_zip_to(file, dname, verbose)
            return True

    def install(self, args : argparse.Namespace, addi_args):

        pkg = args.pkg
        if pkg.find("/") == -1:
            print(f"Invalid pkg name: {pkg}")
            return False

        owner, dname = pkg.split("/")

        file = os.path.join(self.cfg.PKG_DIR, pkg + ".zip")
        fileurl = f"{self.cfg.SERVER}/public/pkg/download/{pkg}?accessToken={self.cfg.ACCESS_TOKEN}"
        md5url  = f"{self.cfg.SERVER}/public/pkg/shortinfo/{pkg}?accessToken={self.cfg.ACCESS_TOKEN}"
        ok, info = http.require_file_and_check_md5(fileurl, md5url, file, f"Getting {pkg}", args.update, verbose)
        if not ok:
            print(f"Failed to install pkg {pkg}.")
            return False

        if info["type"] == "PythonScript":
            if not args.disable_run:
                return self.__run_py(file, args)
            else:
                print(f"Script run denied: {file}")
                return False
        elif info["type"] == "BashScript":
            if not args.disable_run:
                return self.__run_bash(file)
            else:
                print(f"Script run denied: {file}")
                return False
        else:
            if args.save is None:
                install_to = os.path.join(self.cfg.LIB_DIR, dname)
            else:
                install_to = args.save

            self.__rmtree(install_to)
            http.extract_zip_to(file, install_to, verbose)

            print(f"Install to {install_to}")
            link_file = os.path.abspath(os.path.join(install_to, ".link"))
            if os.path.exists(link_file):
                return self.__run_link(link_file)
            return True

    def clean(self, args : argparse.Namespace, addi_args):
        self.__rmtree(self.cfg.CODE_DIR)
        self.__rmtree(self.cfg.PKG_DIR)
        self.__rmtree(self.cfg.DATA_DIR)
        os.makedirs(self.cfg.DATA_DIR, exist_ok=True)
        os.makedirs(self.cfg.PKG_DIR,  exist_ok=True)
        os.makedirs(self.cfg.CODE_DIR, exist_ok=True)
        return True

    def run(self, args : argparse.Namespace, addi_args):

        file    = args.runfile
        workdir = args.workdir

        if file is None:
            file = os.path.abspath(".kiwi/auto.py")
            if not os.path.exists(file):
                cwd = os.path.abspath(os.getcwd())
                p = cwd.rfind("/")
                while p != -1:
                    file = os.path.join(cwd[:p], ".kiwi/auto.py")
                    if os.path.exists(file):
                        break
                    p = cwd.rfind("/", 0, p)
                    
            if not os.path.exists(file):
                file = os.path.abspath(".kiwi/auto.sh")
                if not os.path.exists(file):
                    cwd = os.path.abspath(os.getcwd())
                    p = cwd.rfind("/")
                    while p != -1:
                        file = os.path.join(cwd[:p], ".kiwi/auto.sh")
                        if os.path.exists(file):
                            break
                        p = cwd.rfind("/", 0, p)

        if not os.path.exists(file):
            print("Can not found any auto script to run.")
            return False

        if workdir is None:
            workdir = os.path.dirname(os.path.dirname(file))

        with ChangeCWD(workdir):

            if addi_args is not None:
                allargs = addi_args
                kwargs_map = {}
                args_list  = []
                for item in allargs:
                    if item.startswith("--") or item.startswith("-"):
                        stlen = 2 if item.startswith("--") else 1
                        line = item[stlen:]
                        p = line.find("=")
                        if p != -1:
                            kwargs_map[line[:p]] = line[p+1:]
                        else:
                            kwargs_map[line] = True
                    else:
                        args_list.append(item)
                args.args = args_list
                args.__dict__.update(kwargs_map)

            if file.endswith(".py"):
                return self.__run_py(file, args)
            elif file.endswith(".sh"):
                return self.__run_bash(file)
            return False

    def search(self, args : argparse.Namespace, addi_args):
        param = urlencode({"key": args.key, "accessToken": self.cfg.ACCESS_TOKEN})
        url = f"{self.cfg.SERVER}/public/search/list?" + param
        data = http.request_text(url)
        if data is None:
            return False

        print(f"Search {len(data)} results using {args.key}")
        for i, (size, shortDescription, createTime, dtype, path) in enumerate(data):
            
            i += 1
            if dtype in ["Data", "Package"]:
                if shortDescription is not None:
                    print(f"{i}[{dtype}]: {path}, {format_size(size)}, {shortDescription}")
                else:
                    print(f"{i}[{dtype}]: {path}, {format_size(size)}")
            else:
                if shortDescription is not None:
                    print(f"{i}[{dtype}]: {path}, {shortDescription}")
                else:
                    print(f"{i}[{dtype}]: {path}")
        return True

class Application:
    def __init__(self):
        self.cfg     = Config()
        self.actions = Actions(self)
        self.setup_env()

    def setup_env(self):
        os.makedirs(self.cfg.CACHE_ROOT, exist_ok=True)

    def run_with_command(self, args=None)->bool:

        global verbose
        if args is not None and isinstance(args, str):
            args = args.split(" ")
        elif args is None:
            args = sys.argv[1:]

        for i in range(len(args)):
            if args[i] == "-verbose":
                del args[i]
                verbose = True
                break
        
        addi_args = None
        if len(args) > 0:
            if(args[0] == "run"):
                addi_args = []
                old_args  = []
                skip = [False] * len(args) 
                for i in range(1, len(args)):
                    if skip[i]: continue

                    arg = args[i]
                    if not (arg.startswith("-runfile") or arg.startswith("-workdir")):
                        addi_args.append(arg)
                    else:
                        if arg.find("=") == -1:
                            if i + 1 < len(args):
                                old_args.append(arg)
                                old_args.append(args[i + 1])
                                skip[i + 1] = True
                        else:
                            old_args.append(arg)
                args = ["run"] + old_args

        cmd = Cmd(self.actions)
        c = cmd.add_cmd("config", "Configure")
        c.add_argument("key",   nargs="?", type=str, help=f"config name, support: {', '.join(self.cfg.dynamic_keys)}")
        c.add_argument("value", nargs="?", type=str, help="config value")

        c = cmd.add_cmd("get", "Get code from server")
        c.add_argument("repo", type=str, help="repo name")
        c.add_argument("-update", action="store_true", help="Force update")
        c.add_argument("-save", type=str, help="Unzipped folder")
        c.add_argument("-disable-run", action="store_true", help="Disable auto run")

        c = cmd.add_cmd("run", "Run script")
        c.add_argument("-runfile", type=str, help="script file, default is .kiwi/auto.py or .kiwi/auto.sh")
        c.add_argument("-workdir", type=str, help="workspace dir, default is solution dir")

        c = cmd.add_cmd("auth", "Set auth ACCESS_TOKEN")
        c.add_argument("token", type=str, help="Access token name")

        c = cmd.add_cmd("getd", "Get data from server")
        c.add_argument("data", type=str, help="data name")
        c.add_argument("-update", action="store_true", help="Force update")
        c.add_argument("-save", type=str, help="Unzipped folder")
        c.add_argument("-disable-run", action="store_true", help="Disable auto run")

        c = cmd.add_cmd("clean", "Clean cache file")

        c = cmd.add_cmd("install", "Install package from server")
        c.add_argument("pkg", type=str, help="pkg name")
        c.add_argument("-update", action="store_true", help="Force update")
        c.add_argument("-save", type=str, help="Unzipped folder")
        c.add_argument("-disable-run", action="store_true", help="Disable auto run")

        c = cmd.add_cmd("search", "Search solution / data / package")
        c.add_argument("key", type=str, help="search name")
        return cmd.run(args, addi_args)