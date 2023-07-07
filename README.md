# Language Detection App
## 1. What it is
This is a web app that identifies what language a text input is written in.

https://github.com/mkang32/language-detection-app/assets/26635198/485628ee-2dd3-4de1-97da-3869031d42d9

This repo consists of two parts: the RESTful API service (`app-api`) and the Streamlit frontend (`app-frontend`). The Streamlit frontend makes API requests to get language predictions and visualize the results. 

## 2. How to run the app
Clone the repo and run docker-compose.
```bash
git clone https://github.com/mkang32/language-detection-app.git
cd language-detection-app

docker-compose up -d --build
```

The container will be accessible at localhost:8501. The frontend code change will be applied without rebuilding the docker container.  

When you want to stop the application, use
```bash
docker-compose stop
```

Alternately, if you want to stop the application, remove the container, and remove all images associated in the docker-compose.yml file. 
```bash
docker-compose down --rmi all
```


## 3. Local Development - ML model
The model is based on [this tutorial](https://github.com/AssemblyAI-Examples/ml-fastapi-docker-heroku). Also, check out more details about the ML model in this [Google Colab](https://colab.research.google.com/drive/1uaALcaatvxOu42IhQA4r0bahfdpw-Z7v?usp=sharing). If you want to update the ML pipeline or the final model output, reference the following logic and update either `app-api/model/model.py` or the final model artifact, `trained_pipeline-0.1.1.pkl`. 

1. Dataset   
It uses this [Kaggle Language Detection dataset](https://www.kaggle.com/datasets/basilb2s/language-detection) in a csv file, which contains 17 languages.
   ```text
   ['Arabic', 'Danish', 'Dutch', 'English', 'French', 'German',
    'Greek', 'Hindi', 'Italian', 'Kannada', 'Malayalam', 'Portugeese',
    'Russian', 'Spanish', 'Sweedish', 'Tamil', 'Turkish']
   ```

2. Pre-processing  
It only takes letters by removing any numbers or special characters using Python built-in regex function.
   ```python
    text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9]', ' ', text)
    text = re.sub(r'[[]]', ' ', text)
    text = text.lower()
   ```

    Then, vectorize the texts using `CountVectorizer`.
    ```python
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    cv.fit(X_train)
    
    x_train = cv.transform(X_train).toarray()
    x_test  = cv.transform(X_test).toarray()
    ```

3. Model  
Build a classifier using `MultinomialNB`.
   ```python
   from sklearn.naive_bayes import MultinomialNB

    model = MultinomialNB()
    model.fit(x_train, y_train)
   ```
   
4. Model export 
Export the model file as a pickle file.
   ```python
    with open('trained_pipeline-0.1.0.pkl','wb') as f:
        pickle.dump(pipe, f)
    ```
   
## 4. Local development - API
In this app, the model is exposed as APIs using FastAPI. Check out `app/main.py`. The main two API end points are as below:

```python
@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}


@app.post("/predict", response_model=PredictionOut)
def predict(payload: TextIn):
    language, prob = predict_pipeline(payload.text)
    return {"language": language, "probability": prob}
```

### 4.1. Set the local environment
Create and activate a virtual environment and install requirements.
```bash
cd app-api
python3 -m venv venv-language-detection-api

source venv-language-detection-api/bin/activate

pip install -r requirements.txt
```

### 4.2. Spin up the API service
Run this in your terminal
```bash
uvicorn main:app --reload
```
You will see something like 
```bash
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
Copy and paste the ULR to your browser. You will see the health check API results.
Note that you cannot test your POST request in your browser because browsers can only handle GET requests.

### 4.3. Test your API
#### 4.3.1. Swagger 
Go to `http://127.0.0.1:8000/docs` and test the end points.
- Click POST `/predict` endpoint 
- Click the 'Try it out' button
- Add a JSON input to Request body
```json
{
  "text": "Hello, how are you?"
}
```
- Click the Execute button
![](images/test_swagger.png)

#### 4.3.2. Postman
Open up Postman and test the end points. 
- Change the request type to POST
- Add a JSON input to the Body
```json
{
  "text": "Hello, how are you?"
}
```
- Click Send
- Check out the response

![](images/test_postman.png)

### 4.4. Dockerize the API (Optional)
As we use docker-compose.yml at the end to dockerize the API and the frontend services, we don't necessarily need this step. However, if you want to test if the API service itself works in a Docker container separately, you can perform this step. 

Build a Docker image. This may take a few minutes if first time.
```bash
cd app-api
docker build -t language-detection-api .
```

Start the Docker Container with the following command
```bash
docker run -d --name language-detection-api -p 80:80 language-detection-api
```

Go to swagger (http://0.0.0.0/docs) or use Postman to test out the endpoints in your dockerized app. Use the same steps above but with the replaced url (http://0.0.0.0:80). Note that the url has changed from `http://127.0.0.1:8000` to `http://0.0.0.0:80`. # TODO

When you rebuild and run a new container with the same name, make sure to remove the existing container.

Check container id: 
```bash
docker ps 
```
Stop the docker container
```bash
docker stop {container_id}
```

Remove the container: 
```bash
docker rm {container_id}
```

## 5. Local Development - Frontend
Streamlit is used for the frontend, which will simply make an API request with the given input text and visualize in the browser.

### 5.1. Set up the local environment
Create and activate a virtual environment and install requirements.
```bash
cd app-frontend
python3 -m venv venv-language-detection-frontend

source venv-language-detection-frontend/bin/activate

pip install -r requirements.txt
```

### 5.2. Launch the streamlit app
Depending on which environment you are running the API service, use the corresponding `API_URL` in `app-frontend/settings.py`. By default, it uses `API_URL = "http://api:80"` assuming the app is built and run through docker-compose.yml. If the API is available through Docker container, activate `"http://0.0.0.0:80"` instead. 

Once the right API url is chosen, open another terminal and run the following command. 
```bash
streamlit run main.py
```
You will be able to see the web app in your browser at this URL:
```http://localhost:8501```

### 5.3. Frontend dockerization
Go to `app-frontend` folder and build a Docker image. This may take a few minutes.
```bash
docker build -t language-detection-frontend .
```

Start the Docker Container with the following command
```bash
docker run -p 8501:8501 language-detection-frontend
```

You should see the output similar to the following:
```bash

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.


  You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:8501
```


# Reference
* [AssemblyAI Example "ml-fastapi-docker-heroku"](https://github.com/AssemblyAI-Examples/ml-fastapi-docker-heroku) for the ML model development and exposing it through FastAPI
* [Paul Iusztin's "The Full Stack 7-Steps MLOps Framework](https://github.com/iusztinpaul/energy-forecasting) for using streamlit for FastAPI application
* [Ben's "streamlit-docker-example"](https://github.com/iwpnd/streamlit-docker-example) for using docker-compose for a streamlit application


## Other
* Frontend photo credit: [Towfiqu barbhuiya](https://unsplash.com/@towfiqu999999?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash
