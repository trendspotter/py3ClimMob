FROM ubuntu:20.04

MAINTAINER Alianza Bioversity-CIAT
ENV CR=America/Costa_Rica
ENV DEBIAN_FRONTEND noninteractive
RUN ln -snf /usr/share/zoneinfo/$CR /etc/localtime && echo $CR > /etc/timezone
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y software-properties-common
RUN add-apt-repository universe && add-apt-repository multiverse
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository -y 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
RUN apt-get update

RUN apt-get install -y build-essential qt5-default qtbase5-private-dev qtdeclarative5-dev libqt5sql5-mysql libqt5webkit5-dev libqt5svg5-dev libqt5xmlpatterns5-dev cmake mongodb jq libboost-all-dev unzip zlib1g-dev automake npm redis-server libmysqlclient-dev mysql-client-8.0 openjdk-11-jdk git python3-venv wget texlive-extra-utils r-base libcurl4-openssl-dev pandoc pandoc-citeproc libfontconfig1-dev libcairo2-dev libudunits2-dev libgdal-dev cutycapt xvfb sqlite3 libqt5sql5-sqlite libgmp3-dev libmpfr-dev tidy mysql-shell

# This is a patched MySQL Driver to allow connections between Client 8.0 and Server 5.7.X
COPY ./docker_files/sqldriver/libqsqlmysql.s_o /usr/lib/x86_64-linux-gnu/qt5/plugins/sqldrivers/libqsqlmysql.so

RUN npm install svg2png -g --unsafe-perm

WORKDIR /opt
RUN git clone https://github.com/BioversityCostaRica/wkhtmltopdf.git
WORKDIR wkhtmltopdf
RUN qmake
RUN make -j 4
RUN make install

WORKDIR /opt
RUN git clone https://github.com/AgrDataSci/ClimMob-analysis.git new_r_code

RUN wget https://github.com/BurntSushi/xsv/releases/download/0.13.0/xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz
RUN tar xvfz xsv-0.13.0-x86_64-unknown-linux-musl.tar.gz
RUN cp xsv /bin

RUN git clone https://github.com/qlands/csv2xlsx.git
WORKDIR csv2xlsx
RUN go build
RUN cp csv2xlsx /bin

WORKDIR /opt

RUN git clone https://github.com/qlands/odktools.git

RUN mkdir odktools-deps
WORKDIR /opt/odktools-deps
RUN wget --user=user https://github.com/mongodb/mongo-c-driver/releases/download/1.6.1/mongo-c-driver-1.6.1.tar.gz
RUN wget --user=user https://github.com/jmcnamara/libxlsxwriter/archive/RELEASE_0.7.6.tar.gz
RUN wget https://downloads.sourceforge.net/project/quazip/quazip/0.7.3/quazip-0.7.3.tar.gz
RUN git clone https://github.com/rgamble/libcsv.git

RUN tar xvfz mongo-c-driver-1.6.1.tar.gz
WORKDIR /opt/odktools-deps/mongo-c-driver-1.6.1
RUN ./configure
RUN make
RUN make install
WORKDIR /opt/odktools-deps

RUN tar xvfz quazip-0.7.3.tar.gz
WORKDIR /opt/odktools-deps/quazip-0.7.3
RUN mkdir build
WORKDIR /opt/odktools-deps/quazip-0.7.3/build
RUN cmake -DCMAKE_C_FLAGS:STRING="-fPIC" -DCMAKE_CXX_FLAGS:STRING="-fPIC" ..
RUN make
RUN make install
WORKDIR /opt/odktools-deps

RUN ln -s /usr/bin/aclocal-1.16 /usr/bin/aclocal-1.14
RUN ln -s /usr/bin/automake-1.16 /usr/bin/automake-1.14

RUN tar xvfz RELEASE_0.7.6.tar.gz
WORKDIR /opt/odktools-deps/libxlsxwriter-RELEASE_0.7.6
RUN mkdir build
WORKDIR /opt/odktools-deps/libxlsxwriter-RELEASE_0.7.6/build
RUN cmake ..
RUN make
RUN make install
WORKDIR /opt/odktools-deps

WORKDIR /opt/odktools-deps/libcsv
RUN ./configure
RUN make
RUN make install

WORKDIR /opt/odktools/dependencies/mongo-cxx-driver-r3.1.1
RUN mkdir build
WORKDIR /opt/odktools/dependencies/mongo-cxx-driver-r3.1.1/build
RUN cmake -DCMAKE_C_FLAGS:STRING="-O2 -fPIC" -DCMAKE_CXX_FLAGS:STRING="-O2 -fPIC" -DBSONCXX_POLY_USE_BOOST=1 -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local ..
RUN make
RUN make install
WORKDIR /opt/odktools

RUN qmake
RUN make

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

COPY ./docker_files/packages.r /opt
WORKDIR /opt
RUN Rscript ./new_r_code/R/check_packages.R
RUN Rscript ./packages.r