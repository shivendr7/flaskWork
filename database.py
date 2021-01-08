import pickle
with open('model_pickle','rb') as f:
    model=pickle.load(f)
    print(model.predict([[5]]))