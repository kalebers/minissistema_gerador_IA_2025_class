from paip.gps import gps

"""
Domínio: Melhoria do controle de estoque em uma empresa.
Objetivo: Resolver problemas identificados na auditoria interna através de ações concretas.
Método: Planejamento automatizado baseado no método STRIPS.
"""

problem = {
    "init": ["problema no controle de estoque"],
    "finish": ["estoque controlado"],
    "ops": [
        {
            "action": "Revisar processo de entrada de materiais",
            "preconds": ["problema no controle de estoque"],
            "add": ["processo de entrada revisado"],
            "delete": []
        },
        {
            "action": "Treinar equipe sobre novo processo",
            "preconds": ["processo de entrada revisado"],
            "add": ["equipe treinada"],
            "delete": []
        },
        {
            "action": "Implementar checklist de conferência",
            "preconds": ["equipe treinada"],
            "add": ["estoque controlado"],
            "delete": ["problema no controle de estoque"]
        }
    ]
}

def main():
    start = problem['init']
    finish = problem['finish']
    ops = problem['ops']
    msg = "Você deve:"

    plan = gps(start, finish, ops, msg)

    if plan is not None:
        print("\nPlano gerado com sucesso:")
        current_state = set(start)
        for i, action in enumerate(plan):
            print(f"\nPasso {i + 1}: {action}")
            clean_action = action.replace("Você deve:", "").strip()
            op = next(op for op in ops if op["action"] == clean_action)

            print(f"  - Pré-condições: {op['preconds']}")
            print(f"  - Estado antes: {list(current_state)}")
            current_state -= set(op.get("delete", []))
            current_state |= set(op.get("add", []))
            print(f"  - Estado depois: {list(current_state)}")
        print(f"\nEstado final alcançado: {finish[0] in current_state}")
    else:
        print('O plano não foi gerado')

if __name__ == '__main__':
    main()
