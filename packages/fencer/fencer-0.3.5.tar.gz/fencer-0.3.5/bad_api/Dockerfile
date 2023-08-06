FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv
#RUN pipenv install --system --ignore-pipfile
#
#COPY insecure_api /app/
#
#EXPOSE 5000
#
#CMD [ "flask", "run" ]
