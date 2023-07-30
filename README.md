# KLOPP'S LIVERPOOL EPL MATCH PREDICTOR

### Powered by 🅱🅻🅰🆀


![li](https://user-images.githubusercontent.com/100685852/214846024-51910198-1951-48e6-8b1a-2c0a8056dcd8.jpg) ![liv2](https://user-images.githubusercontent.com/100685852/214846291-f3899b64-f38b-43c2-8f72-fc86ff40eb5a.jpg) ![liv](https://user-images.githubusercontent.com/100685852/214846371-205623ff-b198-4313-9353-d6607a4b140e.png)

# Welcome to Klopp's Liverpool EPL Match Predictor!
This prediction service provides insights into Liverpool FC's matches in the English Premier League under the management of Jurgen Klopp. The model has been trained on a dataset consisting of less than 300 EPL matches played by Liverpool since Klopp took charge during the 2015/2016 season. While the dataset is relatively small, our model has demonstrated impressive performance on both previously-seen and unseen data, achieving an accuracy of ```99.62%``` and ```56.06%```, respectively.

### Important Note:
Please be aware that the data and predictions provided by this service are intended for learning and educational purposes only. We strongly discourage using this service for actual gambling or making financial decisions. The outcomes of football matches are influenced by numerous factors, and our model may not account for all dynamic changes in the team's performance.

### Service Overview:
This service predicts the outcome of Liverpool FC's matches in the English Premier League based on various characteristics:

**Form**: Reflects Liverpool's current form based on their performance in the last 5 games. The categories include ***Top*** (won at least 4 of the last 5 games), ***Decent*** (won 3 games), and ***Poor*** (won less than 3 games).

**Opposition**: Measures the challenge posed by the opposition team based on their position on the Premier League table. The categories include ***Tough*** (top 6 on the table or any of the **Big Six** teams placed in the top 9), ***Medium*** (positions 7 to 12 on the table, excluding the *Big Six* teams in 7th, 8th, or 9th positions), and ***Poor*** (outside the top 12 teams).

**Season**: Represents the stage of the season when the match will be played, categorized as ***Early*** (first 11 games), ***Middle*** (12th to 30th games), and ***Late*** (last 8 games).

**Venue**: Indicates whether the match will be played at Liverpool FC's home ground (***Home***) or away from home (***Away***).

**Previous_Match**: Records the outcome of Liverpool FC's previous Premier League match. Marked as ***1*** if they won the previous match and ***0*** if they drew or lost it.

**UEFA**: Represents whether Liverpool FC is participating in European club football competitions at the time. Marked as ***Active*** if they are engaged in either the UEFA Champions League or UEFA Europa League, and ***Inactive*** if they are not.

### Model Performance:
Our model's current accuracy of ```99.62%``` on previously-seen data and ```56.06%``` on unseen data is promising considering the limitations of the dataset. It exhibits a precision of ```62%```, indicating that when it predicts a safe betting opportunity for Liverpool, it is likely to be correct.

### Usage and Caution:
We encourage users to bet responsibly and not rely solely on this prediction service. Football outcomes are unpredictable, and external factors such as injuries, weather conditions, and team dynamics can influence match results. As the team's style and squad change over time, the model's predictions may evolve.

### Running the Service:
Before running the service, create a virtual environment with Python 3.10.11 (or any desired version) using Conda or a virtual environment manager.

- Set up the MLflow server to manage the models using the following command:

```mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host localhost --port 5000```

- Run the notebook ```liverpool.ipynb``` to train and save the initial model.

To run the service using the Dockerfile:

1. Ensure Docker is installed on your system.
2. Install external dependencies using ```pip install -r requirements.txt.```
3. Build the Docker image with ```docker build -t <service-name>:v1 .```
Run the Docker container with ```docker run -it --rm -p 9696:9696 <service-name>:latest```
Use the service with the provided endpoint to get predictions for Liverpool FC matches.



On the 28th day of May 2023, the last game of the season,  Liverpool faced off against Southampton on away grounds. That match ended in a draw and you can run prediction on that game:
```python predict_test.py 0 28/5/2023 top poor late away inactive```

![image](https://github.com/Blaqadonis/klopps_liverpool_updated/assets/100685852/aeb7b62e-0f69-4fec-ade7-73e7a09f0ef9)





Remember that this is an educational service, and actual betting or financial decisions should not be based solely on its predictions.

Feel free to explore the service with family, friends, colleagues, or neighbors. We appreciate any feedback and suggestions for improvement
