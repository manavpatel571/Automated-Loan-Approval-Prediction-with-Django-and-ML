from django.shortcuts import render
from . models import approvals
from . serializers import approvalsSerializers
from rest_framework import viewsets
from . form import ApprovalForm
from tensorflow.keras.models import load_model


#from . forms import MyForm
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
import pickle
import joblib
import json
import numpy as np
import pandas as pd
from django.contrib import messages
from keras import backend as K
import tensorflow
from keras import backend as K


# Create your views here.
class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers

# one hot encoding
def ohevalue(df):
	ohe_col=joblib.load("myapp1/allcol.pkl")
	cat_columns=['Gender','Married','Education','Self_Employed','Property_Area']
	df_processed = pd.get_dummies(df, columns=cat_columns)
	newdict={}
	for i in ohe_col:
		if i in df_processed.columns:
			newdict[i]=df_processed[i].values
		else:
			newdict[i]=0
	newdf=pd.DataFrame(newdict)
	return newdf

def approvereject(unit):
	try:
		mdl = load_model("F:/Projects/Loan Approval/DjangoAPI/myapp1/loan_model.h5")
		#mdl=joblib.load("F:/Projects/Loan Approval/DjangoAPI/myapp1/loan_model.pkl")
		scalers=joblib.load("F:/Projects/Loan Approval/DjangoAPI/myapp1/scalers.pkl")
		X=scalers.transform(unit)
		y_pred=mdl.predict(X)
		y_pred=(y_pred>0.58)
		newdf=pd.DataFrame(y_pred, columns=['Status'])
		newdf=newdf.replace({True:'Approved', False:'Rejected'})
		K.clear_session()
		return newdf.values[0][0]
		#return (newdf.values[0][0],X[0])
	except ValueError as e:
		return (e.args[0])


def cxcontact(request):
	if request.method=='POST':
		form=ApprovalForm(request.POST)
		if form.is_valid():
				Firstname = form.cleaned_data['firstname']
				Lastname = form.cleaned_data['lastname']
				Dependents = form.cleaned_data['Dependents']
				ApplicantIncome = form.cleaned_data['ApplicantIncome']
				CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
				LoanAmount = form.cleaned_data['LoanAmount']
				Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
				Credit_History = form.cleaned_data['Credit_History']
				Gender = form.cleaned_data['Gender']
				Married = form.cleaned_data['Married']
				Education = form.cleaned_data['Education']
				Self_Employed = form.cleaned_data['Self_Employed']
				Property_Area = form.cleaned_data['Property_Area']
				myDict = (request.POST).dict()
				df=pd.DataFrame(myDict, index=[0])
				#print(approvereject(ohevalue(df)))
				answer = approvereject(ohevalue(df))
				#Xscalers=approvereject(ohevalue(df))[1]
				if int(df['LoanAmount'])<25000:
					messages.success(request,'Application Status: {}'.format(answer))
				else:
					messages.success(request,'Invalid: Your Loan Request Exceeds $25,000 Limit')
	
	form=ApprovalForm()
				
	return render(request, 'myform/cxform.html', {'form':form})

def cxcontact2(request):
	if request.method=='POST':
		form=ApprovalForm(request.POST)
		if form.is_valid():
				Firstname = form.cleaned_data['firstname']
				Lastname = form.cleaned_data['lastname']
				Dependents = form.cleaned_data['Dependents']
				ApplicantIncome = form.cleaned_data['ApplicantIncome']
				CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
				LoanAmount = form.cleaned_data['LoanAmount']
				Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
				Credit_History = form.cleaned_data['Credit_History']
				Gender = form.cleaned_data['Gender']
				Married = form.cleaned_data['Married']
				Education = form.cleaned_data['Education']
				Self_Employed = form.cleaned_data['Self_Employed']
				Property_Area = form.cleaned_data['Property_Area']
				myDict = (request.POST).dict()
				df=pd.DataFrame(myDict, index=[0])
				answer=approvereject(ohevalue(df))[0]
				Xscalers=approvereject(ohevalue(df))[1]
				messages.success(request, 'Application Status: {}'.format(answer[0]))


	
	form=ApprovalForm()
				
	return render(request, 'myform/form.html', {'form':form})