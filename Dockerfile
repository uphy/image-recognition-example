FROM continuumio/miniconda3:latest

ENV CONTAINER_USER appuser
ENV CONTAINER_UID 1000
ENV CONTAINER_WORKDIR /work

# Create work directory and container user
RUN useradd -m -s /bin/bash -N -u $CONTAINER_UID $CONTAINER_USER && \
    mkdir -p $CONTAINER_WORKDIR && \
    chown -R $CONTAINER_USER $CONTAINER_WORKDIR

# Setup Python environment for image recognization
RUN apt-get update && \
    apt-get install -y g++ &&\
    apt-get install -y libgtk2.0-0 && \
    rm -rf /var/lib/apt/lists/* && \
    conda install jupyter scikit-learn pandas && \
    pip install keras && \
    conda install -yc menpo dlib=18.18 && \
    conda install -yc menpo opencv3=3.1.0 && \
    conda install -yc anaconda flask=0.11.1 && \    
    conda clean -yt && \
    pip install jupyterthemes && \
    jt -t onedork -T -N && \
    pip install jupyter-emacskeys

# Setup keras
RUN mkdir -p /home/$CONTAINER_USER/.keras && \
    chown -R $CONTAINER_USER /home/$CONTAINER_USER/.keras
ADD keras.json /home/$CONTAINER_USER/.keras

# Start main.py
USER $CONTAINER_USER
ENV PATH /opt/conda/bin:$PATH
WORKDIR $CONTAINER_WORKDIR
EXPOSE 5000
CMD python main.py