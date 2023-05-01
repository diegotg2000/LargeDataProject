FROM jupyter/pyspark-notebook

# move the files into the container
COPY --chown=jovyan ./project /home/jovyan/work/project

# install the required packages
WORKDIR /home/jovyan/work/project

# install textblob with pip
RUN pip install textblob

# install dash with pip
RUN pip install dash