from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
import numpy as np

#Code by: Nizar Talty

def processFit(X, Y, features):
    model = LinearRegression().fit(X[list(features)], Y)
    y_pred = model.predict(X[list(features)])
    #computing the RSS
    scoreRss  = np.sum(np.square(y_pred - Y))
    
    return (model, scoreRss, features)

#==========================================================#

#forward is initialized as Null(feature is set to empty list)
def forward(X, Y, predictors):
    remaining_predictors = [p for p in X.columns if p not in predictors]
    result = []
    
    for predictor in remaining_predictors:
        result.append(processFit(X, Y, predictors + [predictor]))
    
    best_score = None
    best_model = None
    best_feature = None
    
    for i in result:
        #We are using the RSS so we should select the model with the smallest RSS
        if best_score is None or i[1] < best_score:
            best_score = i[1]
            best_model = i[0]
            best_feature = i[2]
            
    return best_model, best_feature, best_score

#==========================================================#

def get_all_models(X, Y, n_iteration=None, algorithm=None, features=None):
    #Setting the number of iterations to a default value
    if n_iteration is None:
        n_iteration = len(X.columns)
        
    if algorithm is None:
        algorithm = 'forward'
    
    if algorithm == 'forward':
        current_features = []
        best_models = []
        for i in range(n_iteration):
            mod = forward(X, Y, current_features)
            current_features = mod[1]
            best_models.append((mod[0], mod[2], mod[1]))
            
    if algorithm == 'backward':
        current_features = features
        best_models = []
        while n_iteration > 1:
            mod = backward(X, Y, current_features)
            #print(mod)
            current_features = mod[1]
            #print(current_features)
            best_models.append((mod[0], mod[2], mod[1]))
            n_iteration -= 1
        
    return best_models

#==========================================================#

def validate_best_model(models, data, target):
    
    op_score = None
    optimal_model = None
    optimal_features = None
    
    for model in models:
        cross_v_score = cross_validate(model[0], data[model[2]], data[target], scoring='r2', cv=5)
        cross_v_mean = cross_v_score['test_score'].mean()
        
        if op_score is None or cross_v_mean > op_score:
            op_score = cross_v_mean
            optimal_model = model
            optimal_features = model[1]
    return optimal_features, op_score, optimal_model

#==========================================================#

def create_back_combos(predictors):
    result = []
    for elem in predictors:
        copy_list = predictors.copy()
        copy_list.remove(elem)
        result.append(copy_list)
    return result

def backward(X, Y, predictors):
    
    #Starting from a full model
    if predictors == [] or predictors is None or len(predictors) == 1:
        print('[Error]: Wrong predictors input')
        return -1
    
    result = []
    for possible_feature in create_back_combos(predictors):
        result.append(processFit(X, Y, possible_feature))
        
    best_score = None
    best_model = None
    best_feature = None
    
    for i in result:
        #We are using the RSS so we should select the model with the smallest RSS
        if best_score is None or i[1] < best_score:
            best_score = i[1]
            best_model = i[0]
            best_feature = i[2] 
    
    return best_model, best_feature, best_score