FROM python:alpine3.7
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev 
COPY . /app
WORKDIR /app
RUN pip install cython
RUN . /scipyfile.sh
RUN pip install scipy 
ENTRYPOINT ["python"]
CMD ["python", "main.py"]
