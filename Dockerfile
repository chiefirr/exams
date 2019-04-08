# Pull base image
FROM python:3.6.5-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE=exams.settings
#ENV SECRET_KEY (ibg99*)q#=&rs-+u4d1tl45*fp7#iq4pll^^(=hi9q!7)o_t9
#ENV DB_NAME exams
#ENV DB_USER examo
#ENV DB_PASSWORD 123qwe!!!
# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies
# RUN pip install virtualenv
# COPY Pipfile Pipfile.lock /code/

# Copy project
ADD . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements/base.txt
RUN mkdir /static
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Server
#EXPOSE 8000
#STOPSIGNAL SIGINT
#ENTRYPOINT ["python", "manage.py"]
#CMD ["runserver", "0.0.0.0:8000"]