FROM python:3.12-bookworm

WORKDIR /usr/src/app
COPY ./src /usr/src/app
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python", "code_review_mr.py" ]