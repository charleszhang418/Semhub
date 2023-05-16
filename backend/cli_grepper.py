import semgrepper.semgrepper
import json
if __name__ == '__main__':
    repo_url = input()
    data = semgrepper.semgrepper.semgrep_download(repo_url)
    print(json.dumps(data))