FROM debian:8
LABEL maintainer="mihai.bartha@ait.ac.at"

################## BEGIN INSTALLATION ######################
RUN echo "deb http://ftp.de.debian.org/debian testing main" >> /etc/apt/sources.list && \
    echo 'APT::Default-Release "stable";' >> /etc/apt/apt.conf.d/00local && \
    apt-get update --fix-missing && \
    apt-get -t testing -y upgrade && \
    apt-get -t testing install -y python3.6 python3-pip nginx upstart telnet nano curl && \
    pip3 install --upgrade pip && \
    mkdir -p /srv/graphsenserest
COPY requirements.txt /srv/graphsenserest/requirements.txt

RUN pip3 install -r /srv/graphsenserest/requirements.txt

ADD . /srv/graphsenserest/
ADD ./uwsgi /etc/init.d/uwsgi
ADD ./graphsenserest /etc/nginx/sites-available/graphsenserest

RUN ln -s /etc/nginx/sites-available/graphsenserest /etc/nginx/sites-enabled && \
    rm /etc/nginx/sites-enabled/default && \
    touch /run/nginx.pid && \
    touch /var/run/uwsgi.pid && \
    touch /var/log/uwsgi.log

CMD service uwsgi start && service nginx start && tail -f /var/log/uwsgi.log && tail -f /var/log/nginx/error.log
##################### INSTALLATION END #####################
