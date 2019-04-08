FROM python:3.6.5-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code && mkdir /code/static
WORKDIR /code
COPY . /code/
ADD cmd.sh /
RUN chmod +x /cmd.sh
RUN pip install --upgrade pip
RUN pip install -r requirements/base.txt
CMD ["/cmd.sh"]