FROM kong:3.7.1-ubuntu

# Switch to root to install Python
USER root
ADD ./sources.list /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip musl-dev libffi-dev gcc g++ file make -y

RUN mkdir /usr/local/kong/python_plugin/ -p

COPY . /usr/local/kong/python_plugin/
COPY ./requirements.txt /usr/local/kong/python_plugin/requirements.txt

RUN pip install -r /usr/local/kong/python_plugin/requirements.txt


COPY --chown=kong --chmod=777 pluginserver.py /usr/local/bin/kong-python-pluginserver
COPY --chown=kong --chmod=777 ./Langfuse-Kong-Plugin /usr/local/share/lua/5.1/kong/plugins/