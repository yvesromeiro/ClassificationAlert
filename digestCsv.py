def process_csv_and_insert(csv_file, classifications, session_usersdb, session_marketingdb):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        # Debug: Exibir os nomes das colunas do CSV
        print(f"Colunas do CSV: {reader.fieldnames}")
        for row in reader:
            user_manager = row.get('user_manager')
            if not user_manager:
                print(f"Erro: 'user_manager' não encontrado na linha: {row}")
                continue
            db_classification = get_db_for_manager(classifications, user_manager)

            if db_classification:
                if db_classification['classification'] == 'high':
                    user = User(
                        user_id=row.get('user_id'),
                        name=row.get('name'),
                        email=row.get('email'),
                        birthdate=row.get('birthdate'),
                        document=row.get('document'),
                        gender=row.get('gender'),
                        telephone=row.get('telephone'),
                        user_state=row.get('user_state'),
                        yearly_income=float(row.get('yearly_income', 0))  # Definir 0 como padrão se não estiver presente
                    )
                    session_usersdb.add(user)
                elif db_classification['classification'] == 'medium':
                    user = User(
                        user_id=row.get('user_id'),
                        name=row.get('name'),
                        email=row.get('email'),
                        birthdate=row.get('birthdate'),
                        document=row.get('document'),
                        gender=row.get('gender'),
                        telephone=row.get('telephone'),
                        user_state=row.get('user_state'),
                        yearly_income=float(row.get('yearly_income', 0))
                    )
                    session_marketingdb.add(user)
