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
* **Distribuição Amostral Ponderada:** Recursos como RAM, tipo de armazenamento (*SSD NVMe*, *SATA SSD*, *HDD*) e resolução de tela utilizam probabilidades ajustadas ao perfil de mercado brasileiro (ex.: maior probabilidade para 8 GB e 16 GB de RAM, e menor probabilidade para 64 GB).

---

### 3. Continuidade Temporal por Sistema (`system_id`)

Para simular telemetria real, o script sorteia primeiro um conjunto fixo de **25.000 identificadores únicos de máquinas (`system_id`)**. Em seguida, distribui as **500.000 medições** ao longo desse *pool* de sistemas em diferentes momentos do tempo (`timestamp`), garantindo que a mesma máquina apresente registros repetidos de telemetria ao longo dos dias.

---

### 4. Cálculo Sintético do Score do Sistema

A coluna `system_overall_score` (pontuação de 0.5 a 10.0) é calculada dinamicamente via fórmula matemática que pondera:

* **Potência combinada do hardware gerado:** Núcleos de CPU, total de RAM, VRAM e velocidade do armazenamento.
* **Penalidades pontuais de estresse instantâneo:** Subtração de pontos por eventos como uso de CPU acima de 90% ou disco quase cheio.