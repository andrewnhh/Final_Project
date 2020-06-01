from flask import Flask, render_template, url_for, request, send_from_directory
import numpy as np
import pandas as pd
import folium
import joblib

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route('/storage/<path:x>')
def storage(x):
    return send_from_directory("storage", x)

@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        input = request.form
        #Gender
        gender = input["gender"]
        strGender = ""
        if gender == "m":
            gen = 1
            strGender = "Male"
        elif gender == "f":
            gen = 0
            strGender = "Female"
        #Maried
        MaritalStatus = input["MaritalStatus"]
        strMarital = ""
        if MaritalStatus == "y":
            mar = 1
            div = 0
            sngl = 0
            strMarital = "Married"
        elif MaritalStatus == "n":
            mar = 0
            div = 0
            sngl = 1
            strMarital = "Single"
        else:
            mar = 0
            div = 1
            sngl = 0
            strMarital = "Divorced"
        #OverTime
        OverTime = input["OverTime"]
        strOvt = ""
        if OverTime == "y":
            ovt = 1
            strOvt = "Yes"
        else:
            ovt = 0
            strOvt = "No"
        #BusinessTravel
        travel = input["travel"]
        strTravel = ""
        if travel == "rarely":
            rare = 1
            freq = 0
            non = 0
            strTravel = "Travel Rarely"
        elif travel == "frequently":
            rare = 0
            freq = 1
            non = 0
            strTravel = "Travel Frequently"
        else:
            rare = 0
            freq = 0
            non = 1
            strTravel = "Non Travel"
        #JobRole
        JobRole = input["JobRole"]
        strRole = ""
        if JobRole == "se":
            se = 1
            rs = 0
            lt = 0
            md = 0
            hrep = 0
            man = 0
            sr = 0
            rd = 0
            hr = 0
            strRole = "Sales Executive"
        elif JobRole == "rs":
            se = 0
            rs = 1
            lt = 0
            md = 0
            hrep = 0
            man = 0
            sr = 0
            rd = 0
            hr = 0
            strRole = "Research Scientist"
        elif JobRole == 'lt':
            se = 0
            rs = 0
            lt = 1
            md = 0
            hrep = 0
            man = 0
            sr = 0
            rd = 0
            hr = 0
            strRole = "Laboratory Technician"
        elif JobRole == 'md':
            se = 0
            rs = 0
            lt = 0
            md = 1
            hrep = 0
            man = 0
            sr = 0
            rd = 0
            hr = 0
            strRole = "Manufacturing Director"
        elif JobRole == 'hrep':
            se = 0
            rs = 0
            lt = 0
            md = 0
            hrep = 1
            man = 0
            sr = 0
            rd = 0
            hr = 0
            strRole = "Healthcare Representative"
        elif JobRole == 'man':
            se = 0
            rs = 0
            lt = 0
            md = 0
            hrep = 0
            man = 1
            sr = 0
            rd = 0
            hr = 0
            strRole = "Manager"
        elif JobRole == 'sr':
            se = 0
            rs = 0
            lt = 0
            md = 0
            hrep = 0
            man = 0
            sr = 1
            rd = 0
            hr = 0
            strRole = "Sales Representative"
        elif JobRole == 'rd':
            se = 0
            rs = 0
            lt = 0
            md = 0
            hrep = 0
            man = 0
            sr = 0
            rd = 1
            hr = 0
            strRole = "Research Director"
        else:
            se = 0
            rs = 0
            lt = 0
            md = 0
            hrep = 0
            man = 0
            sr = 0
            rd = 0
            hr = 1
            strRole = "Human Resources"
        #Department
        Department = input["Department"]
        strDept = ""
        if Department == "sales":
            sales = 1
            rdev = 0
            h_r = 0
            strDept = "Sales"
        elif Department == "rdev":
            sales = 0
            rdev = 1
            h_r = 0
            strDept = "Research & Development"
        else:
            sales = 0
            rdev = 0
            h_r = 1
            strDept = "Human Resources"
        #EduField
        EducationField = input["EducationField"]
        strEduField = ""
        if EducationField == "1":
            lisi = 1
            mrkt = 0
            tec = 0
            humres = 0
            med = 0
            otr = 0
            strEduField = "Life Sciences"
        elif EducationField == "2":
            lisi = 0
            mrkt = 1
            tec = 0
            humres = 0
            med = 0
            otr = 0
            strEduField = "Marketing"
        elif EducationField == "3":
            lisi = 0
            mrkt = 0
            tec = 1
            humres = 0
            med = 0
            otr = 0
            strEduField = "Technical Degree"
        elif EducationField == "4":
            lisi = 0
            mrkt = 0
            tec = 0
            humres = 1
            med = 0
            otr = 0
            strEduField = "Human Resources"
        elif EducationField == "5":
            lisi = 0
            mrkt = 0
            tec = 0
            humres = 0
            med = 1
            otr = 0
            strEduField = "Medical"
        else:
            lisi = 0
            mrkt = 0
            tec = 0
            humres = 0
            med = 0
            otr = 1
            strEduField = "Other"
        #JobInv
        jobinv = input["jobinv"]
        strJobinv = ""
        if jobinv == "1":
            job_inv = 1
            strJobinv = "Low"
        elif jobinv == "2":
            job_inv = 2
            strJobinv = "Medium"
        elif jobinv == "3":
            job_inv = 3
            strJobinv = "High"
        else:
            job_inv = 4
            strJobinv = "Very High"
        #PerfRate
        Performance = input["Performance"]
        strPerf = ""
        if Performance == "1":
            perf_rate = 1
            strPerf = "Low"
        elif Performance == "2":
            perf_rate = 2
            strPerf = "Good"
        elif Performance == "3":
            perf_rate = 3
            strPerf = "Excellent"
        else:
            perf_rate = 4
            strPerf = "Outstanding"
        #LifeBalance
        Balance = input["Balance"]
        strLife = ""
        if Balance == "1":
            life_bal = 1
            strLife = "Low"
        elif Balance == "2":
            life_bal = 2
            strLife = "Good"
        elif Balance == "3":
            life_bal = 3
            strLife = "Better"
        else:
            life_bal = 4
            strLife = "Best"
        #Education
        Education = input["Education"]
        strEdu = ""
        if Education == "1":
            educ = 1
            strEdu = "Low"
        elif Education == "2":
            educ = 2
            strEdu = "Good"
        elif Education == "3":
            educ = 3
            strEdu = "Better"
        else:
            life_bal = 4
            strEdu = "Best"
        #EnvSatisfaction
        Environment = input["Environment"]
        strEnv = ""
        if Environment == "1":
            env_sat = 1
            strEnv = "Low"
        elif Environment == "2":
            env_sat = 2
            strEnv = "Medium"
        elif Environment == "3":
            env_sat = 3
            strEnv = "High"
        else:
            env_sat = 4
            strEnv = "Very High"
        #RelationshipSatisfaction
        Relationship = input["Relationship"]
        strRelation = ""
        if Relationship == "1":
            rel_sat = 1
            strRelation = "Low"
        elif Relationship == "2":
            rel_sat = 2
            strRelation = "Medium"
        elif Relationship == "3":
            rel_sat = 3
            strRelation = "High"
        else:
            rel_sat = 4
            strRelation = "Very High"
        #JobSatisfaction
        JobSatisfaction = input["JobSatisfaction"]
        strJobSat = ""
        if JobSatisfaction == "1":
            job_sat = 1
            strJobSat = "Low"
        elif JobSatisfaction == "2":
            job_sat = 2
            strJobSat = "Medium"
        elif JobSatisfaction == "3":
            job_sat = 3
            strJobSat = "High"
        else:
            job_sat = 4
            strJobSat = "Very High"
        #Age
        age = int(input["age"])
        if age <= 20:
            age_cat = 1
        elif age > 20 or age <=30:
            age_cat = 2
        elif age > 30 or age <=40:
            age_cat = 3
        elif age > 40 or age <=50:
            age_cat = 4
        else:
            age_cat = 5
        #Distance
        dist = int(input["Distance"])
        if dist <= 10:
            dist_cat = 1
        elif dist > 10 or dist <=20:
            dist_cat = 2
        else:
            dist_cat = 3
        #DailyRate
        day_rate = int(input["DailyRate"])
        #HourlyRate
        hour_rate = int(input["HourlyRate"])
        #MonthlyIncome
        mth_in = int(input["MonthlyIncome"])
        #MonthlyRate
        mth_rate = int(input["MonthlyRate"])
        #salaryhike
        sal_hike = int(input["salaryhike"])
        #Stock
        stock = int(input["Stock"])
        #TotalWorkYears
        ttlwork = int(input["ttlwork"])
        #Training Times Last Year
        train_time = int(input["traintime"])
        #YearsAtCompany
        years_at = int(input["YearsAtCompany"])
        #Years SinceLast Promotion
        lastpromo = int(input["lastpromo"])
        #Years With Curr Manager
        currmanager = int(input["currmanager"])
        #JobLevel
        job_lvl = int(input["JobLvl"])
        # Years Current Role
        currrole = int(input["currrole"])
        #Num Company Work
        companywork = int(input["companywork"])
        
        
        #Result
        datainput = [[ gen, mar, div, sngl, educ, ovt, rare, freq, non, se,  rs,  lt,  md,  hrep,  man,  sr,  rd,  hr, sales, rdev, h_r, lisi, mrkt, tec, humres, med, otr, job_inv, perf_rate, life_bal, env_sat, rel_sat, job_sat, age_cat, dist_cat, day_rate, hour_rate, mth_in, mth_rate, sal_hike, stock, ttlwork, train_time, years_at, lastpromo, currmanager, job_lvl, currrole, companywork]]
        pred = model.predict(datainput)[0]
        proba = model.predict_proba(datainput)[0]
        if pred == 0:
            prbb = round((proba[0]*100), 1)
            rslt = "No Attrition"
        else:
            prbb = round((proba[1]*100), 1)
            rslt = "Attrition"
        return render_template(
            "result.html", gender= strGender, age= age, travel= strTravel, JobRole= strRole, OverTime=strOvt, Department= strDept, MaritalStatus = strMarital, EducationField= strEduField, jobinv= strJobinv, Balance= strLife, Education=strEdu, Environment=strEnv, Relationship=strRelation, JobSatisfaction=strJobSat, dist=dist, DailyRate=day_rate, HourlyRate=hour_rate, MonthlyIncome=mth_in, MonthlyRate=mth_rate, JobLvl=job_lvl, salaryhike=sal_hike, Stock=stock, ttlwork=ttlwork, traintime=train_time, YearsAtCompany=years_at, lastpromo=lastpromo, currmanager=currmanager, companywork=companywork, Performance=strPerf, result= rslt, proba = prbb
        )


if __name__ == "__main__":
    model = joblib.load("modelML")
    app.run(debug=True, port=5050)