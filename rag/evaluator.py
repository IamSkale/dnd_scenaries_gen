import re
from typing import Dict, List, Tuple

class RAGEvaluator:
    """Evaluador de escenarios D&D que verifica que el texto generado cumpla con las características requeridas"""
    
    def __init__(self):
        print("🎲 Inicializando Evaluador de Escenarios D&D")
        self.criterios_evaluacion = self._cargar_criterios()
    
    def _cargar_criterios(self) -> Dict:
        """Carga los criterios de evaluación"""
        return {
            "raza": {
                "palabras_clave": {
                    "humanos": ["humano", "humanos", "aldea", "castillo", "mercader", "comercio", "ciudad", "reino"],
                    "elfos": ["elfo", "elfos", "árbol", "bosque", "magia", "naturaleza", "ancestral", "feérico"],
                    "enanos": ["enano", "enanos", "montaña", "forja", "martillo", "piedra", "tesoro", "mineral"],
                    "orcos": ["orco", "orcos", "guerrero", "tribu", "fuerza", "combate", "clan", "honor"],
                    "duendes": ["duende", "duendes", "pequeño", "astuto", "trampa", "ingenio"],
                    "halflings": ["halfling", "mediano", "pequeño", "comunidad", "hobbit"],
                    "tieflings": ["tiefling", "infernal", "cuernos", "demonio", "maldición"],
                    "dragonborns": ["dragonborn", "draconico", "escamas", "aliento", "dragon"]
                }
            },
            "ambiente": {
                "palabras_clave": {
                    "bosques": ["árbol", "bosque", "hoja", "naturaleza", "verde", "flora", "fauna", "selva"],
                    "montañas": ["montaña", "pico", "roca", "altura", "nieve", "cordillera", "valle"],
                    "desiertos": ["desierto", "arena", "sol", "duna", "calor", "árido", "sed"],
                    "junglas": ["jungla", "vegetación", "denso", "tropical", "exótico", "selva"],
                    "cuevas": ["cueva", "subterráneo", "caverna", "oscuro", "profundidad", "túnel"],
                    "pantanos": ["pantano", "ciénaga", "lodo", "niebla", "humedad", "ciénaga"],
                    "praderas": ["pradera", "llano", "hierba", "campo", "abierto", "pastizal"],
                    "tundra": ["tundra", "hielo", "nieve", "frío", "glaciar", "polar"],
                    "costas": ["costa", "mar", "playa", "océano", "acantilado", "puerto"]
                }
            },
            "extension": {
                "palabras_clave": {
                    "pueblo": ["pueblo", "aldea", "vecino", "casa", "comunidad", "habitante"],
                    "reino": ["reino", "tierra", "dominio", "territorio", "nación", "frontera"],
                    "región": ["región", "zona", "área", "territorio", "extensión", "provincia"]
                }
            }
        }
    
    def evaluar_escenario(self, texto: str, raza: str, ambiente: str, extension: str) -> Dict:
        """
        Evalúa si el escenario generado cumple con todas las características requeridas
        
        Returns:
            Dict con: {
                "cumple": bool,
                "puntuacion": float (0-100),
                "detalles": dict con evaluaciones por categoría,
                "razones": list de problemas encontrados,
                "sugerencias": list de mejoras sugeridas
            }
        """
        texto_lower = texto.lower()
        
        evaluacion = {
            "cumple": True,
            "puntuacion": 0,
            "detalles": {},
            "razones": [],
            "sugerencias": []
        }
        
        # Evaluar cada categoría
        evaluacion["detalles"]["raza"] = self._evaluar_categoria(
            texto_lower, raza, self.criterios_evaluacion["raza"]["palabras_clave"], "raza"
        )
        
        evaluacion["detalles"]["ambiente"] = self._evaluar_categoria(
            texto_lower, ambiente, self.criterios_evaluacion["ambiente"]["palabras_clave"], "ambiente"
        )
        
        evaluacion["detalles"]["extension"] = self._evaluar_categoria(
            texto_lower, extension, self.criterios_evaluacion["extension"]["palabras_clave"], "extensión"
        )
        
        # Verificar longitud y coherencia
        evaluacion["detalles"]["longitud"] = self._evaluar_longitud(texto)
        evaluacion["detalles"]["coherencia"] = self._evaluar_coherencia(texto)
        
        # Calcular puntuación total
        puntuaciones = [
            evaluacion["detalles"]["raza"]["puntuacion"],
            evaluacion["detalles"]["ambiente"]["puntuacion"],
            evaluacion["detalles"]["extension"]["puntuacion"],
            evaluacion["detalles"]["longitud"]["puntuacion"],
            evaluacion["detalles"]["coherencia"]["puntuacion"]
        ]
        evaluacion["puntuacion"] = sum(puntuaciones) / len(puntuaciones)
        
        # Determinar si cumple (puntuación mínima 70%)
        evaluacion["cumple"] = evaluacion["puntuacion"] >= 70
        
        # Recopilar razones y sugerencias
        for categoria, detalle in evaluacion["detalles"].items():
            if not detalle.get("cumple", True):
                evaluacion["razones"].extend(detalle.get("razones", []))
                evaluacion["sugerencias"].extend(detalle.get("sugerencias", []))
        
        return evaluacion
    
    def _evaluar_categoria(self, texto: str, valor_requerido: str, palabras_clave: Dict, nombre_categoria: str) -> Dict:
        """Evalúa una categoría específica (raza, ambiente, extensión)"""
        
        resultado = {
            "cumple": False,
            "puntuacion": 0,
            "coincidencias": [],
            "razones": [],
            "sugerencias": []
        }
        
        if valor_requerido not in palabras_clave:
            resultado["razones"].append(f"No se encontraron palabras clave para {valor_requerido} en {nombre_categoria}")
            resultado["sugerencias"].append(f"Asegúrate de que el modelo use referencias a {valor_requerido}")
            return resultado
        
        palabras_requeridas = palabras_clave[valor_requerido]
        coincidencias = []
        
        for palabra in palabras_requeridas:
            if re.search(r'\b' + re.escape(palabra) + r'\b', texto, re.IGNORECASE):
                coincidencias.append(palabra)
        
        resultado["coincidencias"] = coincidencias
        
        # Calcular puntuación basada en coincidencias
        puntuacion_base = (len(coincidencias) / len(palabras_requeridas)) * 100
        resultado["puntuacion"] = min(100, puntuacion_base + 20)  # Bonus por cualquier coincidencia
        
        if len(coincidencias) >= len(palabras_requeridas) * 0.3:  # Al menos 30% de coincidencias
            resultado["cumple"] = True
        else:
            resultado["cumple"] = False
            resultado["razones"].append(
                f"Faltan referencias a {valor_requerido} en la descripción del {nombre_categoria}"
            )
            resultado["sugerencias"].append(
                f"Incluye términos como: {', '.join(palabras_requeridas[:5])} en la descripción"
            )
        
        return resultado
    
    def _evaluar_longitud(self, texto: str) -> Dict:
        """Evalúa que la longitud del texto sea adecuada"""
        
        resultado = {
            "cumple": False,
            "puntuacion": 0,
            "razones": [],
            "sugerencias": []
        }
        
        palabras = len(texto.split())
        
        if 150 <= palabras <= 500:
            resultado["cumple"] = True
            resultado["puntuacion"] = 100
        elif 100 <= palabras < 150:
            resultado["cumple"] = True
            resultado["puntuacion"] = 75
            resultado["sugerencias"].append("El escenario podría ser un poco más detallado")
        elif palabras < 100:
            resultado["cumple"] = False
            resultado["puntuacion"] = 40
            resultado["razones"].append(f"El escenario es demasiado corto ({palabras} palabras)")
            resultado["sugerencias"].append("Genera una descripción más detallada (mínimo 150 palabras)")
        elif palabras > 500:
            resultado["cumple"] = True
            resultado["puntuacion"] = 80
            resultado["sugerencias"].append("El escenario es extenso, considera si es apropiado para tu sesión")
        
        return resultado
    
    def _evaluar_coherencia(self, texto: str) -> Dict:
        """Evalúa la coherencia básica del texto"""
        
        resultado = {
            "cumple": True,
            "puntuacion": 85,
            "razones": [],
            "sugerencias": []
        }
        
        # Verificar repeticiones excesivas
        palabras = texto.lower().split()
        frecuencias = {}
        for palabra in palabras:
            if len(palabra) > 3:
                frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
        
        repeticiones = [p for p, f in frecuencias.items() if f > 5 and len(p) > 3]
        if repeticiones:
            resultado["puntuacion"] -= 15
            resultado["sugerencias"].append("Evita repetir las mismas palabras con frecuencia")
        
        # Verificar longitud de párrafos
        parrafos = texto.split('\n')
        parrafos_largos = [p for p in parrafos if len(p.split()) > 150 and p.strip()]
        if parrafos_largos:
            resultado["puntuacion"] -= 10
            resultado["sugerencias"].append("Divide los párrafos muy largos para mejor legibilidad")
        
        # Verificar que no haya texto vacío o error
        if "error" in texto.lower() or "❌" in texto:
            resultado["cumple"] = False
            resultado["puntuacion"] = 0
            resultado["razones"].append("El texto contiene mensajes de error")
            resultado["sugerencias"].append("Regenera el escenario")
        
        return resultado
    
    def regenerar_si_necesario(self, generador, raza: str, ambiente: str, extension: str, max_intentos: int = 3) -> Tuple[str, Dict]:
        """
        Regenera el escenario hasta que cumpla con los criterios o se alcance el máximo de intentos
        
        Returns:
            Tuple con (texto_generado, evaluacion_final)
        """
        for intento in range(max_intentos):
            print(f"\n🔄 Intento {intento + 1} de {max_intentos}")
            
            # Generar escenario
            texto = generador.generar_descripcion_dnd(raza, ambiente, extension)
            
            # Evaluar
            evaluacion = self.evaluar_escenario(texto, raza, ambiente, extension)
            
            print(f"   Puntuación: {evaluacion['puntuacion']:.1f}%")
            print(f"   Cumple criterios: {'✅' if evaluacion['cumple'] else '❌'}")
            
            if evaluacion["cumple"]:
                print(f"   ✅ Escenario aceptado después de {intento + 1} intentos")
                return texto, evaluacion
            else:
                print(f"   ⚠️ No cumple criterios. Razones:")
                for razon in evaluacion["razones"][:3]:
                    print(f"      - {razon}")
        
        print(f"   ⚠️ Se alcanzó el máximo de intentos. Usando el último escenario generado")
        return texto, evaluacion