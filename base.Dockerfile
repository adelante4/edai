# Base image with anaconda and python
FROM miniconda3:23.5.2-0-alpine
# Install the python packages with conda in the base env
COPY ./environment.yml /
RUN conda env update -f /environment.yml -n base && conda clean --all --yes
# Install spacy model
#RUN python -m spacy download de_core_news_lg