FROM icycloud/ubuntu-baseimage:0.9.18
MAINTAINER Icybee <icybee@yeah.net>

ADD . /lshell_build

RUN groupadd icycloud
RUN useradd -g icycloud icycloud
RUN echo "icycloud:icycloud" | chpasswd
RUN /lshell_build/deploy.sh
RUN mkdir /home/icycloud
RUN chown icycloud:icycloud /home/icycloud
CMD ["/sbin/my_entry"]
