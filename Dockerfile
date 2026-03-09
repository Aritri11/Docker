#base image
FROM python:3.9
#workdir
WORKDIR /app

#copy
COPY . /app

#run
RUN pip install -r requirements.txt

#port
EXPOSE 5000

#command
CMD ["python", "./app.py"]