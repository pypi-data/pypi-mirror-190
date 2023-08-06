# Redes Bayesianas

Una librería para construir redes bayesianas y realizar inferencia probabilística.

## Instalación

Con el manejador de paquetes pip:

- **pip install bayesian-networks-rey20074**

## Uso

<sub> 
    
    # importa la libreria
    from bayesian_networks_rey20074 import BayesianNetwork

    # crea los nodos de la red
    node_b = BayesianNetwork.Node('b', 0.001)

    node_e = BayesianNetwork.Node('e', 0.002)

    node_a = BayesianNetwork.Node('a', multiple_parents=True)
    node_a.add_connection_multiple_parents({'b': True, 'e': True}, 0.95)
    node_a.add_connection_multiple_parents({'b': True, 'e': False}, 0.94)
    node_a.add_connection_multiple_parents({'b': False, 'e': True}, 0.29)
    node_a.add_connection_multiple_parents({'b': False, 'e': False}, 0.001)
    node_a.add_connection('j', 0.9, True)
    node_a.add_connection('j', 0.05, False)
    node_a.add_connection('m', 0.7, True)
    node_a.add_connection('m', 0.01, False)

    node_j = BayesianNetwork.Node('j')
    node_m = BayesianNetwork.Node('m')

    # crea la red
    network = BayesianNetwork.BayesianNetwork()
    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_e)
    network.add_node(node_j)
    network.add_node(node_m)

    print(network.probabilistic_inference('m'))

</sub>

## API

Se incluyen las siguientes clases

### Clase BayesianNetwork

- add_node(nombre, valores, probabilidades): Agrega un nodo a la red bayesiana con el nombre especificado, los valores posibles y las probabilidades iniciales.

- add_edge(nodo_padre, nodo_hijo, probabilidades): Agrega una relación entre dos nodos de la red bayesiana, especificando las probabilidades condicionales.

### Clase Inference

- probability(nodo, evidencias): Devuelve la distribución de probabilidad de un nodo dado un conjunto de evidencias.
