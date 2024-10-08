import sqlite3

def create_conection():
    return sqlite3.connect('tarefas.db')

def define_cursor(conexao):
    return conexao.cursor()

def create_table(cursor, conexao):

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS Tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa TEXT NOT NULL,
        status INTEGER DEFAULT 0

        );
    ''')

    conexao.commit()
# implementar ids automáticos e sempre sequenciais

def validate_status():
    while True:
        try:
            status = int(input('Digite o status da tarefa (0 - não feita, 1 - feita)'))
            if status in[0, 1]:
                return status
            else:
                print('Status inválido. Digite 0 ou 1')
        except ValueError:
            print('Entrada inválida. Digite 0 ou 1')

def id_existence(cursor):
    tarefa_id = int(input('Digite o ID da tarefa: '))

    cursor.execute('''
    SELECT id
    FROM tarefas
    WHERE id = ?
    
    ''', (tarefa_id,))

    resultado = cursor.fetchone()

    return tarefa_id, resultado

def create_data(cursor, conexao):

    tarefa = input('Digite a nova tarefa: ')
    status = validate_status()

    cursor.execute('''

        INSERT INTO tarefas (tarefa, status)
        VALUES (?, ?)

    ''', (tarefa, status))

    conexao.commit()
    print(f'Tarefa criada com sucesso: {tarefa}')

def read_data(cursor, conexao):

    cursor.execute('''

        SELECT * FROM tarefas

    ''')
    tarefas = cursor.fetchall()

    print('\nLista de Tarefas:')
    for linha in tarefas:
        status_str = 'Feita' if linha[2] else 'Não feita'
        print(f'ID: {linha[0]}, Tarefa: {linha[1]}, Status: {status_str}')
    print()

def update_task_status(cursor, conexao):
    tarefa_id, resultado = id_existence(cursor)

    if resultado:
        novo_status = validate_status()

        cursor.execute('''
            UPDATE Tarefas
            SET status = ?
            WHERE id = ?
        
        ''', (novo_status, tarefa_id))
        conexao.commit()
        print(f'Status da tarefa de ID {tarefa_id} atualizado com sucesso')
    else:
        print(f'Nenhuma tarefa com o ID {tarefa_id} encontrada')

def update_data(cursor, conexao):

    tarefa_id, resultado = id_existence(cursor)
    
    if resultado:
        nova_tarefa = input('Digite a nova tarefa: ')
        novo_status = validate_status()

        cursor.execute('''

            UPDATE tarefas
            SET tarefa = ?, status = ?
            WHERE id = ?

        ''', (nova_tarefa, novo_status, tarefa_id))

        print(f'Tarefa de ID {tarefa_id} atualizada com sucesso')
    else:
        print(f'Nenhuma tarefa com o ID {tarefa_id} encontrada')

    conexao.commit()
    
def delete_data(cursor, conexao):

    tarefa_id, resultado = id_existence(cursor)

    if resultado:

        cursor.execute('''

            DELETE FROM tarefas

            WHERE id = ?

        ''', (tarefa_id,))

        print(f'Tarefa com id {tarefa_id} apagada com sucesso')

    else:
        print(f'Nenhuma tarefa com o ID {tarefa_id} encontrada')

        

    conexao.commit()
    
def main_menu():
    while True:
        try:
            return int(input('''
            
            ***LISTA DE TAREFAS***
            
            Selecione abaixo o que deseja fazer:

            (1) - Adicionar nova tarefa
            (2) - Visualizar todas as tarefas
            (3) - Atualizar uma tarefa existente
            (4) - Atualizar o status de uma tarefa
            (5) - Apagar um tarefa
            (6) - Sair
            
            '''))
        except ValueError:
            print('Entrada inválida, por favor digite um número entre 1 e 5')

def secondary_menu():
    while True:
        try:
            return int(input('''O que deseja fazer agora?
                                (1) - Voltar ao meunu principal
                                (2) - Executar a mesma tarefa
                        '''))
        except ValueError:
            print('Entrada inválida, por favor digite 1 para voltar ao menu principal, ou 2 para realizar a mesma tarefa')

def handle_secondary_menu(action, cursor, conexao):
    while True:
        next_step = secondary_menu()
        if next_step == 1:
            break
        elif next_step == 2:
            action(cursor, conexao)
        else:
            print('Entrada inválida, por favor digite 1 para voltar ao menu principal, ou 2 para realizar a mesma tarefa')

def user_decision(cursor, conexao):

    choices = {
        1: create_data,
        2: read_data,
        3: update_data,
        4: update_task_status,
        5:delete_data
    }

    while True:
        user_choice = main_menu()

        if user_choice in choices:
            choices[user_choice](cursor, conexao)
            handle_secondary_menu(choices[user_choice], cursor, conexao)

        elif user_choice == 6:
            print('Encerrando o programa')
            conexao.close()
            break
        else:
            print('Entrada inválida, por favor digite um número entre 1 e 5')

def main():

    conexao = create_conection()
    cursor = define_cursor(conexao)
    create_table(cursor, conexao)
    user_decision(cursor, conexao)
    conexao.close()

if __name__ == '__main__':
    main()