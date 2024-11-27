import psycopg2
import time
from statistics import mean

# Consultas
QUERIES = {
    "Q1_Produtividade_Motoristas": """
    WITH HorasTrabalhadas AS (
        SELECT 
            m.CNH,
            m.Nome,
            COUNT(DISTINCT f.Zona) as num_zonas,
            SUM(EXTRACT(EPOCH FROM (f.DataHoraOut - f.DataHoraIn))/3600) as total_horas,
            AVG(f.KmIn) as media_km,
            COUNT(c.CliId) as total_corridas
        FROM Motorista m
        LEFT JOIN Fila f ON m.CNH = f.CNH
        LEFT JOIN Taxi t ON m.Placa = t.Placa
        LEFT JOIN Corrida c ON t.Placa = c.Placa
        GROUP BY m.CNH, m.Nome
        HAVING COUNT(c.CliId) > 0
    )
    SELECT * FROM HorasTrabalhadas ORDER BY total_corridas DESC LIMIT 10;
    """,
    
    "Q2_Demanda_Zona_Periodo": """
    WITH PeriodosDia AS (
        SELECT 
            f.Zona,
            CASE 
                WHEN EXTRACT(HOUR FROM f.DataHoraIn) BETWEEN 6 AND 11 THEN 'Manhã'
                WHEN EXTRACT(HOUR FROM f.DataHoraIn) BETWEEN 12 AND 17 THEN 'Tarde'
                WHEN EXTRACT(HOUR FROM f.DataHoraIn) BETWEEN 18 AND 23 THEN 'Noite'
                ELSE 'Madrugada'
            END as periodo,
            COUNT(*) as quantidade_corridas,
            AVG(EXTRACT(EPOCH FROM (f.DataHoraOut - f.DataHoraIn))/60) as tempo_medio_espera
        FROM Fila f
        GROUP BY f.Zona, periodo
    )
    SELECT * FROM PeriodosDia ORDER BY Zona, periodo;
    """,
    
    "Q3_Utilizacao_Frota": """
    WITH UtilizacaoTaxi AS (
        SELECT 
            t.Placa,
            t.Marca,
            t.Modelo,
            t.AnoFab,
            COUNT(DISTINCT c.CliId) as total_clientes,
            COUNT(c.DataPedido) as total_corridas,
            COUNT(DISTINCT m.CNH) as total_motoristas,
            COALESCE(SUM(EXTRACT(EPOCH FROM (f.DataHoraOut - f.DataHoraIn))/3600), 0) as horas_operacao
        FROM Taxi t
        LEFT JOIN Corrida c ON t.Placa = c.Placa
        LEFT JOIN Motorista m ON t.Placa = m.Placa
        LEFT JOIN Fila f ON m.CNH = f.CNH
        GROUP BY t.Placa, t.Marca, t.Modelo, t.AnoFab
    )
    SELECT * FROM UtilizacaoTaxi WHERE total_corridas > 0 
    ORDER BY horas_operacao DESC;
    """,
    
    "Q4_Padroes_Clientes": """
    WITH ClientePadrao AS (
        SELECT 
            cl.CliId,
            cl.Nome,
            COUNT(c.DataPedido) as total_corridas,
            COUNT(DISTINCT EXTRACT(DOW FROM c.DataPedido)) as dias_semana_distintos,
            COUNT(DISTINCT t.Marca) as marcas_distintas,
            STRING_AGG(DISTINCT z.Zona, ', ') as zonas_utilizadas
        FROM Cliente cl
        JOIN Corrida c ON cl.CliId = c.CliId
        JOIN Taxi t ON c.Placa = t.Placa
        JOIN Motorista m ON t.Placa = m.Placa
        JOIN Fila f ON m.CNH = f.CNH
        JOIN Zona z ON f.Zona = z.Zona
        GROUP BY cl.CliId, cl.Nome
    )
    SELECT * FROM ClientePadrao WHERE total_corridas > 5
    ORDER BY total_corridas DESC;
    """,
    
    "Q5_Eficiencia_Zona": """
    WITH EficienciaZona AS (
        SELECT 
            z.Zona,
            t.Marca,
            t.Modelo,
            COUNT(DISTINCT f.CNH) as total_motoristas,
            COUNT(DISTINCT c.CliId) as total_clientes,
            AVG(EXTRACT(EPOCH FROM (f.DataHoraOut - f.DataHoraIn))/60) as tempo_medio_atendimento,
            AVG(f.KmIn) as media_km,
            COUNT(c.DataPedido) as total_corridas
        FROM Zona z
        JOIN Fila f ON z.Zona = f.Zona
        JOIN Motorista m ON f.CNH = m.CNH
        JOIN Taxi t ON m.Placa = t.Placa
        LEFT JOIN Corrida c ON t.Placa = c.Placa
        GROUP BY z.Zona, t.Marca, t.Modelo
    )
    SELECT * FROM EficienciaZona WHERE total_corridas > 0
    ORDER BY Zona, total_corridas DESC;
    """
}

def run_benchmark():
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            dbname="taxi",
            user="postgres",
            password="1234",  # Altere para sua senha
            host="localhost"
        )
        cursor = conn.cursor()
        
        # Para cada consulta
        for query_name, query in QUERIES.items():
            print(f"\nExecutando {query_name}")
            execution_times = []
            
            # Executar 100 vezes
            for i in range(100):
                cursor.execute("DISCARD ALL")  # Limpar cache
                
                start_time = time.time()
                cursor.execute(query)
                cursor.fetchall()
                execution_time = time.time() - start_time
                
                execution_times.append(execution_time)
            
            # Calcular e mostrar média
            avg_time = mean(execution_times)
            print(f"Tempo médio de execução: {avg_time:.4f} segundos")
        
    except Exception as e:
        print(f"Erro: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_benchmark()