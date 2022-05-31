from flask import Blueprint, redirect , render_template , request
import pickle

auth = Blueprint('auth',__name__)

user = False


@auth.route('/admin')
def admin():
    global user
    if user == True:
           return render_template('predict.html' , proba_in_str = "0.00" , deg = "0.00")
    return redirect('/signin')
 

@auth.route('/signin' , methods=['GET','POST'])
def signin():
    global user
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123':
            user = True
            return redirect('predict')
    if request.method == 'GET' and user == True :
            return redirect('predict')
    return render_template('signin.html')
    
@auth.route('/logout')
def logout():
    global user
    user = False
    return redirect('/signin')


@auth.route('/predict')
def predict():
    global user
    if user == True:
           return render_template('predict.html' , prob_in_str = "0.00" ,deg = "0.00")
    return redirect('/signin')

@auth.route('/predict',methods=['GET' , 'POST'])
def predict_prob():
    

    model = pickle.load(open('model/model.sav' , 'rb'))

    
    
    dp = request.form.get('dp')
    ob = request.form.get('ob')
    st = request.form.get('st')
    sm = request.form.get('sm')
    ts = request.form.get('ts')
    os = request.form.get('os')
    ins = request.form.get('ins')
    pm = request.form.get('pm')
    c = request.form.get('c')
    t = request.form.get('t')
    mc = request.form.get('mc')
    tc= request.form.get('tc')


    features = [dp , ob , st , sm , ts , os , ins , pm , c , t , mc , tc]
    
    
    for f in features:
        if f == None:
            return render_template('predict.html'  , error = "Invalid Customer Data" ,deg = "0.00")
            
            
    try:
        DeviceProtection_No = 1 if dp == '1' else 0
        OnlineBackup_No = 1 if ob == '1' else 0
        StreamingTV_No_internet_service = 1 if st == '3' else 0
        StreamingMovies_No_internet_service = 1 if sm == '3' else 0
        TechSupport_No_internet_service = 1 if ts == '3' else 0
        DeviceProtection_No_internet_service = 1 if dp == '3' else 0
        OnlineBackup_No_internet_service = 1 if ob == '3' else 0
        OnlineSecurity_No_internet_service = 1 if os == '3' else 0
        InternetService_No = 1 if ins == '1' else 0

        tenure_group_61_72 = 1 if int(t) >=61 and int(t) <= 72 else 0

        PaymentMethod_Electronic_check = 1 if pm == '1' else 0
        InternetService_Fiber_optic = 1 if ins == '3' else 0
        TechSupport_No = 1 if ts == '1' else 0
        OnlineSecurity_No = 1 if os == '1' else 0
        Contract_Two_year = 1 if c == '3' else 0

        tenure_group_1_12 = 1 if int(t) >=1 and int(t) <= 12 else 0

        Contract_Month_to_month = 1 if c == '1' else 0

        MonthlyCharges = ( float(mc) - 64.79820819 ) / 30.08383459

        TotalCharges = ( float(mc) - 2283.30044084 ) / 2266.61018071
    except ValueError:
        return render_template('predict.html'  , prob_in_str = "0.00" , error = "Invalid Customer Data" ,deg = "0.00")
    
        
    
    


    prob = model.predict_proba([[DeviceProtection_No, OnlineBackup_No, StreamingTV_No_internet_service, StreamingMovies_No_internet_service, TechSupport_No_internet_service, DeviceProtection_No_internet_service, OnlineBackup_No_internet_service, OnlineSecurity_No_internet_service, InternetService_No, tenure_group_61_72, PaymentMethod_Electronic_check, InternetService_Fiber_optic, TechSupport_No, OnlineSecurity_No, Contract_Two_year, tenure_group_1_12, Contract_Month_to_month, MonthlyCharges, TotalCharges]])[0][1]*100
    prob_in_str = "{:.2f}".format(prob)

    deg = (prob * 180 ) / 100

    return render_template('predict.html' , prob = prob , prob_in_str = prob_in_str, deg = deg)


@auth.route('/csv')
def csv():
    global user
    if user == True:
           return render_template('csv.html')
    return redirect('/signin')