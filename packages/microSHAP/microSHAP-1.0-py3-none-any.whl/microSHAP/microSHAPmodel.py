def microSHAP(dataset):

    import xgboost
    import shap
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    data = dataset

    from sklearn.preprocessing import LabelEncoder

    encoder = LabelEncoder()
    print(data['Condition'])
    data['Condition'] = encoder.fit_transform(data['Condition'])

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    # create a train/test split
    # train XGBoost model
    model = xgboost.XGBClassifier().fit(X, y)

    # compute SHAP values
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    return shap_values
