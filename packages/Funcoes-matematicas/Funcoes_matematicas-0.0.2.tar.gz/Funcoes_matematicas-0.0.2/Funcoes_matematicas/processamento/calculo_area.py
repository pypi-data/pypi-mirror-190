def area_funcao(pontos_x, pontos_y):
    integral_area = 0
    for x in range(len(pontos_x)-1):
        #Área do trapézio
            base1 = pontos_y[x]
            base2 = pontos_y[x+1]
            altura = pontos_x[x+1] - pontos_x[x]
            area = (base1 + base2)/2 * altura
            integral_area += area
    print(integral_area)
