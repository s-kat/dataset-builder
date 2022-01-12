FROM python:3.8
RUN pip install tox && pip install viztracer && pip install pytest

WORKDIR /usr/app/src

COPY . ./

CMD [ "python", "./tox_runner.py"]
