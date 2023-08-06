import inspect
import tabulate
import sys



def debugTable(*args,exitDebug):
    # Busca o contexto de quem chamou a função debug:
    context = inspect.stack()[1][0]

    # Obtém detalhes de onde foi executado o debug:
    filename = context.f_code.co_filename
    linenumber = context.f_lineno

    # Resultados a serem exibidos:
    result = []

     # Percorre todas as variáveis a serem exibidas:
    for name in args:
        # Verifica se é uma variável local no contexto:
        if name in context.f_locals:
            result.append([name, type(context.f_locals[name]),context.f_locals[name] ])
        # Verifica se é uma variável global no contexto:
        elif name in context.f_globals:
            result.append([name, type(context.f_locals[name]),context.f_globals[name]])
        # Variável não encontrada no contexto:
        else:
            result.append([name, "Variable Not Found"])

    # Exibe os resultados em forma de tabela:
    print(f'[DEBUG] {filename} ({linenumber})')
    print(tabulate.tabulate(result, headers=['Variável', 'Type' , 'Valor' ], maxcolwidths=[None, None, 60], tablefmt="grid"))
    if exitDebug:
            sys.exit("Leaving The Debugger Running")
