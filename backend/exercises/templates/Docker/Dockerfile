FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Work directory
RUN mkdir sandbox
WORKDIR sandbox
{% if  tar %}
ADD {{ file_tar }} /sandbox/
{% endif %}
#  Install requirements.txt
{% if requirements %}
RUN pip install {{requirements_list}}
{% elif requirements_file %}
RUN pip install -r requirements.txt
{% endif %}

