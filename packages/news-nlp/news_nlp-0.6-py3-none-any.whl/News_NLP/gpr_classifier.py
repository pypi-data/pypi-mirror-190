import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from News_NLP.clf_sa import Preprocessing_Clf_SA


def GPR_Clf(data):
    data_train = pd.read_csv('./News_NLP/data/topics_for_classifier_V2.csv',index_col=0)
    data_train.reset_index(drop=True, inplace=True)
    data_train['TDC'] = data_train['title_description_content'].progress_apply(lambda x: Preprocessing_Clf_SA(x))


    df_train, df_test = train_test_split(data_train, test_size = 0.2,random_state = 42)

    X_train, y_train = df_train['TDC'], df_train['target']
    X_test, y_test = df_test['TDC'], df_test['target']


    Max_Features=5400

    # create the transformation matrix
    vectorizer = TfidfVectorizer(max_features=Max_Features)
    # tokenize and build vocabularies
    vectorizer_idf= vectorizer.fit(df_train['TDC'])
    # vectorizer.vocabulary_
    # vectorizer.idf_
    X_train  = vectorizer_idf.transform(df_train['TDC']).toarray()
    news_array  = vectorizer_idf.transform(data['TDC_Clf_SA']).toarray()


    import pickle
    Pkl_Filename = "./News_NLP/model/news_unified_model_V3.pkl"  
    with open(Pkl_Filename, 'rb') as file:  
        Pickled_MLP_Model = pickle.load(file)

    df_pred = pd.DataFrame(Pickled_MLP_Model.predict(news_array),columns=['pred_class'])
    clf_news= pd.concat([data, df_pred],axis=1)
    GPR_News = clf_news.query('pred_class != 0')

    return GPR_News
