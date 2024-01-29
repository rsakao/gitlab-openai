# gitlab-openai
A container that reads GitLab merge requests and does code reviews; sends diffs to Azure OpenAI Service and lets the AI in the Large Language Model do code reviews. The results are written to GitLab's merge request screen with comments.  

GitLabのマージリクエストを読み込み、コードレビューを行うコンテナ。差分をAzure OpenAI Serviceに送り、Large Language ModelのAIにコードレビューを行わせる。結果はGitLabのマージリクエスト画面にコメント付きで書き込まれる。

## usage

### build
docker build:
```
docker build -t aireviewer .
```

> [!NOTE]
> The pre-built image can be found here:
> https://hub.docker.com/r/rsakao/gitlab-openai

### run
docker run:
```
docker run --rm \
  -e GITLAB_URL=<gitlab url> \
  -e GITLAB_TOKEN=<gitlab access token> \
  -e PROJECT_ID=<gitlab project id> \
  -e MERGE_REQUEST_ID=<gitlab merge request id> \
  -e AZURE_KEY=<azure openai api key> \
  -e AZURE_ENDPOINT=<azure openai url> \
  rsakao/gitlab-openai:latest
```
### environment variables
| environment variables | default                        | example                        |
| --------------------- | ------------------------------ | ------------------------------ |
| `GITLAB_URL`          | `https://gitlab.mycompany.com` | `http://mygitlab`              |
| `GITLAB_TOKEN`        | -                              | `abcdefghij1234567890`         |
| `GITLAB_SSL_VERIFY`   | `True`                         | `False`                        |
| `PROJECT_ID`          | -                              | `12345`                        |
| `MERGE_REQUEST_ID`    | -                              | `67890`                        |
| `AZURE_KEY`           | -                              | `xxxxxxx`                      |
| `AZURE_ENDPOINT`      | `https://api.azure.com`        | `https://xxx.openai.azure.com` |
| `AZURE_API_VERSION`   | `2023-09-01-preview`           | `2023-05-15`                   |
| `MODEL`               | `gpt-4`                        | `gpt-4-32k`                    |
| `MAX_TOKEN`           | `5000`                         | `32000`                        |

## development usage
pip install:  
```
pip install -r requirements.txt
```

run:  
```
export $(cat .env)
python code_review_mr.py
```