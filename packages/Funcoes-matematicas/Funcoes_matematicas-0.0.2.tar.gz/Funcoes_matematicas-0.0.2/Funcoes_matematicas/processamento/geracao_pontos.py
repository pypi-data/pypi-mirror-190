
def pontos_da_funcao():
    funcao = input('Entre com a expressao da funçao (Ex1: x^2, Ex2: x*3): ')
    incremento = float(input('Qual o valor de incremento desejado para os valores do eixo x? '))

    funcao = funcao.split(' ')

    lista_x = []
    x = 0
    for i in range(10):
        lista_x.append(x)
        x += incremento

    lista_y = []
    for caractere in funcao[0]:
        if caractere == '*':
            for num in lista_x:
                y = num*float(funcao[0][2])
                lista_y.append(y)
        if caractere == '^':
            for num in lista_x:
                y = num**float(funcao[0][2])
                lista_y.append(y)
    print('valores x = ',lista_x)
    print('valores y = ',lista_y)
    return lista_x, lista_y

def teste():
    print('Entrou no teste')