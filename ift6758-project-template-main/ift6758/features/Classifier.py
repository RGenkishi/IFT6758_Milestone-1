from sklearn import linear_model
import numpy as np

class Classifier:
    def __init__(self, dataset):
        self.dataset = dataset
        self.classifier = None

    def train(self):
        self.classifier.fit(self.dataset.x_train, self.dataset.y_train)

    def predict(self, X):
        return self.classifier.predict(X)

    def predict_on_train(self):
        return self.predict(self.dataset.x_train)

    def predict_on_valid(self):
        return self.predict(self.dataset.x_valid)

    def predict_on_test(self):
        return self.predict(self.dataset.x_test)

    def predict_accuracy(self, x, y):
        prediction = self.predict(x)

        return prediction, (prediction == y).sum() / y.shape[0]

    def predict_accuracy_on_train(self):
        return self.predict_accuracy(self.dataset.x_train, self.dataset.y_train)

    def predict_accuracy_on_valid(self):
        return self.predict_accuracy(self.dataset.x_valid, self.dataset.y_valid)

    def predict_accuracy_on_test(self):
        return self.predict_accuracy(self.dataset.x_test, self.dataset.y_test)

    def predict_proba(self, x):
        return self.classifier.predict_proba(x)

    def predict_proba_on_train(self):
        return self.predict_proba(self.dataset.x_train)

    def predict_proba_on_valid(self):
        return self.predict_proba(self.dataset.x_valid)

    def predict_proba_on_test(self):
        return self.predict_proba(self.dataset.x_test)


class LogRegClf(Classifier):
    def __init__(self, dataset):
        super().__init__(dataset)
        self.classifier = linear_model.LogisticRegression()


class RandomClf(Classifier):
    def train(self):
        pass

    def predict(self, X):
        return np.random.randint(low=0, high=2, size=X.shape[0], dtype='int64')

    def predict_proba(self, x):
        return np.random.uniform(low=0.0, high=1.0, size=x.shape[0]*2).reshape((x.shape[0], 2))
