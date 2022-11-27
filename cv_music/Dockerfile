FROM python:3.9.12

ADD . /
RUN apt-get update
RUN apt-get install libglu1-mesa-dev -y
RUN python -m pip install -r requirements.txt
EXPOSE 8000

CMD python -m uvicorn app:app --host 0.0.0.0 --port 8000