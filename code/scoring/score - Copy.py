import pickle
import json
import numpy 
from sklearn.ensemble import RandomForestClassifier
from azureml.core.model import Model

def init():
    global model
    from sklearn.externals import joblib
    # load the model from file into a global object
    model_path = Model.get_model_path(model_name = 'model.pkl')
    model = joblib.load(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)['data']
        data = numpy.array(data)
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})

if __name__ == "__main__":
    # Test scoring
    init()
    test_row = '{"data":[[1,2,3,4,5,6,7,8,9,10],[10,9,8,7,6,5,4,3,2,1]]}'
    prediction = run(test_row)
    print('Test result: ',prediction)