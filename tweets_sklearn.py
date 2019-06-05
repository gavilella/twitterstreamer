from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC


data = []
data_labels = []

with open("./positivo.txt") as file:
    for i in file:
        data.append(i)
        data_labels.append(1)

with open("./negativo.txt") as file:
    for i in file:
        data.append(i)
        data_labels.append(-1)

with open("./neutro.txt") as file:
    for i in file:
        data.append(i)
        data_labels.append(0)

# Vectorizer transforms data into vectors
vectorizer = CountVectorizer(
    analyzer='word',
    lowercase=False,
)
features = vectorizer.fit_transform(
    data
)
features_nd = features.toarray()

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
        features_nd,
        data_labels,
        train_size=.80,
        random_state=1234
)

# Start
log_model = LinearSVC()

# Test
log_model = log_model.fit(X=X_train, y=y_train)

# Predict
y_pred = log_model.predict(X_test)

print(accuracy_score(y_test, y_pred))
# print(vectorizer.fit_transform(['eu sou um amor', 'eu', 'gente']))


features1 = vectorizer.transform(['não quero mais viver'])
pred = log_model.predict(features1)
print(pred)
