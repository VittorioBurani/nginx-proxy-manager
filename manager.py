#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path
from ast import literal_eval
from typing import List, Generator
from abc import ABC, abstractmethod


DOCKER_COMPOSE = Path(__file__).parent / 'docker-compose.yml'
HOMEPAGE       = Path(__file__).parent / 'homepage' / 'index.html'


def execute(cmd:str) -> Generator[str, None, None]:
    '''Execute an external command as a subprocess and yields the output'''
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run_execute(cmd:str) -> None:
    '''Run an external command and print to temrinal'''
    for out_line in execute(cmd):
        print(out_line, end='')


def restart_network() -> None:
    '''Restart the Docker Network'''
    print('Restarting the Docker Network...')
    run_execute('docker compose down && docker compose up -d')


def uncomment_network() -> None:
    '''Uncomment Docker Network settings in the `docker-compose.yml` file'''
    network_name = input('Insert Docker Network name: ')
    print('Uncommenting the Docker Network...')
    doc_comp_cntnt = DOCKER_COMPOSE.read_text()
    doc_comp_cntnt = re.sub(r'#\s+networks:',              r'networks:',               doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+default:',               r'  default:',              doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+external: (true|false)', r'    external: true',      doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+name: \S+',              r'    name: '+network_name, doc_comp_cntnt)
    DOCKER_COMPOSE.write_text(doc_comp_cntnt)


def comment_network() -> None:
    '''Comment Docker Network settings in the `docker-compose.yml` file'''
    print('Commenting the Docker Network...')
    doc_comp_cntnt = DOCKER_COMPOSE.read_text()
    doc_comp_cntnt = re.sub(r'networks:',                 r'# networks:',             doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = re.sub(r'\s+default:',               r'\n#   default:',          doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = re.sub(r'\s+external: (true|false)', r'\n#     external: false', doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = re.sub(r'\s+name: \S+',              r'\n#     name: services',  doc_comp_cntnt, flags=re.S)
    DOCKER_COMPOSE.write_text(doc_comp_cntnt)


def uncomment_homepage() -> None:
    '''Unomment the `homepage` service in the `docker-compose.yml` file'''
    print('Uncommenting `homepage` service...')
    doc_comp_cntnt = DOCKER_COMPOSE.read_text()
    doc_comp_cntnt = re.sub(r'#\s+homepage:',                        r'homepage:',                          doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+image: cupcakearmy/static:latest', r'  image: cupcakearmy/static:latest', doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+pull_policy: always',              r'  pull_policy: always',              doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+restart: unless-stopped',          r'  restart: unless-stopped',          doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+ports:',                           r'  ports:',                           doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+(- \d+:\d+)',                      r'    \1',                             doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+volumes:',                         r'  volumes:',                         doc_comp_cntnt)
    doc_comp_cntnt = re.sub(r'#\s+(-\s\./homepage:/srv:ro)',         r'    \1',                             doc_comp_cntnt)
    DOCKER_COMPOSE.write_text(doc_comp_cntnt)


def comment_homepage() -> None:
    '''Comment the `homepage` service in the `docker-compose.yml` file'''
    print('Commenting `homepage` service...')
    doc_comp_cntnt = DOCKER_COMPOSE.read_text()
    doc_comp_cntnt = re.sub(r'\s+homepage:',                        r'\n  # homepage:',                          doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = re.sub(r'\s+image: cupcakearmy/static:latest', r'\n  #   image: cupcakearmy/static:latest', doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = re.sub(r'\s+(- \d+:\d+)',                      r'\n  #     \1',                             doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = re.sub(r'\s+(-\s\./homepage:/srv:ro)',         r'\n  #     \1',                             doc_comp_cntnt, flags=re.S)
    doc_comp_cntnt = doc_comp_cntnt.replace(
        '\n  #   image: cupcakearmy/static:latest\n    pull_policy: always\n    restart: unless-stopped\n    ports:',
        '\n  #   image: cupcakearmy/static:latest\n  #   pull_policy: always\n  #   restart: unless-stopped\n  #   ports:'
    )
    doc_comp_cntnt = doc_comp_cntnt.replace(
        '\n    volumes:\n  #     - ./homepage:/srv:ro',
        '\n  #   volumes:\n  #     - ./homepage:/srv:ro'
    )
    DOCKER_COMPOSE.write_text(doc_comp_cntnt)


def manage_apps(drop:bool=False) -> None:
    '''Add (drop=False) or Drop (drop=True) an app from the list of exposed apps in the homepage'''
    appname = input(f'Insert app subdomain{" to drop" if drop else ""}: ')
    print(f'{"Dropping selected app from" if drop else "Adding new app to"} the list of exposed apps in the homepage...')
    homepage_cntnt = HOMEPAGE.read_text()
    apps = literal_eval(re.findall(r'const apps = (\[[^\]]*\]);', homepage_cntnt)[0])
    if drop:
        apps.remove(appname)
    else:
        apps.append(appname)
    homepage_cntnt = re.sub(r'(const apps = )\[[^\]]*\];', r"\1"+str(apps)+r';', homepage_cntnt, flags=re.S)
    HOMEPAGE.write_text(homepage_cntnt)


class Cmd(ABC):
    '''Abstract class for commands'''
    def all_cmds(self) -> List[str]:
        return [self.cmd_str] + self.alt_cmds

    def all_cmds_str(self) -> str:
        return '[' + ', '.join(self.all_cmds()) + ']'

    def is_cmd(self, cmd_str:str) -> bool:
        return cmd_str in self.all_cmds()

    @abstractmethod
    def fun(self) -> None:
        pass

    def __call__(self) -> None:
        self.fun()


class Help(Cmd):
    '''Help command'''
    cmd_str  = 'help'
    alt_cmds = ['h', '?']
    msg      = 'print this help'

    def __init__(self, cmd_list:List[Cmd]) -> None:
        self.full_help = ''.join([f'\nAvailable commands:\n  {self.all_cmds_str()} ---> {self.msg}\n'] + [f'  {cmd.all_cmds_str()} ---> {cmd.msg}\n' for cmd in cmd_list])[:-1]

    def fun(self) -> None:
        print(self.full_help)


class Quit(Cmd):
    '''Quit command'''
    cmd_str  = 'quit'
    alt_cmds = ['q', 'exit']
    msg      = 'exit the script'

    def fun(self) -> None:
        print('Exiting the script. Bye!')


class Reload(Cmd):
    '''Reload command'''
    cmd_str  = 'reload'
    alt_cmds = ['r', 'start', 'restart']
    msg      = 'restart the Docker Network'

    def fun(self) -> None:
        restart_network()


class AddNetwork(Cmd):
    '''Add Network command'''
    cmd_str  = 'add-network'
    alt_cmds = ['an', 'addnet', 'add-net']
    msg      = 'set and use a dedicated Docker Network'

    def fun(self) -> None:
        uncomment_network()
        restart_network()


class DropNetwork(Cmd):
    '''Drop Network command'''
    cmd_str  = 'drop-network'
    alt_cmds = ['dn', 'dropnet', 'drop-net']
    msg      = 'drop the dedicated Docker Network and use the default one'

    def fun(self) -> None:
        comment_network()
        restart_network()


class HomeUp(Cmd):
    '''Enable Homepage command'''
    cmd_str  = 'home-up'
    alt_cmds = ['hu', 'hup', 'eh', 'enable-home', 'en-home', 'up-home']
    msg      = 'enable the homepage'

    def fun(self) -> None:
        uncomment_homepage()
        restart_network()


class HomeDown(Cmd):
    '''Disable Homepage command'''
    cmd_str  = 'home-down'
    alt_cmds = ['hd', 'hdown', 'dh', 'disable-home', 'dis-home', 'down-home']
    msg      = 'disable the homepage'

    def fun(self) -> None:
        comment_homepage()
        restart_network()


class AddApp(Cmd):
    '''Add App command'''
    cmd_str  = 'add-app'
    alt_cmds = ['aa', 'addapp']
    msg      = 'add new app to the list of exposed apps in the homepage'

    def fun(self) -> None:
        manage_apps(drop=False)


class DropApp(Cmd):
    '''Drop App command'''
    cmd_str  = 'drop-app'
    alt_cmds = ['da', 'dropapp']
    msg      = 'drop an app from the list of exposed apps in the homepage'

    def fun(self) -> None:
        manage_apps(drop=True)


class CmdList:
    '''Command list manager'''
    def __init__(self) -> None:
        self.cmds = [Reload(), AddNetwork(), DropNetwork(), HomeUp(), HomeDown(), AddApp(), DropApp()]
        self.quit = Quit()
        self.cmds.append(self.quit)
        self.help = Help(self.cmds)
        self.cmds.append(self.help)

    def get_cmd(self, cmd_str:str) -> None:
        for cmd in self.cmds:
            if cmd.is_cmd(cmd_str):
                return cmd
        return None

    def is_quit(self, cmd_str:str) -> None:
        return self.quit.is_cmd(cmd_str)


# Main Function:
def main() -> None:
    # Create objects and force enter:
    cmd_str = 'enter'
    cmd_list = CmdList()
    # Print welcome and help:
    print('''*******************
*** NPM Manager ***
*******************''')
    cmd_list.help()
    print('')
    # Main loop:
    while not cmd_list.is_quit(cmd_str):
        cmd_str = input('> ')
        cmd = cmd_list.get_cmd(cmd_str)
        if cmd:
            cmd()
        else:
            print('Unknown command')
        print('')


# Main Script:
if __name__ == '__main__':
    main()
