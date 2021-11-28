import requests
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='cleaner.log', level=logging.DEBUG, format=LOG_FORMAT)

class RegistryCleaner:
    baseurl = None

    def __init__(self, host, port):
        self.baseurl = 'http://' + host + ':' + port + '/v2/'

    def clean_repo(self, repo):
        repo_url = self.baseurl + repo
        tags_url = repo_url + '/tags/list'
        tags_resp = requests.get(tags_url)
        tags_err = tags_resp.raise_for_status()
        if tags_err is not None:
            logging.error(f'Fail to get tags for repo {repo}: {tags_err}')
            return

        tags_json = tags_resp.json()
        tags = tags_json.get('tags')
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
