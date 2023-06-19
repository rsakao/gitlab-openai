import requests
import openai
from gitlab import Gitlab

# disable warnings unverified HTTPS request
import urllib3
urllib3.disable_warnings()

# GitLabのセットアップ
gl = Gitlab('https://gitlab.example.com', private_token='<GITLAB_TOKEN>')
project_id = '<PROJECT_ID>'
merge_request_id = '<MERGE_REQUEST_ID>'

# OpenAIのセットアップ
openai.api_key = '<OPENAI_API_KEY>'

# マージリクエストの取得
project = gl.projects.get(project_id)
merge_request = project.mergerequests.get(merge_request_id)

# マージリクエストの変更を取得
changes = merge_request.changes()
diffs = changes.get('changes', [])

# 変更の解析
for diff in diffs:

    old_code = diff.get('old_path')
    new_code = diff.get('new_path')

    # ファイルが修正されている（新規作成や削除ではない）場合、解析を行う
    if old_code == new_code:
        prompt = f"""
        # コードレビュー

        次のソースコード修正をレビューしてください:
        
        ```
        {diff['diff']}
        ```

        レビュー結果を以下に記載してください:
        """
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=500
        )

        print(response.choices[0].text)

        # AIのフィードバックをマージリクエストのコメントとして投稿
        note = merge_request.notes.create({"body": response.choices[0].text.strip()})
