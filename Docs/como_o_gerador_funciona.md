# Metodologia de Geração de Dados de Telemetria

A geração dos dados para a massa de telemetria é realizada através de um **modelo procedural condicional**, implementado em Python usando a biblioteca `NumPy`.

Diferente de um sorteio puramente aleatório (que poderia combinar peças incompatíveis ou irrealistas), o algoritmo segue **quatro regras estruturais de dependência**:

---

### 1. Seleção em Cadeia Condicional (Hierarquia de Componentes)

A geração de cada linha do arquivo não é independente entre as colunas; ela segue uma ordem de decisão sequencial:

* **Passo 1 (CPU):** O algoritmo primeiro sorteia o fabricante (*Intel* ou *AMD*), a família (*Core i3/i5/i7/i9* ou *Ryzen 3/5/7/9*) e a geração do processador.
* **Passo 2 (Coerência de Núcleos, Threads e Clock):** Com base na família sorteada, os parâmetros técnicos da CPU são limitados dentro de faixas reais. Por exemplo, se a CPU escolhida for uma *i3* ou *Ryzen 3*, o script restringe a contagem de núcleos a 4.
* **Passo 3 (Condicionamento da GPU):** O modelo da GPU é sorteado em função do processador definido no Passo 1. Se o sistema identificou uma CPU de entrada (*i3* ou *Ryzen 3*), as probabilidades de sorteio são ajustadas para limitar a GPU a modelos integrados (*Intel UHD / Vega*) ou placas dedicadas de entrada (séries *GTX 1050/1650*), impedindo a atribuição de GPUs topo de linha a processadores de entrada.

---

### 2. Atribuição Dinâmica de Especificações Técnicas

* **VRAM por Categoria:** A memória de vídeo dedicada (VRAM) não é sorteada isoladamente. Se a placa gerada for uma GPU integrada, o valor de VRAM é automaticamente fixado em `0.0 GB`. Se for uma placa dedicada, a VRAM sorteada respeita o intervalo compatível com aquele chip gráfico específico (ex.: 4 GB a 12 GB).
* **Distribuição Amostral Ponderada:** Recursos como RAM, tipo de armazenamento (*SSD NVMe*, *SATA SSD*, *HDD*) e resolução de tela utilizam probabilidades ajustadas ao perfil de mercado (ex.: maior probabilidade para 8 GB e 16 GB de RAM, e menor probabilidade para 64 GB).

---

### 3. Continuidade Temporal por Sistema (`system_id`) e Escala de Processamento

Para simular telemetria real, o script sorteia primeiro um conjunto fixo de **25.000 identificadores únicos de máquinas (`system_id`)**. Em seguida, distribui **2.000.000 de medições/eventos** ao longo desse *pool* de sistemas em diferentes momentos do tempo (`timestamp`), garantindo que a mesma máquina apresente múltiplos registros de telemetria ao longo dos dias. 

A geração é realizada através de processamento em lotes (*chunks* de 50.000 linhas) com gravação incremental no arquivo CSV para otimização do uso de memória RAM.

---

### 4. Cálculo Sintético do Score do Sistema (Média Ponderada Real)

A coluna `system_overall_score` (pontuação de 1.0 a 10.0) é calculada dinamicamente via **Média Ponderada com Distribuição Percentual de Relevância**, corrigindo distorções causadas por métricas baseadas em mediana:

* **Pesos Ponderados do Hardware:**
  * **GPU VRAM (30%):** Relevância primária para desempenho gráfico e renderização.
  * **RAM Total (25%):** Capacidade de multitarefa e execução de softwares pesados.
  * **CPU Cores (15%) e Threads (10%):** Capacidade de processamento paralelo.
  * **Tipo de Armazenamento (10%):** Desempenho de leitura/escrita (NVMe SSD = 10.0, SATA SSD = 6.0, SSHD = 4.0, HDD = 2.0).
  * **Clock Base da CPU (5%) e Espaço em Disco Livre (5%):** Desempenho single-core e folga de armazenamento.
* **Penalidades Dinâmicas de Estresse:** Subtração direta na nota caso a máquina apresente gargalos instantâneos (ex.: uso de CPU > 90%, uso de RAM > 90% ou espaço livre em disco < 20 GB).

---

### 5. Injeção Controlada de Ruídos Estatísticos (Para futuro Tratamento ETL)

Para simular falhas reais de captura e permitir o teste de pipelines de limpeza no Data Warehouse, o script injeta um ruído de **0.5%** na massa de dados gerada:
* **Valores Outliers:** Registros com `cpu_usage_pct` variando anormalmente entre 101% e 250%.
* **Valores Nulos (`NaN`):** Ocorrência pontual de registros ausentes na coluna `gpu_vram_total_gb`.

---

> `python gerador_hardware.py` dentro da pasta do arquivo para rodar.