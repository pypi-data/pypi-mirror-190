FROM git.jinr.ru:5005/malyshkin/ubuntu_ntsim_requirements:latest

WORKDIR /workdir

COPY . /software/ntsim
COPY docker/install_nudisxs.sh /workdir
RUN /workdir/install_nudisxs.sh
RUN pip install g4camp mumpropagator

COPY docker/setup.sh /software/
RUN echo "source /software/setup.sh" >> /root/.bashrc

RUN rm -rf /workdir/*
COPY ntsim/tutorials/configs /workdir/configs
COPY docker/run_tests.sh /workdir/
COPY docker/tests/ /workdir/tests/
#RUN /workdir/tests.sh

