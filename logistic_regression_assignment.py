# -*- coding: utf-8 -*-
"""Logistic Regression Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E3KM4dBPWHh6k7oyhi_mG_a9HijjcbgT
"""

import pandas as pd

from google.colab import files
uploaded = files.upload()

df = pd.read_csv('Titanic_train.csv')
df

df.info()

df.describe()

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(16, 10))

# Histogram of numerical variables
plt.subplot(2, 2, 1)
sns.histplot(df['Age'].dropna(), kde=True, bins=30)
plt.title('Distribution of Age')

plt.subplot(2, 2, 2)
sns.histplot(df['Fare'], kde=True, bins=30)
plt.title('Distribution of Fare')

# Box plots for analyzing outliers
plt.subplot(2, 2, 3)
sns.boxplot(x='Pclass', y='Age', data=df)
plt.title('Age distribution across Passenger Classes')

plt.subplot(2, 2, 4)
sns.boxplot(x='Survived', y='Fare', data=df)
plt.title('Fare distribution based on Survival')

plt.tight_layout()
plt.show()

"""**Pattern Observed in Data**


*   Age Distribution: The age distribution is right-skewed with most passengers between 20 and 40 years old. There are some outliers, particularly for passengers aged above 60.

*   Fare Distribution: The fare distribution is heavily right-skewed, with most fares clustered below 100. There are a few extreme outliers where the fare exceeds 500.

*   Age and Passenger Class: Passengers in higher classes (Pclass 1) tend to be older compared to those in lower classes (Pclass 3), where younger passengers are more common.

*   Fare and Survival: Passengers who paid higher fares were more likely to survive, indicating a possible correlation between fare and survival.

"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Handling Missing Values
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df.drop(columns=['Cabin'], inplace=True)

# Encoding Categorical Variables
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df = pd.get_dummies(df, columns=['Embarked'], drop_first=True)
X = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Survived'])
y = df['Survived']
print(X)
print(y)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.4f}')
conf_matrix = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{conf_matrix}')
class_report = classification_report(y_test, y_pred)
print(f'Classification Report:\n{class_report}')

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# Making predictions on the test data
y_pred = logreg.predict(X_test)
y_prob = logreg.predict_proba(X_test)[:, 1]

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1-Score: {f1:.4f}')
print(f'ROC-AUC Score: {roc_auc:.4f}')

# Visualizing the ROC curve
fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

import numpy as np
# Extracting the coefficients
coefficients = logreg.coef_[0]
feature_names = X_train.columns

# Creating a dataframe for easy interpretation
coef_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})
coef_df['Odds Ratio'] = np.exp(coef_df['Coefficient'])  # Convert to odds ratios
coef_df.sort_values(by='Coefficient', ascending=False, inplace=True)

# Displaying the coefficients
print(coef_df)

"""# Discuss the Significance of Features in Predicting Survival:

1.   **Pclass (Passenger Class):**
Lower passenger classes (e.g., 3rd class) are likely to have negative coefficients, meaning passengers in lower classes had a lower probability of survival.

2.   **Sex:**
This is often a significant feature in Titanic datasets. Typically, females (Sex = 1) have a positive coefficient, indicating a higher chance of survival compared to males.

3.   **Age:**
The relationship between age and survival can be complex. Older passengers may have a lower chance of survival (negative coefficient), although this can vary.

4.   **Fare:**
Higher fares may indicate wealthier passengers, often corresponding to a positive coefficient and higher odds of survival.

5.   **SibSp (Number of Siblings/Spouses aboard):**
This could either have a positive or negative coefficient depending on whether having family increased or decreased survival chances.

6.   **Parch (Number of Parents/Children aboard):**
Similarly, having family members may increase the chances of survival, but too many dependents might have reduced survival odds.
"""

import joblib
joblib.dump(logreg, 'titanic_logreg_model.pkl')

import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('titanic_logreg_model.pkl')

# Title of the app
st.title("Titanic Survival Prediction App")

# Subtitle
st.write("Enter the passenger details below to predict survival:")

# User inputs
pclass = st.selectbox("Passenger Class (1 = 1st, 2 = 2nd, 3 = 3rd)", [1, 2, 3])
sex = st.selectbox("Sex (0 = Male, 1 = Female)", [0, 1])
age = st.slider("Age", 0, 80, 25)  # Age between 0 and 80, default 25
sibsp = st.slider("Siblings/Spouses Aboard", 0, 8, 0)  # Number of siblings/spouses aboard
parch = st.slider("Parents/Children Aboard", 0, 6, 0)  # Number of parents/children aboard
fare = st.slider("Fare", 0.0, 500.0, 50.0)  # Fare between 0 and 500, default 50
embarked = st.selectbox("Port of Embarkation (1 = C, 2 = Q, 0 = S)", [0, 1, 2])

# Organize user inputs into a DataFrame
input_data = pd.DataFrame({
    'Pclass': [pclass],
    'Sex': [sex],
    'Age': [age],
    'SibSp': [sibsp],
    'Parch': [parch],
    'Fare': [fare],
    'Embarked_C': [1 if embarked == 1 else 0],
    'Embarked_Q': [1 if embarked == 2 else 0]
})

# Predict survival
if st.button('Predict Survival'):
    prediction = model.predict(input_data)
    survival_probability = model.predict_proba(input_data)[0][1]

    if prediction[0] == 1:
        st.success(f"The passenger is likely to survive! (Probability: {survival_probability:.2f})")
    else:
        st.error(f"The passenger is unlikely to survive. (Probability: {survival_probability:.2f})")