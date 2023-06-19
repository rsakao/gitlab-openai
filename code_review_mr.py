from gitlab import Gitlab
import os
import openai

# disable warnings unverified HTTPS request
import urllib3
urllib3.disable_warnings()

# 環境変数からパラメータを取得、もしくはデフォルト値を設定
gitlab_url = os.environ.get('GITLAB_URL', 'https://gitlab.example.com')
gitlab_token = os.environ.get('GITLAB_TOKEN', '<DEFAULT_GITLAB_TOKEN>')
gitlab_ssl_verify = os.environ.get('GITLAB_SSL_VERIFY', 'True').lower() == 'true'
project_id = os.environ.get('PROJECT_ID', '<DEFAULT_PROJECT_ID>')
merge_request_id = os.environ.get('MERGE_REQUEST_ID', '<DEFAULT_MERGE_REQUEST_ID>')
azure_key = os.environ.get('AZURE_KEY', None)
azure_endpoint = os.environ.get('AZURE_ENDPOINT', None)

# GitLabのセットアップ
gl = Gitlab(gitlab_url, private_token=gitlab_token, ssl_verify=gitlab_ssl_verify)

# マージリクエストの取得
project = gl.projects.get(project_id)
merge_request = project.mergerequests.get(merge_request_id)

# マージリクエストの変更を取得
changes = merge_request.changes()
diffs = changes.get('changes', [])

# OpenAIのセットアップ
openai.api_key = azure_key if azure_key else "<OPENAI_API_KEY>"
openai.api_base = azure_endpoint if azure_endpoint else "https://api.openai.com"

# 変更の解析
for diff in diffs:
    old_code = diff.get('old_path')
    new_code = diff.get('new_path')

    # ファイルが修正されている（新規作成や削除ではない）場合、解析を行う
    if old_code == new_code:
        documents = [f"""
        # コードレビュー

        次のソースコード修正をレビューしてください:
        
        ```
        {diff['diff']}
        ```

        レビュー結果を以下に記載してください:
        """]
        response = openai.Completion.create(engine="text-davinci-003", prompt=documents[0], max_tokens=500)

        print(response)

        # AIのフィードバックをマージリクエストのコメントとして投稿
        note = merge_request.notes.create({"body": response.choices[0].text.strip()})
