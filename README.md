# Agricultural-Commodity-Price-Prediction-using-Machine-Learning
The primary objective of this project is to develop and deploy a machine learning model 
capable of precisely predicting the modal price of key agricultural commodities prevalent in 
markets of Rajasthan, India, specifically Bajra, Barley, Groundnut, Guar, Onion, Potato, 
Soyabean, and Tomato.

Historical market data underwent a rigorous preprocessing phase involving data cleaning and 
an iterative Interquartile Range (IQR) method for outlier removal, resulting in a refined dataset 
for model training. Categorical features, encompassing geographical, product, and temporal 
aspects, were transformed into numerical representations using label encoding, with 
corresponding mapping dictionaries preserved for future application.  

A Random Forest Regressor was selected as the predictive model and trained on the prepared 
data, achieving a robust R-squared score of approximately 0.88 on unseen test data, indicating 
a strong predictive capability. 
