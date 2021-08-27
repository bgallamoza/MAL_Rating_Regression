# MyAnimeList (MAL) Anime Rating Prediction
## **Building a machine learning model to predict MAL ratings**

### This model is accessible through an Amazon Web Service (AWS) EC2 instance! Access the model here*: 

### http://ec2-3-144-31-219.us-east-2.compute.amazonaws.com/

**The site may sometimes be offline for maintenance, thank you for understanding*

-----------------------------------------------------------------------------

Hello! This repository documents my entire process obtaining, cleaning, and using MAL API data to construct a few regression models that predict a MAL rating for a theoretical anime. These models include:

1. Linear Regression
2. Lasso Regression
3. Ridge Regression
4. Random Forest Regression
5. Gradient Boosting Regression

To make my model more interactive, I also made a simple web application with Flask and a user interface built in HTML, JavaScript, and CSS. This allows users to obtain a prediction given their inputted data. There is also a 

## **Requirements**
For this project, I used Python 3.9.5 Anaconda version 2021.05. Many libraries are used, including (but not limited to):
1. Sklearn
2. Pandas
3. Matplotlib/Seaborn
4. Flask/flask-cors
5. SQLite 3

To install all libraries used and their dependencies I have included a ```requirements.txt``` for easy installation. You can install these by navigating to your terminal and running:

```pip install -r requirements.txt```

Alternatively, if you have Anaconda installed, I included the environment I used to create this project, which can be installed in the terminal using:

```conda env create -f mal.yml```

You can then activate the environment by entering into your terminal:

```conda activate mal```

You should also have Git Bash installed as well. You can install it here:

https://git-scm.com/downloads

## **Summary**

MyAnimeList (MAL) is an online anime and manga database and community website that contains information about thousands of anime/manga titles. MAL users can interact with this database through many actions, such as bookmarking, reviewing, and rating titles. **We are interested in how we can use the information of TV anime titles to predict a title's rating by MAL users.** 

On MAL, a title's rating is calculated as a weighted score through this formula:

![alt text](/readme_pictures/equation.png "MAL Weighted Score Formula")

> S = Average score for the anime/manga

> v = Number users giving a score for the anime/manga*

> m = Minimum number of scored users required to get a calculated score

> C = The mean score across the entire Anime/Manga database 

**The v variable only includes users who have viewed at least 1/5 of the series and excludes illegitmate accounts*

Due to the popularity of MAL and its use of a weighted score, the MAL rating is a notable way to determine how successful an anime is. **The implication of the MAL rating make it desirable for producers to maximize.** So, finding out how an anime title's attributes affect its rating is valuable when determining what series are worth funding by a producer.

Using the MAL API, features were either used directly or used in feature engineering processes to generate new variables. 

## **Choosing a model**
Five different supervised regressors were trained and tested: linear regressor, lasso regressor, ridge regressor, random forest regressor, and gradient boosting regressor. For each model, different hyperparameters were tuned. **Ultimately, the Gradient Boosting Regressor was chosen for producing the lowest Mean Squared Error of 0.31**

Of the chosen features, variables such as average episode duration, synopsis length, and the number of related anime were very important to our gradient boosting model.

![alt text](/readme_pictures/gboost_importance.png "GBoost Model Importances")

This process is laid out in two Jupyter Notebooks:

### Exploratory Data Analysis (EDA.ipynb)
- Data preprocessing; includes all cleaning, exploring, and graphing in the dataset

### Model_Building.ipynb
- Pipeline and model building process, including hyperparameter testing with GridSearchCV

## **Running the Flask Server**

Next, run the Flask server by navigating to the ```server``` directory and running ```python server.py```

![alt text](/readme_pictures/flask.png "Starting the Flask server in Git Bash")

Now, you can open ```app.html``` in the ```client``` folder and enter your information for a prediction.

![alt text](/readme_pictures/website.png "Preview of the website, server/app.html")

## Using the Website*

**This repo is set up for running the server **locally,** but these instructions are true for the local and deployed AWS EC2 instances*

Enter information into the displayed fields and press "Predict!" to return a rating prediction displayed in the top yellow box.

Invalid values will result in no prediction and an error message in the lower yellow box.

Alternatively, you can also interact with the SQLite database by retrieving the "nth best" prediction (i.e., inputting 1 will give you the best prediction, 2 will give you the 2nd best, etc). Hitting "Retrieve Anime Details" will display that prediction's values in the form above.

Thank you for looking at my project! Have fun!

## References

1. https://myanimelist.net/info.php?go=topanime
2. https://myanimelist.net/about.php