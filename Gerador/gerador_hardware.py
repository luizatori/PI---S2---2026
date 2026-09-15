import uuid
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#funcoes para geracao dinamica e procedural de componentes
def gerar_cpu_dinamica():
    marcas = ['Intel', 'AMD']
    marca = np.random.choice(marcas, p=[0.55, 0.45])
    
    if marca == 'Intel':
        linha = np.random.choice(['Core i3', 'Core i5', 'Core i7', 'Core i9'], p=[0.25, 0.45, 0.22, 0.08])
        geracao = np.random.choice([9, 10, 11, 12, 13, 14])
        sku = np.random.randint(100, 900)
        sufixo = np.random.choice(['', 'F', 'K', 'KF', 'T'], p=[0.4, 0.3, 0.15, 0.1, 0.05])
        modelo = f"Intel {linha}-{geracao}{sku:03d}{sufixo}".strip()
        
        if 'i3' in linha:
            cores, threads = 4, np.random.choice([4, 8])
            clock = round(float(np.random.uniform(3.1, 3.8)), 1)
        elif 'i5' in linha:
            cores = np.random.choice([6, 10])
            threads = 12 if cores == 6 else 16
            clock = round(float(np.random.uniform(2.5, 3.7)), 1)
        elif 'i7' in linha:
            cores = np.random.choice([8, 12])
            threads = 16 if cores == 8 else 20
            clock = round(float(np.random.uniform(3.4, 3.8)), 1)
        else:
            cores, threads = 16, 24
            clock = round(float(np.random.uniform(3.0, 4.2)), 1)
            
    else:
        linha = np.random.choice(['Ryzen 3', 'Ryzen 5', 'Ryzen 7', 'Ryzen 9'], p=[0.20, 0.50, 0.22, 0.08])
        geracao = np.random.choice([3, 4, 5, 7])
        sku = np.random.choice([600, 700, 800, 900, 200, 400])
        sufixo = np.random.choice(['', 'X', 'G', 'X3D'], p=[0.4, 0.35, 0.2, 0.05])
        modelo = f"AMD {linha} {geracao}{sku}{sufixo}".strip()
        
        if 'Ryzen 3' in linha:
            cores, threads = 4, np.random.choice([4, 8])
            clock = round(float(np.random.uniform(3.4, 3.8)), 1)
        elif 'Ryzen 5' in linha:
            cores, threads = 6, 12
            clock = round(float(np.random.uniform(3.2, 3.9)), 1)
        elif 'Ryzen 7' in linha:
            cores, threads = 8, 16
            clock = round(float(np.random.uniform(3.4, 4.2)), 1)
        else:
            cores, threads = 12, 24
            clock = round(float(np.random.uniform(3.7, 4.5)), 1)
            
    return modelo, cores, threads, clock

def gerar_gpu_coerente(cpu_modelo):
    is_entry_cpu = 'i3' in cpu_modelo or 'Ryzen 3' in cpu_modelo
    
    if is_entry_cpu:
        tipo = np.random.choice(['Integrated', 'NVIDIA_Entry', 'AMD_Entry'], p=[0.60, 0.28, 0.12])
        if tipo == 'NVIDIA_Entry':
            num = np.random.choice([1050, 1650, 1660, 3050])
            sufixo = np.random.choice(['', 'Ti', 'Super'], p=[0.5, 0.3, 0.2])
            vram = float(np.random.choice([3.0, 4.0, 6.0, 8.0]))
            modelo = f"NVIDIA GeForce GTX {num} {sufixo}".strip() if num < 2000 else f"NVIDIA GeForce RTX {num} {sufixo}".strip()
        elif tipo == 'AMD_Entry':
            num = np.random.choice([580, 5500, 6600])
            sufixo = np.random.choice(['', 'XT'], p=[0.7, 0.3])
            vram = float(np.random.choice([4.0, 8.0]))
            modelo = f"AMD Radeon RX {num} {sufixo}".strip()
        else:
            modelo = np.random.choice([
                'Intel HD Graphics 620', 
                'Intel UHD Graphics 630', 
                'Intel Iris Xe Graphics', 
                'AMD Radeon Vega 7', 
                'AMD Radeon Vega 8'
            ])
            vram = 0.0
    else:
        tipo = np.random.choice(['NVIDIA', 'AMD', 'Integrated', 'None'], p=[0.55, 0.25, 0.15, 0.05])
        if tipo == 'NVIDIA':
            serie = np.random.choice(['GTX', 'RTX'], p=[0.2, 0.8])
            if serie == 'GTX':
                num = np.random.choice([1650, 1660])
                sufixo = np.random.choice(['', 'Super'])
                vram = float(np.random.choice([4.0, 6.0]))
            else:
                num = np.random.choice([2060, 3050, 3060, 3070, 4060])
                sufixo = np.random.choice(['', 'Ti'], p=[0.7, 0.3])
                vram = float(np.random.choice([6.0, 8.0, 12.0]))
            modelo = f"NVIDIA GeForce {serie} {num} {sufixo}".strip()
        elif tipo == 'AMD':
            num = np.random.choice([580, 6600, 6700, 7600])
            sufixo = np.random.choice(['', 'XT'], p=[0.7, 0.3])
            vram = float(np.random.choice([4.0, 8.0, 12.0]))
            modelo = f"AMD Radeon RX {num} {sufixo}".strip()
        elif tipo == 'Integrated':
            modelo = np.random.choice([
                'Intel HD Graphics 620', 
                'Intel UHD Graphics 630', 
                'Intel Iris Xe Graphics', 
                'AMD Radeon Vega 7', 
                'AMD Radeon Vega 8'
            ])
            vram = 0.0
        else:
            modelo = 'None'
            vram = 0.0
        
    return modelo, vram

def gerar_massa_telemetria(total_linhas=2_000_000, chunk_size=50_000, output_file='gerador_hardware.csv'):
    print(f"iniciando geracao de {total_linhas:,} linhas com geracao dinamica procedural...")
    inicio = time.time()

    #opcoes de configuracao estatica
    os_opcoes = ['Windows 10', 'Windows 11', 'Ubuntu Linux', 'Debian Linux', 'Fedora', 'macOS']
    os_prob = [0.55, 0.30, 0.08, 0.03, 0.02, 0.02]

    ram_opcoes = [4, 8, 12, 16, 24, 32, 64]
    ram_prob = [0.08, 0.45, 0.07, 0.32, 0.03, 0.04, 0.01]

    storage_opcoes = ['SATA SSD', 'NVMe SSD', 'HDD', 'Hybrid SSHD']
    storage_prob = [0.45, 0.38, 0.15, 0.02]

    resolution_opcoes = ['1366x768', '1600x900', '1920x1080', '2560x1080', '2560x1440', '3840x2160']
    resolution_prob = [0.25, 0.05, 0.60, 0.04, 0.04, 0.02]

    #pool fixo de 25000 maquinas para simular repeticao de eventos
    num_maquinas = 25_000
    print(f"gerando perfil fixo para {num_maquinas:,} maquinas...")
    
    system_ids = [str(uuid.uuid4()) for _ in range(num_maquinas)]
    os_names_pool = np.random.choice(os_opcoes, num_maquinas, p=os_prob)
    os_versions_pool = [
        '22H2' if 'Windows' in os else ('22.04 LTS' if 'Linux' in os else '14.2') 
        for os in os_names_pool
    ]
    
    cpus_pool = [gerar_cpu_dinamica() for _ in range(num_maquinas)]
    cpu_models_pool = [c[0] for c in cpus_pool]
    cpu_cores_pool = [c[1] for c in cpus_pool]
    cpu_threads_pool = [c[2] for c in cpus_pool]
    cpu_clocks_pool = [c[3] for c in cpus_pool]
    
    ram_totals_pool = np.random.choice(ram_opcoes, num_maquinas, p=ram_prob)
    
    gpus_pool = [gerar_gpu_coerente(cpu_models_pool[idx]) for idx in range(num_maquinas)]
    gpu_models_pool = [g[0] for g in gpus_pool]
    gpu_vrams_pool = [g[1] for g in gpus_pool]
    
    storage_types_pool = np.random.choice(storage_opcoes, num_maquinas, p=storage_prob)
    resolutions_pool = np.random.choice(resolution_opcoes, num_maquinas, p=resolution_prob)

    #atribuicao de maquina para cada evento
    sys_idx = np.random.choice(num_maquinas, total_linhas)
    data_base = datetime.utcnow() - timedelta(days=30)

    for i in range(0, total_linhas, chunk_size):
        atual_chunk = min(chunk_size, total_linhas - i)
        
        batch_sys_indices = sys_idx[i:i+atual_chunk]
                
        #recupera as propriedades fixas das maquinas deste lote
        batch_system_ids = [system_ids[idx] for idx in batch_sys_indices]
        os_names         = [os_names_pool[idx] for idx in batch_sys_indices]
        os_versions      = [os_versions_pool[idx] for idx in batch_sys_indices]
        cpu_models       = [cpu_models_pool[idx] for idx in batch_sys_indices]
        cpu_cores        = [cpu_cores_pool[idx] for idx in batch_sys_indices]
        cpu_threads      = [cpu_threads_pool[idx] for idx in batch_sys_indices]
        cpu_clocks       = [cpu_clocks_pool[idx] for idx in batch_sys_indices]
        ram_totals       = [ram_totals_pool[idx] for idx in batch_sys_indices]
        gpu_models       = [gpu_models_pool[idx] for idx in batch_sys_indices]
        gpu_vrams        = [gpu_vrams_pool[idx] for idx in batch_sys_indices]
        storage_types    = [storage_types_pool[idx] for idx in batch_sys_indices]
        resolutions      = [resolutions_pool[idx] for idx in batch_sys_indices]
        
        #1. identificacao e controle temporal por evento
        event_ids = [str(uuid.uuid4()) for _ in range(atual_chunk)]
        timestamps = [
            (data_base + timedelta(seconds=int(np.random.randint(0, 30*24*3600)))).isoformat() + "Z"
            for _ in range(atual_chunk)
        ]

        #2. telemetria e metricas dinamicas em tempo real
        storage_frees = np.round(np.random.uniform(2.0, 950.0, atual_chunk), 2)
        cpu_usages = np.round(np.random.uniform(1.0, 100.0, atual_chunk), 2)
        ram_usages = np.round(np.random.uniform(10.0, 99.0, atual_chunk), 2)
        
        gpu_vram_usages = np.round(
            np.where(np.array(gpu_vrams) > 0, np.random.uniform(5.0, 98.0, atual_chunk), 0.0), 
            2
        )

        #3. calculo do score sintetico geral baseado na media ponderada real
        
        #normalizacao dos componentes (0.0 a 10.0)
        nota_gpu = np.clip(np.nan_to_num(gpu_vrams) / 12.0, 0.0, 1.0) * 10.0
        nota_ram = np.clip(np.array(ram_totals) / 32.0, 0.0, 1.0) * 10.0
        nota_cpu_cores = np.clip(np.array(cpu_cores) / 12.0, 0.0, 1.0) * 10.0
        nota_cpu_threads = np.clip(np.array(cpu_threads) / 24.0, 0.0, 1.0) * 10.0
        nota_cpu_clock = np.clip((np.array(cpu_clocks) - 2.0) / 2.0, 0.0, 1.0) * 10.0
        
        st_arr = np.array(storage_types)
        nota_storage_tipo = np.where(st_arr == 'NVMe SSD', 10.0,
                            np.where(st_arr == 'SATA SSD', 6.0,
                            np.where(st_arr == 'Hybrid SSHD', 4.0, 2.0)))
        
        nota_storage_livre = np.clip(np.array(storage_frees) / 250.0, 0.0, 1.0) * 10.0

        #formula de media ponderada com distribuicao percentual
        #gpu (30%), ram (25%), cores (15%), threads (10%), storage tipo (10%), clock (5%), storage livre (5%)
        media_ponderada_hardware = (
            (nota_gpu * 0.30) +
            (nota_ram * 0.25) +
            (nota_cpu_cores * 0.15) +
            (nota_cpu_threads * 0.10) +
            (nota_storage_tipo * 0.10) +
            (nota_cpu_clock * 0.05) +
            (nota_storage_livre * 0.05)
        )

        #penalidade dinamica pontual por estresse instantaneo
        penalidade_uso = (
            np.where(cpu_usages > 90.0, 0.6, 0.0) +
            np.where(ram_usages > 90.0, 0.6, 0.0) +
            np.where(storage_frees < 20.0, 0.5, 0.0)
        )

        system_scores = np.round(np.clip(media_ponderada_hardware - penalidade_uso, 1.0, 10.0), 2)

        #montagem do dataframe
        df_chunk = pd.DataFrame({
            'event_id': event_ids,
            'system_id': batch_system_ids,
            'timestamp': timestamps,
            'os_name': os_names,
            'os_version': os_versions,
            'cpu_model': cpu_models,
            'cpu_cores_physical': cpu_cores,
            'cpu_threads': cpu_threads,
            'cpu_clock_base_ghz': cpu_clocks,
            'cpu_usage_pct': cpu_usages,
            'ram_total_gb': ram_totals,
            'ram_usage_pct': ram_usages,
            'gpu_model': gpu_models,
            'gpu_vram_total_gb': gpu_vrams,
            'gpu_vram_usage_pct': gpu_vram_usages,
            'storage_primary_type': storage_types,
            'storage_free_gb': storage_frees,
            'display_resolution': resolutions,
            'system_overall_score': system_scores
        })

        #insercao de ruidos estatisticos para tratamento posterior no etl / data warehouse
        ruido_mask = np.random.rand(atual_chunk) < 0.005
        df_chunk.loc[ruido_mask, 'cpu_usage_pct'] = np.random.uniform(101.0, 250.0, np.sum(ruido_mask))
        df_chunk.loc[ruido_mask, 'gpu_vram_total_gb'] = np.nan

        #gravacao incremental no arquivo csv
        modo_escrita = 'w' if i == 0 else 'a'
        df_chunk.to_csv(output_file, mode=modo_escrita, header=(i == 0), index=False)

        print(f"   [+] processadas {i + atual_chunk:,} / {total_linhas:,} linhas...")

    tempo_total = time.time() - inicio
    print(f"\nconcluido! arquivo '{output_file}' gerado com sucesso em {tempo_total:.2f} segundos.")

if __name__ == '__main__':
    #valor de linhas completamente alteravel de acordo com a nescessidade 
    gerar_massa_telemetria(total_linhas=5_000_000)git push