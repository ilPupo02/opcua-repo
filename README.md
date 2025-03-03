# opcua-repo

## OPC UA Simulator

This project simulates an OPC UA server for interfacing with production machinery. The simulated data includes variables such as pressure, temperature, print quality, and other process variables. The server allows testing and simulating the operation of industrial machines such as presses, dryers, printers, and kilns.

## Features

### Recipes

The system simulates the application of three different recipes for the production process:

- **Recipe 1**:
  - Pressure: 200 bar
  - Kiln temperature: 1200°C
  
- **Recipe 2**:
  - Pressure: 350 bar
  - Kiln temperature: 1000°C
  
- **Recipe 3**:
  - Pressure: 300 bar
  - Kiln temperature: 1350°C

Note: The recipe can be selected via an HMI system, and the pressure and temperature values are set accordingly.

### Equipment

1. **Press**:
   - Pressure: Ranges from 300 bar [High value from 400 bar]
   - Conveyor roll
   - Slab count
   - Humidity

2. **Dryer**:
   - Humidity
   - Temperature ranging from 150°C to 200°C

3. **Printer**:
   - Printhead quality (3 printheads with ratings from 1 to 5 for each printhead's quality)
   - Visual sensor for slab quality (Rating from 1 to 5; a rating of 1 indicates a sheet with defects like scratches)

4. **Kiln**:
   - Temperature ranging from 900°C to 1400°C
   - Tone quality (Rating from 1 to 5)

### Simulated Anomalies

The system supports the simulation of various anomalies that affect production data:

1. **FlagAnomalyPression**: If activated, the press pressure will be set to high values [400 - 600 bar].
2. **FlagAnomalyResetPH**: If activated, the 3 printheads will be set to high quality (value 5).
3. **FlagAnomalyPH-1**: If activated, the first printhead will be set to low quality (value 1).
4. **FlagAnomalyTempKiln**: If activated, the kiln temperature will be set to high values [1400 - 1600 °C].
5. **FlagAnomalyQualitySlab**: If activated, the quality of the slab will be set to low value (value 1).

Anomalies are simulated as variations in the normal system values, and the quality ratings are adjusted unfairly to reflect real-world events.

## Settable Environment Variables

You can configure the following environment variables to customize the simulation behavior:

- `OPC_IP`: The IP address of the OPC UA server (Default: `0.0.0.0`)
- `OPC_PORT`: The port for the OPC UA server (Default: `4840`)
- `OPC_URI`: The URI for the OPC UA namespace (Default: `http://server-opcua/simulation/`)
- `OPC_PATH`: The OPC UA path for the simulated data (Default: `simulation/opc-ua/`)
