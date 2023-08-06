import pyAgrum as gum


def crearred(red):
    # red = input('Cual es tu red?: ')
    bn = gum.fastBN(red)
    return bn


def estaDescrita(red):
    bn = gum.fastBN(red)
    nodes_count = bn.nodes()
    arcs_count = bn.arcs()

    if len(nodes_count) == len(arcs_count):
        print('La red Bayesiana esta completamente descrita')
    else:
        print('La red Bayesiana no esta completamente descrita')


# estaDescrita('c->r->w<-s<-c')


def redCompacta(red):
    bn = gum.fastBN(red)
    print('Representacion compacta: ', bn)


# redCompacta('c->r->w<-s<-c')


def factores(red):
    bn = gum.fastBN(red)
    for i in range(len(bn.nodes())):
        node = bn.variable(i)
        factor = bn.cpt(bn.nodeId(node))
        print(node.name(), ':', factor)


# factores('c->r->w<-s<-c')


def algoritmo_de_enumeracion(red):
    bn = gum.fastBN(red)
    ie = gum.LazyPropagation(bn)
    for i in range(len(bn.nodes())):
        node = bn.variable(i)
        results = ie.posterior(bn.nodeId(node))
        results_str = str(results)
        print(results_str)


# algoritmo_de_enumeracion('c->r->w<-s<-c')
