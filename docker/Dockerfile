#docker build -t [image_name] .
#docker exec -it [container_id] bash
#docker run -p 5000:5000 [image_name]

FROM ubuntu:18.04

RUN apt update
RUN apt install -y nodejs npm libstdc++6 libgconf-2-4
RUN apt install -y python-pip git yarn
RUN apt install -y build-essential python-dev libxml2 libxml2-dev zlib1g-dev libatlas3-base liblzma-dev
RUN rm -rf /var/cache/apt/*

RUN cd /home \
	&& git clone https://github.com/swcmdb/pyflow3.git
	
RUN cd /home/pyflow3/src \
	&& pip install --target . flask

RUN cd /home/pyflow3/src/static \
	&& npm install
	
WORKDIR /
EXPOSE 5000

CMD python /home/pyflow3/src/server.py
 
	



