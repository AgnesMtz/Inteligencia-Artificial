from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

#Cargar el dataset Iris (Modelo)
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#####Maximo de iteraciones
mlp = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=500, random_state=42)

#Hace predicciones
mlp.fit(X_train, y_train) #Entrena el modelo

#Evalua el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'nPrecisión en test: {accuracy:.4f}')

