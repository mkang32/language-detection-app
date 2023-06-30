# base image to use
FROM python:3.10

# set the current working directory to /code
WORKDIR /code

# copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# install packages if the requirements file has a change, otherwise use cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy all files
COPY . /code

# Run the uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
