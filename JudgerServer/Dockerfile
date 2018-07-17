FROM ubuntu:16.04
COPY . /code
RUN apt-get update && apt-get install -y cmake python python3 python-pip libseccomp-dev gcc g++ git
RUN git clone -b newnew --depth 1 https://github.com/QingdaoU/Judger && cd Judger && \
	mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python setup.py install && \
	pip install celery && pip install pika
