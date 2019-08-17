#################################################################
#################################################################
#Ubuntu 18.04 minimal from docker HUB
ARG BASE_CONTAINER=ubuntu:18.04
FROM $BASE_CONTAINER

LABEL maintainer="Luciano Barosi <lbarosi@gmail.com>"
ARG NB_USER="cosmos"

CMD [ “/bin/bash”, “-c” ]
EXPOSE 8888
USER root
#################################################################
# Install all OS dependencies
ADD /install/* /tmp/
RUN apt-get update && apt-get -yq upgrade \
     && cat /tmp/packages| xargs apt-get install -yq --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/packages
#################################################################
#Configure LOCALE
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
#################################################################
# Configure environment
ENV SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
# Add user sudoer
RUN  addgroup --gid 1000 cosmos && \
     adduser --disabled-password  --gecos '' --uid 1000 --ingroup cosmos cosmos && \
     adduser cosmos sudo && \
     echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
#################################################################
USER cosmos:cosmos

ENV  PATH="/usr/bin/:/usr/local/bin/:/opt/conda/bin:${PATH}" \
     LD_LIBRARY_PATH="/opt/cfitsio/lib/:${LD_LIBRARY_PATH}" \
     CLIK_PATH="/home/cosmos/planck_2018/code/plc_3.0/plc-3.01:${LD_LIBRARY_PATH_PATH}"

#################################################################
#PYTHON 3 BASE ENVIRONMENT
ADD  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh /tmp/Miniconda3-latest-Linux-x86_64.sh
# Conda environment should be owned by cosmos
RUN  sudo chown -R cosmos:cosmos /tmp/ && \
     sudo chown -R cosmos:cosmos /opt/ && \
     sudo chown -R cosmos:cosmos /home/cosmos/ &&\
     cd /tmp && \
     sudo chown cosmos:cosmos Miniconda3-latest-Linux-x86_64.sh && \
     /bin/bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
     rm Miniconda3-latest-Linux-x86_64.sh

ENV  PATH=/opt/conda/bin:${PATH}
WORKDIR /home/cosmos
RUN  conda install --quiet --yes conda && \
     conda env create -f /tmp/environment.yml

ENV PATH /opt/conda/envs/cosmos3/bin:$PATH
RUN /bin/bash -c "source activate cosmos3"

#Setting Jupyter to run with password and nice theme
#ENV  PATH=/opt/conda/envs/cosmos3/bin:${PATH}
RUN  jupyter notebook --generate-config && \
     jupyter-nbextension install rise --py --sys-prefix && \
     jupyter-nbextension enable rise --py --sys-prefix && \
     jt -t onedork -T &&\
     python /tmp/jupyterPassword.py
#################################################################
#PYTHON 2 COSMOS ENVIRONMENT
#Making python2 environment
ENV  PATH=/opt/conda/bin:${PATH}
RUN conda env create -f /tmp/environment2.yml
#################################################################
# CFITSIO
# Installing CFITSIO system wide
ADD http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz /tmp
WORKDIR /tmp
RUN  sudo chown -R cosmos:cosmos /tmp/ && \
     /bin/bash /tmp/installCFITSIO.sh
#################################################################
# Installing Planck LikelyHood 2018
ADD http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_Likelihood_Code-v3.0_R3.01.tar.gz /home/cosmos/planck_2018/
WORKDIR /home/cosmos/planck_2018
RUN /bin/bash /tmp/installPlanck2018.sh
#################################################################
# Installing Planck Data 2018
ADD  http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_Likelihood_Data-baseline_R3.00.tar.gz /home/cosmos/planck_2018
WORKDIR /home/cosmos/planck_2018
RUN  sudo chown -R cosmos:cosmos /home/cosmos/planck_2018 && \
     tar zxvf product-action && \
     rm product-action
#################################################################
# Installing CAMB
WORKDIR /home/cosmos
RUN /bin/bash /tmp/installCAMB.sh
#################################################################
# Installing CosmoMC
WORKDIR /home/cosmos
RUN /bin/bash /tmp/installCosmoMC.sh
#################################################################
# # Installing COSMOSIS
WORKDIR /home/cosmos
RUN /bin/bash /tmp/installcosmosis.sh
#################################################################
# # Installing COBAYA
WORKDIR /home/cosmos
RUN mkdir cobaya && \
     cobaya-install cosmo -m /home/cosmos/cobaya
#################################################################
# # Installing CLASS
WORKDIR /home/cosmos
RUN /bin/bash /tmp/installCLASS.sh
#################################################################
# # Installing MontePython
WORKDIR /home/cosmos
RUN /bin/bash /tmp/installMontepython.sh

#Sourcing bashrc
WORKDIR /home/cosmos
RUN cp /tmp/bashrc /home/cosmos/.bashrc && \
     mkdir /home/cosmos/code/ && \
     rm -f /tmp/*
#################################################################
#Preparing smooth jupyter run
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0"]
