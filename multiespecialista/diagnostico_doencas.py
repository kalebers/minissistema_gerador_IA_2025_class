class Node:
    def __init__(self, question=None, yes=None, no=None, result=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.result = result

    def is_leaf(self):
        return self.result is not None

    def print_tree(self, prefix=""):
        if self.is_leaf():
            print(prefix + "➡️ Diagnóstico: " + self.result)
        else:
            print(prefix + "🔹 Pergunta: " + self.question)
            print(prefix + "👉 Se SIM:")
            self.yes.print_tree(prefix + "    ")
            print(prefix + "👉 Se NÃO:")
            self.no.print_tree(prefix + "    ")

    def diagnose(self):
        if self.is_leaf():
            return self.result
        answer = input(self.question + " (s/n): ").strip().lower()
        if answer == 's':
            return self.yes.diagnose()
        else:
            return self.no.diagnose()


def planta_especialista():
    # Árvore de decisão para plantas
    return Node(
        "As folhas estão amareladas?",
        yes=Node(
            "Há manchas marrons nas folhas?",
            yes=Node(result="Fungos – aplicar fungicida."),
            no=Node(result="Falta de nutrientes – adubar.")
        ),
        no=Node(
            "As folhas estão caindo?",
            yes=Node(result="Excesso de água – reduzir irrigação."),
            no=Node(result="Planta saudável.")
        )
    )


def pet_especialista():
    # Árvore de decisão para pets
    return Node(
        "O animal está se coçando frequentemente?",
        yes=Node(
            "Há feridas ou queda de pelos?",
            yes=Node(result="Dermatite ou sarna – consultar veterinário."),
            no=Node(result="Presença de pulgas – aplicar antipulgas.")
        ),
        no=Node(
            "Ele está com apatia e sem apetite?",
            yes=Node(result="Possível virose – levar ao veterinário."),
            no=Node(result="Animal saudável.")
        )
    )


def main():
    print("🌱🐶 Bem-vindo ao Sistema Multiespecialista!")
    print("1. Diagnóstico de plantas")
    print("2. Diagnóstico de pets")

    escolha = input("Escolha a especialidade (1 ou 2): ").strip()

    if escolha == '1':
        especialista = planta_especialista()
        print("\n🧾 Árvore de decisão do especialista em plantas:")
        especialista.print_tree()
        print("\n🔍 Iniciando diagnóstico...\n")
        resultado = especialista.diagnose()
        print(f"\n✅ Resultado: {resultado}")

    elif escolha == '2':
        especialista = pet_especialista()
        print("\n🧾 Árvore de decisão do especialista em pets:")
        especialista.print_tree()
        print("\n🔍 Iniciando diagnóstico...\n")
        resultado = especialista.diagnose()
        print(f"\n✅ Resultado: {resultado}")

    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
