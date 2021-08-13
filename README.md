# MyAnimeList (MAL) Anime Rating Prediction
## **Building a machine learning model to predict MAL ratings**

Hello! This repository documents my entire process obtaining, cleaning, and using MAL API data to construct a few regression models that predict a MAL rating for a theoretical anime. These models include:

1. Linear Regression
2. Lasso Regression
3. Ridge Regression
4. Random Forest Regression
5. Gradient Boosting Regression

This process is laid out in two Jupyter Notebooks:

### **Exploratory Data Analysis (EDA.ipynb)**
    Data preprocessing; includes all cleaning, exploring, and graphing in the dataset

### **Model_Building.ipynb**
    Pipeline and model building process, including hyperparameter testing with GridSearchCV

To make my model more interactive, I also made a simple web application with Flask and a user interface built in HTML, JavaScript, and CSS. This allows users to obtain a prediction given their inputted data.

## **Libraries Used**
For this project, I used Anaconda version 2021.05, which should come with all necessary libararies used throughout the project. Notable libraries used include:
1. Sklearn
2. Pandas
3. Matplotlib/Seaborn
4. Flask/flask-cors

To make this process easier, I have included a ```requirements.txt``` file to install all the necessary Python libraries. You can install these by navigating to your terminal and running:

```pip install -r requirements.txt```

Alternatively, if you have Anaconda installed, I included the environment I used to create this project, which can be installed in the terminal using:

```conda env create -f mal.yml```

You can then activate the environment by entering into your terminal:

```conda activate mal```

## **Summary**

MyAnimeList (MAL) is an online anime and manga database and community website that contains information about thousands of anime/manga titles. MAL users can interact with this database through many actions, such as bookmarking, reviewing, and rating titles. **We are interested in how we can use the information of TV anime titles to predict a title's rating by MAL users.** 

On MAL, a title's rating is calculated as a weighted score through this formula:

### Weighted Score = $(\frac{v}{v + m}*S) + (\frac{m}{v + m}*C)$

> S = Average score for the anime/manga

> v = Number users giving a score for the anime/manga*

> m = Minimum number of scored users required to get a calculated score

> C = The mean score across the entire Anime/Manga database 

**The v variable only includes users who have viewed at least 1/5 of the series and excludes illegitmate accounts*

Due to the popularity of MAL and its use of a weighted score, the MAL rating is a notable way to determine how successful an anime is. **The implication of the MAL rating make it desirable for producers to maximize.** So, finding out how an anime title's attributes affect its rating is valuable when determining what series are worth funding by a producer.

Using the MAL API, features were either used directly or used in feature engineering processes to generate new variables. 

## **Choosing a model**
Five different supervised regressors were trained and tested: linear regressor, lasso regressor, ridge regressor, random forest regressor, and gradient boosting regressor. For each model, different hyperparameters were tuned. **Ultimately, the Gradient Boosting Regressor was chosen for producing the highest $R^2$ value and the lowest MSE and MAE.** 

## **Running the Flask Server**

Next, run the Flask server by navigating to the ```server``` directory and running ```python server.py```

![alt text](/readme_pictures/flask.png "Starting the Flask server in Git Bash")

Now, you can open ```app.html``` in the ```client``` folder and enter your information for a prediction.

![alt text](/readme_pictures/website.png "Preview of the website, server/app.html")

Have fun!

## References

1. https://myanimelist.net/info.php?go=topanime
2. https://myanimelist.net/about.php