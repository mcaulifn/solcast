FROM python:3

WORKDIR /app

ADD solcast ./solcast

ADD entrypoint.py ./

ADD setup.cfg ./

ADD setup.py ./

ADD Makefile ./

ADD README.rst ./

ADD HISTORY.rst ./

RUN pip install .

CMD [ "python", "/app/entrypoint.py" ]