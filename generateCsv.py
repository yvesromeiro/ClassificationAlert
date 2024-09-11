import csv
import uuid
import random

# Função para gerar um ID aleatório
def generate_user_id():
    return str(uuid.uuid4())

# Função para gerar um estado de usuário aleatório
def generate_user_state():
    return random.choice(['active', 'inactive', 'pending'])

# Função para atribuir um gerente de forma aleatória
def assign_user_manager():
    return random.choice(['lucas.sec@company.com', 'anna@company.com'])

# Gerar os dados
users_data = []
for i in range(1, 501):
    row_id = i
    user_id = generate_user_id()
    user_state = generate_user_state()
    user_manager = assign_user_manager()
    users_data.append([row_id, user_id, user_state, user_manager])

# Escrever os dados em um arquivo CSV
csv_file = 'users_data.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['row_id', 'user_id', 'user_state', 'user_manager'])  # Cabeçalho
    writer.writerows(users_data)

csv_file
