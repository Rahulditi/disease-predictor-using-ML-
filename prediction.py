import requests
import json
import warnings
import sys
import pandas as pd
import pickle

def predict_disease(symptoms):
    df = pd.DataFrame(symptoms, index=[0])

    warnings.filterwarnings("ignore")

   
    with open('./models/diseasepredictor.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

  
    prediction = model.predict(df)

    
    with open('./models/predictonlabeler.pkl', 'rb') as model_label:
        label = pickle.load(model_label)

 
    predicted_disease = label.inverse_transform(prediction)

    return predicted_disease[0]

def search_wikipedia(disease):

    response = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={disease}&redirects=1")
    data = response.json()
    
   
    page_id = list(data['query']['pages'].keys())[0]
    if page_id != '-1':
        wikipedia_url = f"https://en.wikipedia.org/?curid={page_id}"
        return wikipedia_url
    else:
        return None

def main(symptoms):
    
    predicted_disease = predict_disease(symptoms)
    
    
    wikipedia_url = search_wikipedia(predicted_disease)
    
    
    return [predicted_disease,wikipedia_url]

if __name__ == "__main__":
    symptoms = json.loads(sys.argv[1])
    result = main(symptoms)
    print(json.dumps(result))
