# opcua-repo

# OPC UA Simulator

Questo progetto simula un server OPC UA per l'interfacciamento con macchinari di produzione. I dati simulati includono variabili come la pressione, la temperatura, la qualità della stampa e altre variabili di processo. Il server consente di testare e simulare il funzionamento di macchinari industriali, come presse, essiccatori, stampanti e forni.

## Funzionalità

### Ricette

Il sistema simula l'applicazione di tre ricette differenti per il processo di produzione:

- **Ricetta 1**:
  - Pressione: 200 bar
  - Temperatura forno: 1200°C
  
- **Ricetta 2**:
  - Pressione: 350 bar
  - Temperatura forno: 1000°C
  
- **Ricetta 3**:
  - Pressione: 300 bar
  - Temperatura forno: 1350°C

Nota: La ricetta viene selezionata tramite un sistema HMI, e i valori di pressione e temperatura vengono impostati di conseguenza.

### Equipment (Macchinari)

1. **Pressa**:
   - Pressione: Variabile tra 300 bar
   - Rulliera di trasporto
   - Conteggio delle lastre
   - Umidità

2. **Essicatore**:
   - Umidità
   - Temperatura tra 150 - 200°C

3. **Stampante**:
   - Qualità delle testine (9 testine con una valutazione da 1 a 5 della qualità)
   - Sensore visivo per la qualità della lastra (Valutazione da 1 a 5; un valore di 1 indica una lastra con anomalie come graffi)

4. **Forno**:
   - Temperatura tra 900 - 1400°C
   - Qualità del tono (Valutazione da 1 a 5)

### Anomalie Simulate

Il sistema supporta la simulazione di diverse anomalie, che influenzano i dati di produzione:

1. **FlagPressa**: Se attivato, la pressione della pressa verrà impostata su valori alti.
2. **FlagStampaTestina**: Se attivato, una delle 9 testine di stampa avrà una bassa qualità (valore 1).
3. **FlagStampaSensore**: Se attivato, la qualità di una lastra sarà bassa (valore 1).
4. **FlagForno**: Se attivato, la temperatura del forno verrà impostata su valori elevati.

Le anomalie vengono simulate come variazioni nei valori normali del sistema, e le qualità sono modificate in modo non equo per riflettere eventi reali.

## Come usare

1. **Clona il repository**:
   ```bash
   git clone https://github.com/ilpupo02/opcua-repo.git
   cd opcua-repo
