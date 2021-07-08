from sklearn.datasets import load_iris
import joblib
from sklearn.svm import SVC

iris = load_iris()
data = iris.data
label = iris.target

model = SVC()
model.fit(data, label)
# 모델 저장하기
joblib.dump(model, "model.pkl")