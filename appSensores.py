from flask import Flask, request, jsonify
import json
import os
import csv

app = Flask(__name__)

ARCHIVO_JSON = 'datosSensor.json'
ARCHIVO_CSV = 'datosSensor.csv'

def actualizar_csv(datos):
    """Agrega una nueva fila al archivo CSV"""
    file_exists = os.path.isfile(ARCHIVO_CSV)
    with open(ARCHIVO_CSV, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['temperatura', 'humedad', 'timestamp'])
        if not file_exists:
            writer.writeheader() # Crea el encabezado si el archivo es nuevo
        writer.writerow(datos)

@app.route('/datos_sensor', methods=['POST'])
def recibirDatos():
    datos = request.get_json()
    
    # 1. Guardar en JSON 
    if not os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON,'w') as f:
            json.dump([], f)
            
    with open(ARCHIVO_JSON,'r') as f:
        contenido = json.load(f)
    
    contenido.append(datos)
    
    with open(ARCHIVO_JSON,'w') as f:
        json.dump(contenido, f, indent=4)
    
    # 2. Guardar en CSV 
    actualizar_csv(datos)
        
    return jsonify({'mensaje':'Dato recibido y guardado en JSON/CSV'}), 201

@app.route('/estadisticas', methods=['GET'])
def obtenerEstadisticas():
    """Calcula y muestra promedio, máximo y mínimo"""
    if not os.path.exists(ARCHIVO_JSON):
        return jsonify({'error': 'No hay datos suficientes'}), 404
    
    with open(ARCHIVO_JSON, 'r') as f:
        datos = json.load(f)
    
    if not datos:
        return jsonify({'mensaje': 'Lista de datos vacía'}), 200

    # Extraer listas de valores
    temps = [d['temperatura'] for d in datos]
    humedades = [d['humedad'] for d in datos]

    # Cálculos
    stats = {
        "promedio_humedad": round(sum(humedades) / len(humedades), 2),
        "temp_maxima": max(temps),
        "temp_minima": min(temps),
        "total_registros": len(datos)
    }
    
    return jsonify(stats), 200

if __name__ == '__main__':
    app.run(debug=True)