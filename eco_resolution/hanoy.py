import os
os.environ["PATH"] += os.pathsep + "/usr/local/bin"

from graphviz import Digraph

class Disco:
    def __init__(self, tamanho, destino, nome):
        self.nome = nome
        self.tamanho = tamanho
        self.destino = destino
        self.torre_atual = None
        self.satisfeito = False

    def pode_mover(self):
        return self.torre_atual[-1] == self

    def objetivo_satisfeito(self):
        return self.torre_atual == self.destino

    def tentar_mover(self, uml):
        if self.objetivo_satisfeito():
            self.satisfeito = True
            print(f"{self.nome}: já está satisfeito.")
            uml.node(self.nome, f"{self.nome}\nSatisfeito")
            return

        if not self.pode_mover():
            bloqueador = self.torre_atual[-1]
            if bloqueador != self:
                print(f"{self.nome}: está bloqueado por {bloqueador.nome}. Agressão!")
                uml.edge(self.nome, bloqueador.nome, label="Agressão")
                bloqueador.agredido_por(self, uml)
            return

        if self.destino and (not self.destino or self.destino[-1].tamanho > self.tamanho):
            self.mover_para(self.destino, uml)

    def agredido_por(self, outro, uml):
        print(f"{self.nome}: foi agredido por {outro.nome}, tentando fugir...")
        for torre in torres:
            if torre == self.torre_atual or torre == outro.torre_atual:
                continue
            if not torre or torre[-1].tamanho > self.tamanho:
                self.mover_para(torre, uml, fuga=True, de=outro)
                return
        print(f"{self.nome}: não conseguiu fugir. Agressão em cadeia!")
        uml.edge(self.nome, "Bloqueado", label="Falha na fuga")

    def mover_para(self, nova_torre, uml, fuga=False, de=None):
        origem = torres.index(self.torre_atual)
        destino = torres.index(nova_torre)
        acao = "fugiu para" if fuga else "moveu para"
        print(f"{self.nome} {acao} T{destino} (de T{origem})")

        self.torre_atual.remove(self)
        nova_torre.append(self)
        self.torre_atual = nova_torre

        if fuga and de:
            uml.edge(self.nome, f"T{destino}", label=f"Fugiu de {de.nome}")
        else:
            uml.edge(self.nome, f"T{destino}", label="Movimentou-se")

# Setup inicial
uml = Digraph(comment="Decisões ECO-RESOLUTION")

T1, T2, T3 = [], [], []
torres = [T1, T2, T3]

# Criação dos discos
d1 = Disco(1, T3, "D1")
d2 = Disco(2, T3, "D2")
d3 = Disco(3, T3, "D3")

# Adicionando todos na torre inicial
T1.extend([d3, d2, d1])  # ordem: menor no topo
for d in T1:
    d.torre_atual = T1

discos = [d1, d2, d3]

# Loop da simulação
for i in range(20):
    print(f"\n--- Iteração {i+1} ---")
    for disco in discos:
        if not disco.satisfeito:
            disco.tentar_mover(uml)

    if all(d.satisfeito for d in discos):
        print("Todos os discos estão satisfeitos. Fim da simulação.")
        break

# Salvar o gráfico UML
uml.render('uml_eco_resolution_hanoi', format='png', cleanup=True)
print("\n Diagrama UML salvo como 'uml_eco_resolution_hanoi.png'")
