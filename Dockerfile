# Base Image
FROM python:3.8
# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
# create and set working directory
RUN mkdir /app
WORKDIR /app
ADD . /app/


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install environment dependencies
RUN pip3 install --upgrade pip

RUN pip install -r requirements.txt
RUN pip3 install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN (echo "from summarizer import Summarizer" ; echo "model = Summarizer()") | python
# Install project dependencies
# RUN pipenv install --skip-lock --system --dev

EXPOSE 8080

RUN python manage.py collectstatic --noinput

CMD gunicorn web_app_text_classify.wsgi:application --timeout 600 --workers=8 --bind 0.0.0.0:8080 & python manage.py qcluster

