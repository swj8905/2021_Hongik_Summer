from sklearn.svm import SVC
import pandas as pd
from sklearn.metrics import accuracy_score

df_train = pd.read_csv("./mnist/train.csv")
df_test = pd.read_csv("./mnist/t10k.csv")

train_label = df_train.iloc[:, 0]
train_data = df_train.iloc[:, 1:]
test_label = df_test.iloc[:, 0]
test_data = df_test.iloc[:, 1:]

model = SVC()
model.fit(train_data, train_label)

result = model.predict(test_data)
score = accuracy_score(result, test_label)
print(score)

# 학습한 모델 저장
import pickle
f = open("./mnist_model.pkl", "wb")
pickle.dump(model, f)
f.close()