from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, abort, flash
from flask_login import login_required, current_user

import pandas as pd
import sqlite3
import pickle

query = Blueprint('query', __name__)
def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM Sheet1"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data_from_db('project/data/data.db')
categories = sorted(df['product_interest'].astype(str).unique())

df2 = pd.read_excel('project/data/99999.xlsx')


@query.route('/')
def index():
    return render_template('index.html', title='home', active='home')

@query.route('/about')
def about():
    return render_template('about.html', title='about', active='about')

@query.route('/service')
# @login_required
def service():
    return render_template('service.html', title='service', active='service')

@query.route('/price')
def price():
    return render_template('price.html', title='price', active='price')

@query.route('/contact')
def contact():
    return render_template('contact.html', title='contact', active='contact')

@query.route('/StreamerRank')
def StreamerRank():
    return render_template('StreamerRank.html', title='Streamer Rank')

@query.route('/DataVisualization')
def DataVisualization():
    return render_template('DataVisualization.html', title='Data Visualization')

@query.route('/SelectStreamer')
def SelectStreamer():
    return render_template('SelectStreamer.html', title='Select Streamer')


@query.route('/PeriodSuggestion', methods=['GET', 'POST'])
def PeriodSuggestion():
    result = ''
    input_value = 'All'
    start_time = 0
    end_time = 0

    if request.method == 'POST':
        input_value = request.form['input_value']
        start_time = int(request.form['start_time'])
        end_time = int(request.form['end_time'])

    if input_value != 'All':
        df = pd.read_excel('project/data/period.xlsx')
        df = df.loc[df["類別"] == input_value]

        df = df[(df['start_time'] >= start_time) & (df['end_time'] <= end_time)]
        if df.empty:
            result = ""
            result = f"There are no live-streaming in this time period{result}"
            return render_template('PeriodSuggestion.html', result=result, title='Streaming Period Suggestion')
        time_counts = df['start_time'].value_counts()
        min_count = time_counts.min()
        min_value = time_counts[time_counts == min_count].index[0]
        min_row = df[df['start_time'] == min_value].iloc[0]
        result = int(min_row['start_time'])
        result = f"We recommend starting the live-streaming at {result}:00"

    return render_template('PeriodSuggestion.html', result=result, title='Streaming Period Suggestion')

@query.route('/PriceSuggestion')
def PriceSuggestion():
    result = ''
    return render_template('PriceSuggestion2.html', **locals())


@query.route('/PriceSug', methods=['GET', 'POST'])
def PriceSug():
    result = ''

    if request.method == 'POST':
        df1 = pd.read_excel('project/data/product.xlsx')
        category = request.form['category']
        costing = float(request.form['costing'])
        profit_margin = float(request.form['profit_margin'])
        selling_price = request.form['selling_price']
        price = costing * ((100 + profit_margin) / 100)

        total = 0
        count = 0
        for i in range(len(df1)):
            if df1['category'][i] == category:
                total += df1['price'][i]
                count += 1
        ave_SellPrice = total / count

        if (selling_price == 'OPTIONAL'):
            selling_price = 0
            result = "The suggested selling price is: ${:.2f}, The average selling price in the database is ${:.2f}".format(price, ave_SellPrice)
        else:
            selling_price = float(selling_price)
            if float(selling_price) > price:
                result = "The selling price is NOT REASONABLE as it exceeded the profit margin, the suggested selling price is: ${:.2f},  " \
                         "The average selling price in the database file is: ${:.2f}".format(price, ave_SellPrice)
            elif float(selling_price) == price:
                result = "The selling price is REASONABLE. The average selling price in the database file is: ${:.2f}".format(ave_SellPrice)
            else:
                result = "The selling price is NOT REASONABLE as it has not enough profit margin, the suggested selling price is: ${:.2f} " \
                         "The average selling price in the database file is: ${:.2f}".format(price, ave_SellPrice)

    return render_template('PriceSuggestion2.html', title='Price Suggestion', **locals())

@query.route('/SalesPrediction', methods=['GET', 'POST'])
def SalesPrediction():
    result = ''
    return render_template('SalesAmountPrediction1.html', **locals())

@query.route('/predict', methods=['GET', 'POST'])
def predict():
    # Basic information/data
    modelSelection = int(request.form['model_selection'])    # Use the loaded model to make predictions
    if modelSelection == 1:
        model = pickle.load(open('project/modelprojRidge.sav', 'rb'))
        report_message = 'Ridge regression is a type of regularized linear regression model used in statistics and machine learning. ' \
                         'It is a modification of the ordinary least squares (OLS) regression method that adds a penalty term to the ' \
                         'regression equation in order to avoid overfitting and improve the predictive accuracy.'
    elif modelSelection == 2:
        model = pickle.load(open('project/modelLasso.sav', 'rb'))
    elif modelSelection == 3:
        model = pickle.load(open('project/modelprojNN.sav', 'rb'))

    gender = int(request.form['sex'])
    FansNumber = float(request.form['fans_number'])
    MemNumber = float(request.form['member_number'])
    TotLiNumber = int(request.form['total_live_number'])
    TotSaRev = float(request.form['totalSales_revenue'])
    TotSaVol = float(request.form['totalSales_volume'])

    # Data within 30 days
    LiNum30 = float(request.form['live_number_within30.1'])
    TotProConvRate = float(request.form['totalProductConversion_rate'])
    AveUValue = float(request.form['average_uv_value'])
    TotProdNum = float(request.form['total_product_number'])
    TotFansChange = float(request.form['total_fans_change'])
    TotVideoNum = float(request.form['total_video_number'])
    AveVideoLikNum = float(request.form['average_videoLike_number'])
    AveVideoViNum = float(request.form['average_videoViewe_number'])
    AveCommentNumperVideo = float(request.form['average_videoComment_number'])
    AveFeFansRate = float(request.form['average_femaleFans_rate'])
    AveMaFansRate = float(request.form['average_maleFans_rate'])

    # Data of last live
    LiTime = float(request.form['living_time(h)'])
    ViNum = float(request.form['viewer_number'])
    prodNum = float(request.form['product_number'])
    ComNum = float(request.form['comment_number'])
    SaNum = float(request.form['sales_number'])
    IncFansNum = float(request.form['increaseFans_number'])
    VibecomeFansRate = float(request.form['fans_rate'])
    NumLik = float(request.form['like_number'])
    ProdConRate = float(request.form['ProductConversion_rate'])
    AveSaperPerson = float(request.form['perSales'])
    UValue = float(request.form['UV_value'])
    NumLuckybags = float(request.form['lucky_bag'])
    AvestayTimeperPerson = float(request.form['averageStay_time'])
    InteractionRate = float(request.form['interact_rate'])
    FeFansProp = float(request.form['femaleFans_rate'])
    MaFansProp = float(request.form['maleFans_rate'])
    ProdInterest = float(request.form['product_interest'])
    # set the variable for product interest
    Apparel = 0
    Baby = 0
    Beauty = 0
    Food = 0
    Household = 0
    if ProdInterest == 1:
        Apparel = 1;
    elif ProdInterest == 2:
        Baby = 1;
    elif ProdInterest == 3:
        Beauty = 1;
    elif ProdInterest == 4:
        Food = 1;
    elif ProdInterest == 5:
        Household = 1;
    # StartTime = request.form['hourSelect']

    result = model.predict([[gender, FansNumber, MemNumber, TotLiNumber, TotSaRev, TotSaVol, LiNum30, TotProConvRate,
                             AveUValue, TotProdNum,
                             TotFansChange, TotVideoNum, AveVideoLikNum, AveVideoViNum, AveCommentNumperVideo,
                             AveFeFansRate, AveMaFansRate, LiTime, ViNum, prodNum,
                             ComNum, SaNum, IncFansNum, VibecomeFansRate, NumLik, ProdConRate, AveSaperPerson, UValue,
                             NumLuckybags, AvestayTimeperPerson, InteractionRate, FeFansProp,
                             MaFansProp, Apparel, Baby, Beauty, Food, Household]])[0]

    return render_template('SalesAmountPrediction1.html', title='Sales Prediction', **locals())

@query.route('/SearchFilter', methods=['GET', 'POST'])
def SearchFilter():
    if request.method == 'POST':
        # Get user input from search form
        query = request.form.get('query')

        if not query and 'category' not in request.form:
            return "Please enter a search term or select a category."

        # Filter data by query and selected category (if any)
        if 'category' in request.form:
            category = request.form.get('category')
            if category == 'All':
                filtered_df = df[df['liveStreamer_name'].str.contains(query, na=False)]
            else:
                filtered_df = df[(df['product_interest'] == category) & (df['liveStreamer_name'].str.contains(query, na=False))]
        else:
            filtered_df = df[df['liveStreamer_name'].str.contains(query, na=False)]

        # Check if data is found
        if filtered_df.empty:
            return 'Data not found'

        # Sort data by selected header (if any)
        sort_header = request.form.get('sort')
        if sort_header:
            filtered_df = filtered_df.sort_values(by=sort_header, ascending=False)

        # Convert filtered data to HTML table
        table = filtered_df.to_html(index=False, classes='table table-striped')

        # Return filtered data as HTML string
        return table

    return render_template('SearchFilter.html', title='Search Filter', categories=categories)