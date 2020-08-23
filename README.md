# COMP9900 Meal Match
---
The Avengers team:  
Yiwen Xu: z5224340@ad.unsw.edu.au  
Sheng Du: z5171466@ad.unsw.edu.au  
Mengxiao shao: z5204004@ad.unsw.edu.au  
Yan Zhao: z5180410@ad.unsw.edu.au  
Yaming Kuang: z5215654@ad.unsw.edu.au

![WechatIMG105.png](https://i.loli.net/2020/08/06/wEyFOMuHzARmoTh.png)

This is a website about recipes and ingredients. It can realize user registration, user login, log out, search for ingredients or recipes, and filter search results according to some special requirements. In addition, users can publish their own recipes, and users can comment and like the recipes according to their preferences.
## Initialization
---
1. The project is based on Flask, which based on Werkzeug WSGI toolbox and Jinja2 template engine.  
2. Firstly, check whether you have installed pip3, just type pip3 in terminal. Then you need to install virtual environment by type follow code in terminal:    
` pip install virtualenv`

3. Run the virtual environment on Mac os:  
` virtualenv -p /user/local/bin/python3 env source env/bin/activate`

4. Then, run virtual environment and check whether some packages is installed in the virtual environment:  
` pip freeze`  

5. Install all packages which will be imported in project by typing follow code:  
` pip install -r requirements.txt` 

6. Shutdown virtualenv:  
` deactivate`  

## Required Packages and their version  

The packages and their related version which should be installed has listed in the "requirements.txt":  

 flask==1.1.2  
 Scrapy==2.1.0  
 Flask-RESTful==0.3.8  
 flask-sqlalchemy==2.4.3  
 Flask-Mail==0.9.1  
 itsdangerous==1.1.0  
 pandas==1.0.5  
 gensim==3.8.3  
 textblob==0.15.3  
 matplotlib==3.3.0  
 seaborn==0.10.1  
 wordcloud==1.7.0
 numpy==1.18.5

## Run project
---
* If you use Linux or Mac os, just type follow code to run project:  
```
$ export FLASK_APP=main
$ export FLASK_ENV=production
$ flask run
```
* If you use Windows os, type follow code to run project:  
```
> set FLASK_APP=main
> set FLASK_ENV=production
> flask run
```
* Then copy the link to your broswer.

## Project sturcture
---
```
SourceCode/  
├── Config  
├── DAO  
│   ├── DataBase  
│   └── data  
├── Entities  
├── Service  
│   ├── BuildIn  
│   ├── Comment  
│   ├── Home  
│   ├── Publish  
│   ├── Recipe  
│   ├── Recommend  
│   ├── Scrapy  
│   │   └── Scrapy  
│   │       └── spiders  
│   ├── Search  
│   └── User  
├── Static  
│   ├── css  
│   ├── icon  
│   ├── img  
│   │   └── IngredientTypes  
│   └── js  
├── UI  
│   ├── Frontend  
│   │   ├── css  
│   │   ├── icon  
│   │   └── js  
│   └── Templates  
├── Utils  
```

This root shows the structure of this project.
* Config is the configuration file for flask，which configs "SECRET_KEY" and "SECURITY_PASSWORD_SALT" and so on.  
* DAO stores the database of the project.  
* The entities stores entity files, map database.
* The Service  contains the services models of Meal Match.  
  * BuildIn is a inline model.  
  * Comment model offer the comment function.  
  * Punlish model offer the publish recipe function.  
  * Recipe model offer the function that users can choose their favourite recipe, delate favourite recipe and so on.
  * Recommend model offer the function that website can give the recommendation recipes base on which ingredients are choosed by user.
  * Search model let users can search ingredients and recipes in the "search bar" in homepage, and filter the outcomes. 
  * User model offer the functions include log in, log out, sing up, and forget password.
* Static folder contains static files such as images.
* UI folder stores html files.  

## Website operation display
---
### 1. User model
* 1.1 Sign in  
![sign in.jpeg](https://i.loli.net/2020/08/01/nlZeHB8fTmEQ4vs.jpg)
Use your email address/username and password to login your account and then you can try another functions.  
* 1.2 Sign up  
![sign up.jpeg](https://i.loli.net/2020/08/01/YVNq1efdjGEQL7R.jpg)
If you don't have an account of this website, just click the button "New around here? sign up" which is located at the bottom of "sign in" page.  
* 1.3 Forgot password  
![forgot password.jpeg](https://i.loli.net/2020/08/01/LrBA4s3m1fuW6Sa.jpg)
If you forgot your password, firstly, click the button "Forgot password?" button which is located at the botton of "sign in" page. And then you can reset the password by verifying email address.
* 1.4 Edit profile, check favourite and published recipes, log out  
![logout.jpeg](https://i.loli.net/2020/08/01/ZVH5rATcRF9Qxv6.jpg)  
Click this label, users can edit their profil, check favourite and published recipes, and log out.
### 2. Publish
* Share recipes  
![share recipe.png](https://i.loli.net/2020/07/29/qpVrJE7HO6jidfD.png)
User can publish their own recipes by clicking the yellow button which is named “Share my recipe” in the homepage. In this page, users can input the name, ingredients, time needed of recipe, and choose the type of recipe.  
### 3. Search
* Search and filter  
![search and filter.jpeg](https://i.loli.net/2020/08/01/RYb5NQwJnmUDiEr.jpg)
Users can search ingredients and recipes in the search bar which is located in the homepage. In this page, it will show results that match the user’s search. Furthermore, users can choose the ingredients which they want to cook. Moreover, users can use filter to filter search outcomes.
### 4. Comment
* Publish comment  
![comment.jpeg](https://i.loli.net/2020/08/01/q8lVBLIUFtnEa6o.jpg)
Users can write the comment for recipes and submit it.
### 5. Recommend
![recommend.jpeg](https://i.loli.net/2020/08/01/uFsdTBEAzacQgVY.jpg)
The website can offer some recipes that match the preference of users in the homepage.
