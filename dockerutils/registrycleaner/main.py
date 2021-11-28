import requests
import logging
import sys, getopt

from dockerutils.exception import CmdError
from dockerutils.command import Command

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='cleaner.log', level=logging.DEBUG, format=LOG_FORMAT)

class CleanRegCmdParser:
    @staticmethod
    def parse(argv):
        host = 'localhost'
        port = '5000'
        repo = None
        try:
            opts, args = getopt.getopt(argv, "hH:p:r:", ["host=", "port=", "repo="])
        except getopt.GetoptError:
            raise CmdError('Invalid option of command cleanreg', help())
        for opt, arg in opts:
            if opt == '-h':
                return Helper()
            elif opt in ("-H", "--host"):
                host = arg
            elif opt in ("-p", "--port"):
                port = arg
            elif opt in ("-r", "--repo"):
                repo = arg

        if repo is None:
            raise CmdError('Invalid option of command cleanreg', help())

        return RegistryCleaner(host, port, repo)

class Helper(Command):
    def execute(self):
        print('main.py cleanreg [-H <registry host>] [-p <registry port>] -r <repository name>')
        print('registry host default value is localhost, registry port default value is 5000')

class RegistryCleaner(Command):
    baseurl = None
    repo = None

    def __init__(self, host, port, repo):
        self.baseurl = 'http://' + host + ':' + port + '/v2/'
        self.repo = repo

    def execute(self):
        repo_url = self.baseurl + self.repo
        tags_url = repo_url + '/tags/list'
        tags_resp = requests.get(tags_url)
        tags_err = tags_resp.raise_for_status()
        if tags_err is not None:
            logging.error(f'Fail to get tags for repo {self.repo}: {tags_err}')
            return

        tags_json = tags_resp.json()
        tags = tags_json.get('tags')

        if tags is None:
            return

        for tag in tags:
            logging.info(f'Processing tag {tag}')
            tag_mani_url = repo_url + '/manifests/' + tag
            tag_mani_resp = requests.get(tag_mani_url, headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'})
            tag_mani_err = tag_mani_resp.raise_for_status()
            if tag_mani_err is not None:
                logging.warning(f'Fail to get manifest for tag {tag}: {tag_mani_err}')
                continue
            tag_digest = tag_mani_resp.headers['Docker-Content-Digest']
            digest_url = repo_url + '/manifests/' + tag_digest
            digest_del_resp = requests.delete(digest_url, headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'})
            digest_del_err = digest_del_resp.raise_for_status()
            if digest_del_err is not None:
                logging.warning(f'Fail to delete digest for tag {tag}: {digest_del_err}')
                continue
