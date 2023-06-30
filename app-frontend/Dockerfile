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

# use Streamlit's default port 8501
EXPOSE 8501

# Run the frontend
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501"]
