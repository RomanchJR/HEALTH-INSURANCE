from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('InsuranceCost.pkl','rb'))
@app.route('/',methods=["GET"])
def Home():
	return render_template('insuranceprice.html')

standard_to = StandardScaler()
@app.route('/predict',methods=["POST"])
def predict():
	if request.method=="POST":
		age = int(request.form["Age"])
		bmi = float(request.form["BMI"])
		children = int(request.form["Children"])
		sex_male = str(request.form["Sex"])
		if(sex_male=="M"):
			sex_male=1
		else:
			sex_male=0
		smoker_yes = str(request.form["Smoker"])
		if(smoker_yes=="yes"):
			smoker_yes=1
		else:
			smoker_yes=0
		region = str(request.form["Region"])
		if(region=="Northwest"):
			region_northeast=0
			region_northwest=1
			region_southeast=0
			region_southwest=0
		elif(region=="Southeast"):
			region_northeast=0
			region_northwest=0
			region_southeast=1
			region_southwest=0
		elif(region=="Southwest"):
			region_northeast=0
			region_northwest=0
			region_southeast=0
			region_southwest=1
		else:
			region_northeast=1
			region_northwest=0
			region_southeast=0
			region_southwest=0

		input_features = [age, bmi, children, sex_male, smoker_yes, region_northwest, region_southeast, region_southwest]
		input_feat=[np.array(input_features)]
		prediction = model.predict(input_feat)
		output = round(prediction[0],2)
		if output<0:
			return render_template('insuranceprice.html',prediction_text="Sorry price can not be negative")
		else:
			return render_template('insuranceprice.html',prediction_text="Predicted insurance cost for this person is {}".format(output))
	else:
		return render_template('insuranceprice.html')
if __name__=="__main__":
	app.run(debug=True)