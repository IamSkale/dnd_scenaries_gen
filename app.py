from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
from datetime import datetime

# Obtener la ruta absoluta del directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CORREGIDO: La carpeta debe llamarse 'templates' (plural)
app = Flask(__name__,
           template_folder=os.path.join(BASE_DIR, 'templates'),
           static_folder=os.path.join(BASE_DIR, 'static'))

# Ruta para servir la página principal
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error al cargar la plantilla: {str(e)}", 500

# Ruta para servir archivos estáticos (CSS, JS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Ruta para obtener los textos del JSON
@app.route('/api/textos', methods=['GET'])
def obtener_textos():
    json_path = os.path.join(BASE_DIR, 'data.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return jsonify(data)
    except FileNotFoundError:
        # Si no existe el archivo, crear uno por defecto
        datos_por_defecto = {
            "textos": [
                {
                    "id": 1,
                    "texto": "Bienvenido a la aplicación de lista de textos",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "id": 2,
                    "texto": "Puedes agregar nuevos textos usando el botón en la esquina superior",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "id": 3,
                    "texto": "Los textos se guardan automáticamente en el servidor",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }
        guardar_json(datos_por_defecto, json_path)
        return jsonify(datos_por_defecto)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para guardar un nuevo texto
@app.route('/api/textos', methods=['POST'])
def agregar_texto():
    json_path = os.path.join(BASE_DIR, 'data.json')
    try:
        nuevo_texto = request.json
        nuevo_texto['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Leer el archivo JSON actual
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Agregar el nuevo texto
        data['textos'].append(nuevo_texto)
        
        # Guardar en el archivo JSON
        guardar_json(data, json_path)
        
        return jsonify({"success": True, "mensaje": "Texto guardado exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Ruta para eliminar un texto
@app.route('/api/textos/<int:id>', methods=['DELETE'])
def eliminar_texto(id):
    json_path = os.path.join(BASE_DIR, 'data.json')
    try:
        # Leer el archivo JSON actual
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Filtrar el texto a eliminar
        data['textos'] = [texto for texto in data['textos'] if texto['id'] != id]
        
        # Guardar en el archivo JSON
        guardar_json(data, json_path)
        
        return jsonify({"success": True, "mensaje": "Texto eliminado exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Función auxiliar para guardar JSON
def guardar_json(data, json_path):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # Asegurarse de que la carpeta templates existe
    templates_dir = os.path.join(BASE_DIR, 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"✓ Creada carpeta: {templates_dir}")
    
    print(f"🚀 Servidor iniciado en http://localhost:5000")
    print(f"📁 Directorio de templates: {templates_dir}")
    print(f"📁 Directorio static: {app.static_folder}")
    print(f"📄 Archivo data.json: {os.path.join(BASE_DIR, 'data.json')}")
    print("\n")
    
    app.run(debug=True, host='localhost', port=5000)