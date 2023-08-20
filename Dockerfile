FROM python:3.10
WORKDIR /app
COPY . ./app
SHELL ["/bin/bash", "-c"]
RUN pip install --upgrade pip
RUN python -m venv venv
RUN source venv/bin/activate
#SHELL ["/bin/bash", "-c", "source venv/bin/
RUN pip install -r ./app/requirements.txt
CMD ["python", "./app/main.py"]