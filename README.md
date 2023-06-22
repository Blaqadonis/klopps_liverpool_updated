# KLOPP'S  LIVERPOOL EPL MATCH PREDICTOR by 🅱🅻🅰🆀



![li](https://user-images.githubusercontent.com/100685852/214846024-51910198-1951-48e6-8b1a-2c0a8056dcd8.jpg) ![liv2](https://user-images.githubusercontent.com/100685852/214846291-f3899b64-f38b-43c2-8f72-fc86ff40eb5a.jpg) ![liv](https://user-images.githubusercontent.com/100685852/214846371-205623ff-b198-4313-9353-d6607a4b140e.png)

## Understanding the service:
This is a classifier that predicts if it is safe to bet on Liverpool FC NOT LOSING (win or draw) an English Premier League match under the management of Jurgen Klopp. The dataset upon which this classifier was trained is small, as there have been less than 300 EPL matches for Liverpool since Klopp assumed the managerial position in the 2015/2016 season. Again, there have 
been some tactical and individual alterations in recent times to Jurgen's style that we might have to wait a while to retrieve more data of this new style in order to train a model that is almost foolproof. Nonetheless, this classifier works just fine for now, as is evident in the screenshots below of the model accurately predicting that it would
be safe to bet on Liverpool not losing their EPL match on the 28th of May 2023, against Southampton FC.

## Understanding the data:

*Caveat* This is just for learning purposes. The data is was gotten from https://www.premierleague.com/tables , please do not gamble your hard-earned possessions with the outcome of this project.

This data was trained to predict the 'Outcome', Win  or No_win, of an English Premier League game for Liverpool FC under Klopp's management based on such characteristics as:
1. 'Form' - This is Liverpool's current form. It takes into consideration their performance in the last 5 games. Top means they won at least 4 of the last 5 games, Decent means that they won 3 games, Poor means they won less than 3 games.

2. 'Opposition' - This is the measure of how much of a challenge the opposition team is. It takes into consideration their position on the English Premier League table at the time of the match. Tough means that the opposition club is top 6 on the table, or any of the 'Big Six' is placed top 9. Medium means that the opposition club is placed somewhere between positions 7 and 12 on the table, except for the 'Big Six' placed 7th, 8th, or 9th in which case they are still considered as Tough. Poor means that the opposition club is placed outside of the top 12 teams on the table. 

3. 'Season' - This is the time of the season the match will be played. There is Early, for matches that fall within first 11 matches. Matches that fall between 12th match of the season and 30th match of the season are considered as Middle, while the last 8 matches are considered Late.

4. 'Venue' - This is the ground the match will be played on. There is Home, when Liverpool FC are playing at home in front of their home fans, and Away when they are not.  

5. 'Previous_Match' - This is a record of the outcome of the previous Premier League match played by Liverpool FC. 1 if they won it, 0 otherwise (if they drew it, or lost it). 

6. 'UEFA' - This represents if Liverpool FC are engaged in European club football competitions at the time or not. Active for yes they are engaged in either UEFA Champions League or UEFA Europa League, Inactive for no they are not.

'Big Six' referenced above refers to the 6 clubs that have been dominating the league for over a decade, and have proven to be miles ahead of the other clubs in terms of how difficult it is to get the win over them. These clubs are: Manchester City, Chelsea, Manchester United, Arsenal, Tottenham Hotspurs, and Liverpool. So anytime Liverpool plays against any of the remaining 5 teams of the 'Big Six', as long as they are placed top 9 teams in the table, they are always considered Tough.

## Running this service:


Everything here runs locally. If you want to try out the service, follow the steps below:

Before you proceed, create a virtual environment. I used ```python version 3.10.11``` 

To create an environment with that version of python using Conda: ```conda create -n <env-name> python=3.10.11```

Just replace ```<env-name>``` with any title you want. Next:

 ```conda activate <env-name>``` to activate the environment.
 
Create a directory called model  ```mkdir model```
 
Next, spin up the MLflow server with: ```mlflow server --backend-store-uri sqlite:///local_server.db --default-artifact-root ./artifacts --host localhost --port 5000```

This will create a folder ```artifacts``` on your local machine, as well as the database ```local_server```.

Run the notebook ```liverpool.ipynb```

### 1. Running the container (Dockerfile)


First, you need to have docker installed on your system. I am using a windows machine, and I have docker desktop installed on my system. If you do not have that, then you should try doing that first. If you are all set and good, then proceed.

Now run ```pip install -r requirements.txt``` to install all necessary external dependencies.

Next, Run ```docker build -t <service-name>:v1 .```

Replace ```<service-name>``` with whatever name you wish to give to the service, to build the image.

To run this service ```docker run -it --rm -p 9696:9696 <service-name>:latest```


NOTE: I am running this on Windows hence Waitress. If your local machine requires Gunicorn, I think the Dockerfile should be edited with something like this:


```
FROM python:3.10-slim

RUN pip install -U pip 

WORKDIR /app

COPY [ "predict.py", "tree.bin", "vectorizer.bin", "requirements.txt", "./" ]

RUN pip install -r requirements.txt

EXPOSE 9696 

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "local_server/classifier_predict:app" ]
 ```


If the container is up and running, open up a new terminal. Reactivate the Conda environment. Run ```python webservice/predict_test.py```

NOTE: ```predict_test.py``` is an example of data you can send to the ENTRYPOINT to interact with the service. Edit it as much as you desire and try out some predictions.



### 2. Simple web service (server managed locally with Flask)
  
  
You need to first run:

```pip install -r requirements.txt```

Followed by ```python predict.py``` to run this service.

Open up a new terminal. Run ```python webservice/predict_test.py``` to interact with the service.


### 3. Web service hosted and managed on MLflow servers



 You need to first run: ```pip install -r requirements.txt```

Now, run ```python cloud_server/flow.py``` in one terminal, followed by ```python cloud_server/test_flow.py``` in another terminal.

Try it out with family, friends, colleagues, neighbours, and let me know how to improve on it.

