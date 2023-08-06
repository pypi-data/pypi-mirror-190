# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['News_NLP']

package_data = \
{'': ['*'], 'News_NLP': ['data/*', 'model/*']}

install_requires = \
['newsapi-python>=0.2.6,<0.3.0', 'nltk>=3.8.1,<4.0.0', 'spacy>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'news-nlp',
    'version': '0.6',
    'description': 'This package aims to collect news data via Google News API, preporcessing, implement pretrained news type classifer and sentiment classifier and perform predictive model for news event and then implememnt multiple geolocator.',
    'long_description': '\n<!-- ![](/home/jason/Documents/data/newplot.png) -->\n# News NLP for Global Geopolitical Risk\n===========================\n\nThis is a simple Python client for the news NLP.\n\nUsage\n-----\nFirst install it\n\n```\npip install News_NLP\n```\n\nThen instantiate and use it like this:\n\n```python\nimport News_NLP\nfrom News_NLP.GNews import GNews\nfrom News_NLP.preprocessing import Preprocessing_Clf_SA, Preprocessing_GEO,Combine_Col\nfrom News_NLP.gpr_classifier import GPR_Clf\nfrom News_NLP.sentiment_clf import Sen_Clf\nfrom News_NLP.geolocator import Get_CSC_Prob, CSC_Prob\n```\n\n* Fetch news articles from Google News API, `from News_NLP.GNews import GNews`,\n* Preproces news data for sentiment analysis and news type classifier, `from News_NLP.preprocessing import Preprocessing_Clf_SA`\n* Preproces news data for multiple-geolocator `from News_NLP.preprocessing import Preprocessing_GEO`,\\\n* Implement pretrained deep leanring model to caterise news article `from News_NLP.gpr_classifier import GPR_Clf`,\\\n* Perform sentiment classifier `from News_NLP.sentiment_clf import Sen_Clf`,\\\n* Implement multiple geolocator `form News_NLP.geolocator import Get_CSC_Prob, CSC_Prob`,\n\nFor a demenstration see `https://github.com/HigherHoopern/News_NLP`\n\n',
    'author': 'Jason Lu',
    'author_email': 'luzhenxian@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
