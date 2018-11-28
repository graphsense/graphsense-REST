FROM debian:8
MAINTAINER mihai.bartha@ait.ac.at

################## BEGIN INSTALLATION ######################
RUN echo "deb http://ftp.de.debian.org/debian testing main" >> /etc/apt/sources.list
RUN echo 'APT::Default-Release "stable";' >> /etc/apt/apt.conf.d/00local
RUN apt-get update --fix-missing
RUN apt-get -t testing -y upgrade
RUN apt-get -t testing install -y python3.6 python3-pip nginx upstart telnet nano curl
RUN pip3 install --upgrade pip
RUN mkdir -p /srv/graphsenserest
ADD ./requirements.txt /srv/graphsenserest/


RUN pip3 install cassandra-driver
RUN cd /srv/graphsenserest; pip3 install -r requirements.txt
ADD ./ /srv/graphsenserest/

ADD ./uwsgi /etc/init.d/uwsgi
ADD ./graphsenserest /etc/nginx/sites-available/graphsenserest
RUN ln -s /etc/nginx/sites-available/graphsenserest /etc/nginx/sites-enabled
RUN rm /etc/nginx/sites-enabled/default

RUN touch /run/nginx.pid
RUN touch /var/run/uwsgi.pid
RUN touch /var/log/uwsgi.log
CMD service uwsgi start && service nginx start && tail -f /var/log/uwsgi.log && tail -f /var/log/nginx/error.log
##################### INSTALLATION END #####################
