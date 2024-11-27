import random
from datetime import datetime, timedelta
import names

def generate_sql_data(total_records=10000):
    def generate_plate():
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        numbers = ''.join(random.choices('0123456789', k=4))
        return f'{letters}{numbers}'
    
    def generate_cpf():
        numbers = ''.join(random.choices('0123456789', k=11))
        return f'{numbers[:3]}.{numbers[3:6]}.{numbers[6:9]}-{numbers[9:]}'
    
    def generate_cnh():
        return ''.join(random.choices('0123456789', k=6))
    
    def generate_cli_id():
        return str(random.randint(1000, 9999))

    car_models = {
        'Toyota': ['Corolla', 'Etios', 'Camry'],
        'Volkswagen': ['Voyage', 'Virtus', 'Jetta'],
        'Chevrolet': ['Cobalt', 'Onix', 'Prisma'],
        'Hyundai': ['HB20S', 'Elantra', 'New i20'],
        'Ford': ['Ka Sedan', 'Focus', 'Fusion']
    }
    
    zones = ['Barão Geraldo', 'Cambuí', 'Taquaral', 'Unicamp']
    
    with open('populate_taxi.sql', 'w', encoding='utf-8') as f:
        # Limpar tabelas
        f.write("""
-- Desabilitar verificação de chaves estrangeiras
SET CONSTRAINTS ALL DEFERRED;

-- Limpar todas as tabelas na ordem correta
TRUNCATE TABLE Fila CASCADE;
TRUNCATE TABLE Corrida CASCADE;
TRUNCATE TABLE Motorista CASCADE;
TRUNCATE TABLE Cliente CASCADE;
TRUNCATE TABLE Taxi CASCADE;
TRUNCATE TABLE Zona CASCADE;

-- Habilitar verificação de chaves estrangeiras
SET CONSTRAINTS ALL IMMEDIATE;

""")
        
        # Inserir zonas
        for zona in zones:
            f.write(f"INSERT INTO Zona (Zona) VALUES ('{zona}');\n")
        f.write('\n')
        
        # Gerar táxis
        num_taxis = total_records // 20
        plates = set()
        print(f"Gerando {num_taxis} táxis...")
        while len(plates) < num_taxis:
            plate = generate_plate()
            if plate not in plates:
                plates.add(plate)
                marca = random.choice(list(car_models.keys()))
                modelo = random.choice(car_models[marca])
                ano = random.randint(2015, 2024)
                licenca = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                f.write(f"INSERT INTO Taxi VALUES ('{plate}', '{marca}', '{modelo}', {ano}, '{licenca}');\n")
        f.write('\n')
        plates = list(plates)
        
        # Gerar clientes
        num_clients = total_records // 10
        client_ids = set()
        print(f"Gerando {num_clients} clientes...")
        while len(client_ids) < num_clients:
            cli_id = generate_cli_id()
            if cli_id not in client_ids:
                client_ids.add(cli_id)
                nome = names.get_full_name().replace("'", "''")
                cpf = generate_cpf()
                f.write(f"INSERT INTO Cliente VALUES ('{cli_id}', '{nome}', '{cpf}');\n")
        f.write('\n')
        client_ids = list(client_ids)
        
        # Gerar motoristas
        num_drivers = total_records // 20
        drivers = set()  # Tupla (CNH, Placa)
        print(f"Gerando {num_drivers} motoristas...")
        while len(drivers) < num_drivers:
            cnh = generate_cnh()
            placa = random.choice(plates)
            if (cnh, placa) not in drivers:
                drivers.add((cnh, placa))
                nome = names.get_full_name().replace("'", "''")
                f.write(f"INSERT INTO Motorista VALUES ('{cnh}', '{nome}', 1, '{placa}');\n")
        f.write('\n')
        
        # Gerar corridas
        num_rides = total_records * 4 // 10
        rides = set()  # Tupla (CliId, Placa, Data)
        print(f"Gerando {num_rides} corridas...")
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        days_range = (end_date - start_date).days
        
        while len(rides) < num_rides:
            cli_id = random.choice(client_ids)
            placa = random.choice(plates)
            date = start_date + timedelta(days=random.randint(0, days_range))
            date_str = date.strftime('%Y-%m-%d')
            
            if (cli_id, placa, date_str) not in rides:
                rides.add((cli_id, placa, date_str))
                f.write(f"INSERT INTO Corrida VALUES ('{cli_id}', '{placa}', '{date_str}');\n")
        f.write('\n')
        
        # Gerar registros de fila
        num_queue = total_records * 4 // 10
        queue_entries = set()  # Tupla (Zona, CNH)
        print(f"Gerando {num_queue} registros de fila...")
        
        while len(queue_entries) < num_queue:
            zona = random.choice(zones)
            cnh = random.choice([driver[0] for driver in drivers])  # Pegar CNH dos motoristas
            
            if (zona, cnh) not in queue_entries:
                queue_entries.add((zona, cnh))
                date = start_date + timedelta(days=random.randint(0, days_range))
                time_in = date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
                time_out = time_in + timedelta(minutes=random.randint(5, 120))
                km_in = random.randint(1000, 200000)
                
                f.write(f"INSERT INTO Fila VALUES ('{zona}', '{cnh}', "
                       f"'{time_in.strftime('%Y-%m-%d %H:%M:%S')}', "
                       f"'{time_out.strftime('%Y-%m-%d %H:%M:%S')}', {km_in});\n")
        
    print("\nArquivo SQL gerado com sucesso!")
    print("Para executar no PostgreSQL:")
    print("psql -U postgres -d taxi -f populate_taxi.sql")

if __name__ == "__main__":
    generate_sql_data(10000)