from django.shortcuts import render,redirect
from userapp.models import User
from adminapp.models import Dataset
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
import math
from django.contrib import messages
from imblearn.over_sampling import SMOTE


# Create your views here.


def index(request):
    t_users = User.objects.all()
    a_users = User.objects.filter(status="Accepted")
    p_users = User.objects.filter(status="Verified")
    context ={
        't_users':len(t_users),
        'a_users':len(a_users),
        'p_users':len(p_users),

    }
    return render(request,'admin/index.html',context)






def attacks_analysis(request):
    # datasets = Dataset.objects.all()
    # data_list = []
    # for dataset in datasets:
    #     df = pd.read_csv(dataset.file)
    #     protocol_counts = df['Attack Type'].value_counts()
    #     normal = protocol_counts.get('normal', 0)
    #     print(normal)
    #     dos = protocol_counts.get('dos', 0)
    #     print(dos)
    #     probe = protocol_counts.get('probe', 0)
    #     print(probe)
    #     r2l = protocol_counts.get('r2l', 0)
    #     print(r2l)
    #     u2r = protocol_counts.get('u2r', 0)
    #     print(u2r)

    #     data_list.append({
    #         'title': dataset.title,
    #         'normal': normal,
    #         'dos': dos,
    #         'probe': probe,
    #         'r2l': r2l,
    #         'u2r': u2r,

    #     })

    return render(request, 'admin/attacks-analysis.html')







def upload_dataset(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file') 
        if csv_file:
            Dataset.objects.all().delete()
            dataset = Dataset(title=csv_file.name, file=csv_file)
            dataset.save()
            return redirect('view_dataset')
    return render(request,'admin/upload-dataset.html')



def view_dataset(request):
    datasets = Dataset.objects.all()
    data_list = []
    
    for dataset in datasets:
        df = pd.read_csv(dataset.file)
        # df = df.head(1000)
        data = df.to_html(index=False)
        data_list.append({
            'title': dataset.title,
            'data': data
        })
        dataset.save()
    return render(request,'admin/view-dataset.html',{'data_list': data_list})


def alg4(request):
    dataset = Dataset.objects.first()  
    df = pd.read_csv(dataset.file)
    target_column = "status"  
    y = df['status']
    X = df.drop(columns=['status'])
    ros = SMOTE()
    X , y =  ros.fit_resample(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logreg_model = LogisticRegression() 
    logreg_model.fit(X_train, y_train)
    y_pred = logreg_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    request.session['LogisticRegression_accuracy'] = accuracy  
    metrics_data = {
        'algorithm': 'LogisticRegression',
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
    }
    context = {
        'dataset_title': dataset.title,
        'target_column': target_column,
        'metrics_data': metrics_data,
    }
    return render(request,'admin/algorithm-four.html',context)
















