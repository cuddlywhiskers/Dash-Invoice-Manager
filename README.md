# Dash Invoice Management App
Demo built to create an [invoice management app](https://invoice-management-demo.herokuapp.com/) with built-in analytics for SMEs. 

This app is currently only running on local machines with pre-built SQL databases, there are future plans to develop cloud-based database that allows users to store invoice details on cloud platforms. 

## Usage

To run this app, 

1. kindly fork this repo
2. run the follow code in your command line terminal
```
python app.py 
```
3. Enter this website on your browser: http://127.0.0.1:8050/ 


## Screenshots 
**Dashboard/Main Tab:**
Analytics based on collected invoice 

![Screenshot 2020-03-02 at 11 36 21 PM](https://user-images.githubusercontent.com/54569808/75690964-ac36f780-5cde-11ea-9e27-7a68625f36f8.png)

**Monthly Statement:**
Create monthly statement by filtering for company, statement month and total payable. Readily prints into monthly statement. 

![Screenshot 2020-03-02 at 11 38 12 PM](https://user-images.githubusercontent.com/54569808/75691171-e86a5800-5cde-11ea-9cab-aa48d676379e.png)

**Create New Invoice**
Input new invoice based and store data to generate monthly statement and analytics. 

![Screenshot 2020-03-02 at 11 41 01 PM](https://user-images.githubusercontent.com/54569808/75691640-4bf48580-5cdf-11ea-9384-165d79303723.png)

The app is built using [Dash](https://plot.ly/dash/) and hosted on [Heroku](https://dashboard.heroku.com/)
