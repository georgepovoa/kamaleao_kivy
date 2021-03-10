cursor_kamaleao.execute("SELECT * FROM formulas WHERE nome LIKE '{}%'".format(value))
try:
    ###### aqui a gente limpa o dict que foi transformado em str #####
    formula_completa = cursor_kamaleao.fetchone()[1]
    formula_completa = formula_completa.replace("{", '')
    formula_completa = formula_completa.replace("}", '')
    formula_completa = formula_completa.translate({ord("'"): None})
    ###### e transforma ele em uma lista no formato nome da cor : valor #####
    formula_completa = formula_completa.split(',')

    ## Agora separa essas listas, para pegar o Nome e o valor de cada matéria prima ##
    for s in formula_completa:
        s = s.strip()
        s = s.split(":")

        ## aqui, soma no dict um valor se a matéria prima já estiver dentro do dict ##
        ## ou adiciona no dict uma nova matéria prima com seu valor a ser descontado  ##
        limite_formula = 0
        for limite in range(1,10000):
            nome = [s[0]]
            cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome =?",nome)
            estoque_atual = cursor_kamaleao.fetchone()[0]

            if s[0] in formula_formatada:
                formula_formatada[s[0]] = float(s[1]) * limite
                if formula_formatada[s[0]] > estoque_atual:
                    limite_formula = limite-1
                    print("f", f)
                    print("x", limite_formula)
                    direita_tab_limites.add_widget(Label(text= "{}x{}".format(f,limite_formula)))
                    break
            else:
                formula_formatada[s[0]] = float(s[1]) * limite
                if formula_formatada[s[0]] > estoque_atual:
                    limite_formula = limite

                    break




except Exception as e:
    print(e)

    background_color = (42 / 255, 62 / 255, 70 / 255, 1)