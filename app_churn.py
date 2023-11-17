from flask import Flask,request,render_template
import pickle
import xgboost as xgb

model=pickle.load(open('xgboost_model.pkl','rb'))
app=Flask(__name__,template_folder="frontend_churn")
@app.route("/")
def home():
    return render_template("web_page_churn.html")
@app.route("/prediction",methods=['POST','GET'])
def prediction():
    if request.method==["POST"]:
        age=int(request.form['age'])
        joining_date=request.form['date']
        last_visit_time =request.form['time']
        days_since_last_login=int(request.form['last login'])
        avg_time_spent=float(request.form['avg time'])
        avg_transaction_value=float(request.form['transaction'])
        points_in_wallet=float(request.form['points'])
        churn_risk_score=float(request.form['churn'])
        gender=request.form['gender']
        feedback=request.form['feedback']
        internet_option=request.form['internet']
        medium_of_operation=request.form['medium'] 
        joined_through_referral=request.form['reference'] 
        preferred_offer_types =request.form['preference'] 
        membership_category=request.form['membership'] 
        region_category=request.form['region'] 
        used_special_discount=request.form['discount']
        past_complaint=request.form['complaint'] 
        #gender
        if gender=="F":
            Gender=0
        else:
            Gender=1

        #region_category
        if region_category=="Village": 
            Region=2
        elif region_category=="City":
            Region=0
        else:
            Region=1

        #membership
        if membership_category=="Gold Membership":
            Membership=1
        elif membership_category=="Silver Membership":
            Membership=5
        elif membership_category=="Platinum Membership":
            Membership=3
        elif membership_category=="Basic Membership":
            Membership=0
        elif membership_category=="No Membership":
            Membership=2
        else:
            Membership=4

        #preference
        if preferred_offer_types=="Gift Vouchers/Coupons":
            preference=1
        elif preferred_offer_types=="Credit/Debit Card Offers":
            preference=0
        else:
            preference=2

        #feedback
        if feedback=="Products always in Stock":
            Feedback=4
        elif feedback=="Quality Customer Care":
            Feedback=5
        elif feedback=="Poor Website":
            Feedback=3
        elif feedback=="No reason specified":
            Feedback=6
        elif feedback=="Poor Product Quality":
            Feedback=0
        elif feedback=="Poor Customer Service":
            Feedback=1
        else:
            Feedback=2

        #used_special_discount
        if used_special_discount=="Yes":
            discount=1
        else:
            discount=0

        #past_complaint
        if past_complaint=="Yes":
            complaint=1
        else:
            complaint=0

        #joined_through_referral
        if joined_through_referral=="Yes":
            reference=2
        elif joined_through_referral=="No":
            reference=0
        else:
            reference=1

        #internet_option
        if internet_option=="Wi-Fi":
            internet=2
        elif internet_option=="Mobile_Data":
            internet=1
        else:
            internet=0

        #medium_of_operation
        if medium_of_operation=="Desktop":
            medium=2
        elif medium_of_operation=="Smartphone":
            medium=3
        elif medium_of_operation=="Both":
            medium=1
        else:
            medium=0

        d=joining_date.split("-")
        year=int(d[0])
        month=int(d[1])
        day=int(d[2])

        t=last_visit_time.split(":")
        hour=int(t[0])
        minute=int(t[1])
        second=int(t[2])

        data={"age":[age],"days_since_last_login":[days_since_last_login],"avg_time_spent":[avg_time_spent],"avg_transaction_value":
              [avg_transaction_value],"points_in_wallet":[points_in_wallet],"churn_risk_score":[churn_risk_score],"Gender":[Gender],
              "Region":[Region],"Membership":[Membership],"preference":[preference],"reference":[reference],"medium":[medium],
              "internet":[internet],"discount":[discount],"complaint":[complaint],"Feedback":[Feedback],"year":[year],"month":
              [month],"day":[day],"hour":[hour],"min":[minute],"sec":[second]}
        
        import pandas as pd
        df=pd.DataFrame.from_dict(data)
        prediction=model.predict(df)
        
        
        return render_template("prediction.html",prediction_text="Churn score is {}".format(prediction))
    else:
        return render_template("prediction.html")


@app.route("/analysis")
def analysis():
    return render_template("churn.html")
if __name__=="__main__":
    app.run(debug=True)



