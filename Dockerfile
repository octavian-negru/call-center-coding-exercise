FROM python:3.9-slim
ADD . /call_center
WORKDIR /call_center
RUN pip install -r requirements.txt
CMD ["python3", "call_center/entrypoint.py"]
