# Base image with anaconda and python
FROM eda-base:base
# Copy all the files from this repo into the image
COPY ./ /
# Make entrypoint file executable no matter from whom
RUN chmod +x entrypoint.sh
# Define entrypoint for commands
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
