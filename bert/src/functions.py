# for NLP
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
STOP_WORDS = stopwords.words('english')
lemmatizer = WordNetLemmatizer() 

# for model eval
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, plot_confusion_matrix

def text_cleaner_for_non_BERT(text):  
    
    # lower chars and treat whitespaces
    text = text.lower()
    text = re.compile('\s+').sub(' ', text) # whitespaces
    text = text.strip() # trailing whitespaces  

    # delete special characters and numbers
    text = re.compile('[^a-z]').sub(' ', text) 
    
    # after numbers
    text = re.sub(' th ', '', text)
    text = re.sub(' st ', '', text)
    text = re.sub(' nd ', '', text)
    text = re.compile('\s+').sub(' ', text) # whitespaces
    text = re.compile('\s+').sub(' ', text) # whitespaces
    text = text.strip() # trailing whitespaces 
    
    # stopwords
    text = ' '.join([word for word in text.split() if word not in STOP_WORDS])
    
    # lemmatization
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    
    # final whitespace treatment
    text = re.compile('\s+').sub(' ', text) # whitespaces
    text = text.strip() # trailing whitespaces 
    
    return text


def text_cleaner_for_BERT(text):  
    
    # lower chars and treat whitespaces
    text = text.lower()
    text = re.compile('\s+').sub(' ', text) # whitespaces
    text = text.strip() # trailing whitespaces  
    
    # remove spec chars except apostrophe
    text = re.sub(r"[^\w\d'\s]+", '', text)
    
    return text

def evaluate_text_class_predictions(y_true, model, prediction_data, model_name: str, 
                                    neural_net = False, 
                                    neural_net_pred_dict = {0 : 'Biology', 1 : 'Physics', 2 : 'Chemistry'}):
    
    if neural_net == True:
        predictions_raw = model.predict(prediction_data).argmax(axis=-1)
        predictions_classes = list(map(neural_net_pred_dict.get, predictions_raw))
        accuracy = accuracy_score(y_true, predictions_classes)
        class_report = classification_report(y_true, predictions_classes)
        
    else:
        accuracy = accuracy_score(y_true, model.predict(prediction_data))
        class_report = classification_report(y_true, model.predict(prediction_data))
    
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.rcParams.update({'font.size': 12})
        plt.title('Classification report for ' + model_name + '\n')
        plot_confusion_matrix(model, prediction_data, y_true, ax = ax, cmap = 'Greys')
        plt.show()
    
    return accuracy, class_report