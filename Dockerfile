FROM python:3.9-slim
ADD . .
WORKDIR .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "call_center/entrypoint.py"]
