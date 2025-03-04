import sys
import time
import random
import os
import logging
from opcua import ua, Server

# Ricette con valori iniziali predefiniti
RECIPES = {
    1: {"press": 200, "temp": 1200},
    2: {"press": 350, "temp": 1000},
    3: {"press": 300, "temp": 1350},
}


VARIATION_RANGE = {
    "pression": 1,
    "speed": 0.1,
    "count": 5,
    "hum-press": 2,
    "hum-dry": 2,
    "temp-dry": 2,
    "temp-kiln": 4
}

# Configurazione del logger
logger = logging.getLogger("opcua_simulator")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Funzione per generare dati simulati con variazioni naturali
def generate_simulated_data(previous_data, anomaly_flags):
    global VARIATION_RANGE, logger

    # Gestione anomalie
    if anomaly_flags["FlagAnomalyPression"] and previous_data["pression"] < 400:
        previous_data["pression"] = random.randint(400, 600)
        logger.info("Generating pression anomaly")
    elif not anomaly_flags["FlagAnomalyPression"] and previous_data["pression"] > 400:
        previous_data["pression"] = 300
        logger.info("Deleting pression anomaly")

    if anomaly_flags["FlagAnomalyResetPH"]:
        previous_data["quality_printhead_1"] = 5
        previous_data["quality_printhead_2"] = 5
        previous_data["quality_printhead_3"] = 5
        logger.info("Managing printhead to restart")

    if anomaly_flags["FlagAnomalyPH-1"] and previous_data["quality_printhead_1"] > 1:
        previous_data["quality_printhead_1"] = 1
        logger.info("Generating printhead 1 anomaly")
    elif not anomaly_flags["FlagAnomalyPH-1"] and previous_data["quality_printhead_1"] == 1:
        previous_data["quality_printhead_1"] = 5
        logger.info("Deleting printhead 1 anomaly")

    if anomaly_flags["FlagAnomalyTempKiln"] and previous_data["temp-kiln"] < 1400:
        previous_data["temp-kiln"] = random.randint(1400, 1600)
        logger.info("Generating kiln's temperature anomaly")
    elif not anomaly_flags["FlagAnomalyTempKiln"] and previous_data["temp-kiln"] > 1400:
        previous_data["temp-kiln"] = 1200
        logger.info("Deleting kiln's temperature anomaly")


    # Normale variazione dati
    data = {}
    for key in previous_data:
        if key in VARIATION_RANGE:
            variation = random.uniform(-VARIATION_RANGE[key], VARIATION_RANGE[key])
            data[key] = max(0, round(previous_data[key] + variation, 2))
        else:
            data[key] = previous_data[key]  # No variation

    # Variation quality testina 2
    var = random.randint(0, 100)
    ph2 = data["quality_printhead_2"]

    if ph2 > 1 and var >= 99:
        ph2 -= 1

    # Variation quality testina 3
    ph3 = data["quality_printhead_3"]

    if ph3 > 1 and var <= 1:
        ph3 -= 1

    data["quality_printhead_2"] = ph2
    data["quality_printhead_3"] = ph3

    ph_sum = ph3 + ph2 + data["quality_printhead_1"]

    if ph_sum >= 14:
        data["quality_slab"] = 5
        data["quality_tone"] = 5
    elif ph_sum > 13:
        data["quality_slab"] = 4
        data["quality_tone"] = 4
    elif ph_sum > 10:
        data["quality_slab"] = 3
        data["quality_tone"] = 3
    elif ph_sum > 5:
        data["quality_slab"] = 2
        data["quality_tone"] = 2
    else:
        data["quality_slab"] = 1

    if anomaly_flags["FlagAnomalyQualitySlab"] and data["quality_slab"] > 1:
        data["quality_slab"] = 1
        logger.info("Generating slab's quality anomaly")

    if data["pression"] < 500 and data["pression"] > 400 and data["quality_slab"] > 1:
        data["quality_slab"] -= 1
        data["quality_tone"] -= 1
    elif data["pression"] > 500 and data["quality_slab"] > 2:
        data["quality_slab"] -= 2
        data["quality_tone"] -= 2

    if data["temp-kiln"] < 1500 and data["temp-kiln"] > 1400 and data["quality_tone"] > 1:
        data["quality_tone"] -= 1
    elif data["temp-kiln"] > 1500 and data["quality_tone"] > 2:
        data["quality_tone"] -= 2

    return data

# Lettura variabili di ambiente per IP, porta e URI
opc_ip = os.getenv('OPC_IP', '0.0.0.0')  # Default: 0.0.0.0
opc_port = os.getenv('OPC_PORT', '4840')  # Default: 4840
uri = os.getenv('OPC_URI', 'http://server-opcua/simulation/')  # Default URI
opc_path = os.getenv('OPC_PATH', 'simulation/opc-ua/')

if __name__ == "__main__":
    server = Server()

    # Impostazione dell'endpoint con variabili di ambiente
    server.set_endpoint(f"opc.tcp://{opc_ip}:{opc_port}/{opc_path}")

    logger.info(f"Server OPC UA in esecuzione su: opc.tcp://{opc_ip}:{opc_port}/{opc_path}")
    logger.info(f"Namespace registrato con URI: {uri}")

    idx = server.register_namespace(uri)

    objects = server.get_objects_node()
    simulated_data_node = objects.add_object(idx, "GrandiFiandreSim")

    # Variabili iniziali
    current_recipe = server.nodes.objects.add_variable(idx, "CurrentRecipe", 1)
    current_recipe.set_writable()

    anomaly_flags = {
        "FlagAnomalyPression": server.nodes.objects.add_variable(idx, "FlagAnomalyPression", False),
        "FlagAnomalyResetPH": server.nodes.objects.add_variable(idx, "FlagAnomalyResetPH", False),
        "FlagAnomalyPH-1": server.nodes.objects.add_variable(idx, "FlagAnomalyPH-1", False),
        "FlagAnomalyQualitySlab": server.nodes.objects.add_variable(idx, "FlagAnomalyQualitySlab", False),
        "FlagAnomalyTempKiln": server.nodes.objects.add_variable(idx, "FlagAnomalyTempKiln", False),
    }

    for flag in anomaly_flags.values():
        flag.set_writable()

    # Equipment e variabili
    equipments = {
        "Press": {"pression": 300, "speed": 2, "count": 10, "hum-press": 40},
        "Dryer": {"hum-dry": 10, "temp-dry": 175},
        "Printer": {"quality_printhead_1": 5, "quality_printhead_2": 5, "quality_printhead_3": 5, "quality_slab": 5},
        "Kiln": {"temp-kiln": 1200, "quality_tone": 5},
    }

    opc_tags = {}
    for eq, tags in equipments.items():
        eq_node = simulated_data_node.add_object(idx, eq)
        opc_tags[eq] = {tag: eq_node.add_variable(idx, tag, value) for tag, value in tags.items()}

    for eq in opc_tags.values():
        for tag in eq.values():
            tag.set_writable()

    server.start()
    previous_data = {
        "pression": 300, "speed": 1, "count": 40, "hum-press": 40,
        "hum-dry": 10, "temp-dry": 175,
        "quality_printhead_1": 5, "quality_printhead_2": 5, "quality_printhead_3": 5, "quality_slab": 5,
        "temp-kiln": 1200, "quality_tone": 5
    }

    try:
        selected = 0
        while True:
            selected_recipe = current_recipe.get_value()
            if selected_recipe in RECIPES and selected != selected_recipe:
                logger.info(f"Applying Recipe {selected_recipe}")
                selected = selected_recipe
                previous_data["pression"] = RECIPES[selected]["press"]
                previous_data["temp-kiln"] = RECIPES[selected]["temp"]

            anomaly_state = {flag: var.get_value() for flag, var in anomaly_flags.items()}
            data = generate_simulated_data(previous_data, anomaly_state)
            previous_data.update(data)

            # Process anomalies and reset flags
            for flag, value in anomaly_state.items():
                if value and flag == "FlagAnomalyResetPH":  # If flag is True
                    anomaly_flags[flag].set_value(False)

            for eq, tags in opc_tags.items():
                for tag_name, var in tags.items():
                    if tag_name in data:
                        var.set_value(data[tag_name])

            time.sleep(1)
    finally:
        server.stop()
        logger.info("Server stopped")
