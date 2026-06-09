from typing import Dict, Tuple

class RAGEvaluator:
    """Evaluador de escenarios D&D que usa el mismo modelo para evaluar y corregir"""
    
    def __init__(self, generator):
        self.generator = generator
        print("🎲 Inicializando Evaluador de Escenarios D&D con IA")
    
    def evaluar_escenario(self, texto: str, raza: str, ambiente: str, extension: str) -> Dict:
        """
        Usa el modelo para evaluar si el escenario cumple con las características requeridas
        """
        
        prompt_evaluacion = f"""Evalúa la siguiente descripción de un escenario de Dungeons & Dragons y determina si cumple con los requisitos.

Características requeridas:
- Raza predominante: {raza}
- Ambiente: {ambiente}
- Extensión: {extension}

DESCRIPCIÓN A EVALUAR:
{texto}

INSTRUCCIONES DE EVALUACIÓN:
Analiza la descripción y responde SOLO con un JSON válido en este formato exacto:
{{
    "cumple": true/false,
    "puntuacion": (número entre 0 y 100),
    "raza_cumple": true/false,
    "ambiente_cumple": true/false,
    "extension_cumple": true/false,
    "longitud_adecuada": true/false,
    "texto_completo": true/false,
    "problemas": ["problema1", "problema2"],
    "sugerencias": ["sugerencia1", "sugerencia2"]
}}

Criterios de evaluación:
1. ¿La descripción menciona adecuadamente la raza {raza} y sus características?
2. ¿El ambiente {ambiente} está bien representado?
3. ¿La extensión {extension} es apropiada para el nivel de detalle?
4. ¿El texto está completo (no cortado a mitad)?
5. ¿La calidad narrativa es buena para D&D?

Sé estricto pero justo. Si el texto está cortado o incompleto, marca "texto_completo": false.
Si la puntuación es menor a 70, considera que no cumple."""
        
        try:
            # Usar el mismo modelo para evaluar con temperatura baja para consistencia
            respuesta = self.generator._generate(prompt_evaluacion, max_tokens=500, temperature=0.2)
            
            # Extraer JSON de la respuesta
            import json
            import re
            
            # Buscar JSON en la respuesta
            json_match = re.search(r'\{[^{}]*\{[^{}]*\}[^{}]*\}|{[^{}]*}', respuesta, re.DOTALL)
            if json_match:
                evaluacion = json.loads(json_match.group())
            else:
                # Si no encuentra JSON, crear evaluación por defecto
                evaluacion = self._evaluacion_por_defecto(texto, raza, ambiente, extension)
            
            return evaluacion
            
        except Exception as e:
            print(f"   ⚠️ Error en evaluación con IA: {e}")
            return self._evaluacion_por_defecto(texto, raza, ambiente, extension)
    
    def _evaluacion_por_defecto(self, texto: str, raza: str, ambiente: str, extension: str) -> Dict:
        """Evaluación de respaldo por si falla la IA"""
        palabras = len(texto.split())
        
        # Verificar si el texto parece cortado
        texto_completo = texto.endswith(('.', '!', '?', '"', "'")) and not texto.endswith((' y ', ' o ', ' pero '))
        
        return {
            "cumple": palabras > 100 and texto_completo,
            "puntuacion": min(100, max(0, (palabras / 200) * 100)) if texto_completo else 40,
            "raza_cumple": raza.lower() in texto.lower(),
            "ambiente_cumple": ambiente.lower() in texto.lower(),
            "extension_cumple": extension.lower() in texto.lower(),
            "longitud_adecuada": palabras > 100,
            "texto_completo": texto_completo,
            "problemas": ["Texto incompleto" if not texto_completo else "Longitud insuficiente" if palabras < 100 else ""],
            "sugerencias": ["Completa la descripción" if not texto_completo else "Añade más detalles" if palabras < 100 else ""]
        }
    
    def corregir_escenario(self, texto: str, raza: str, ambiente: str, extension: str, problemas: list) -> str:
        """
        Usa el modelo para corregir el escenario basado en los problemas detectados
        """
        
        prompt_correccion = f"""La siguiente descripción de un escenario de D&D necesita mejoras.

CARACTERÍSTICAS REQUERIDAS:
- Raza: {raza}
- Ambiente: {ambiente}
- Extensión: {extension}

DESCRIPCIÓN ACTUAL:
{texto}

PROBLEMAS DETECTADOS:
{chr(10).join(f'- {p}' for p in problemas if p)}

INSTRUCCIONES DE CORRECCIÓN:
1. Completa el texto si está cortado o incompleto
2. Añade más detalles sobre la raza {raza} y su cultura
3. Enriquece la descripción del ambiente {ambiente}
4. Ajusta el nivel de detalle para que sea apropiado para un {extension}
5. Mantén el mismo tono y estilo narrativo
6. NO incluyas la palabra "EDITADO:" ni "CORREGIDO:" en la respuesta
7. Responde SOLO con el texto corregido, sin explicaciones adicionales

Genera la versión mejorada de la descripción:"""
        
        try:
            # Usar temperatura ligeramente más alta para creatividad en corrección
            texto_corregido = self.generator._generate(prompt_correccion, max_tokens=800, temperature=0.6)
            
            # Limpiar el resultado si es necesario
            if texto_corregido.startswith('"') and texto_corregido.endswith('"'):
                texto_corregido = texto_corregido[1:-1]
            
            return texto_corregido.strip()
            
        except Exception as e:
            print(f"   ⚠️ Error en corrección con IA: {e}")
            return texto  # Devolver el original si falla
    
    def regenerar_si_necesario(self, raza: str, ambiente: str, extension: str, max_intentos: int = 3) -> Tuple[str, Dict]:
        """
        Regenera y evalúa el escenario hasta que cumpla con los criterios
        """
        texto = None
        evaluacion = None
        
        for intento in range(max_intentos):
            print(f"\n🔄 Intento {intento + 1} de {max_intentos}")
            
            if intento == 0:
                # Primera generación normal
                texto = self.generator.generar_descripcion_dnd(raza, ambiente, extension)
            else:
                # Intentos siguientes: corregir el texto anterior
                if evaluacion and evaluacion.get("problemas"):
                    print(f"   🔧 Corrigiendo escenario basado en evaluación...")
                    texto = self.corregir_escenario(texto, raza, ambiente, extension, evaluacion.get("problemas", []))
                else:
                    # Si no hay problemas específicos, regenerar desde cero con temperatura diferente
                    print(f"   🎲 Regenerando con temperatura ajustada...")
                    texto = self.generator.generar_descripcion_dnd(raza, ambiente, extension, temperature=0.8)
            
            # Evaluar el texto generado
            evaluacion = self.evaluar_escenario(texto, raza, ambiente, extension)
            
            print(f"   📊 Puntuación: {evaluacion.get('puntuacion', 0):.1f}%")
            print(f"   📝 Completo: {'✅' if evaluacion.get('texto_completo', False) else '❌'}")
            print(f"   🎯 Cumple requisitos: {'✅' if evaluacion.get('cumple', False) else '❌'}")
            
            if evaluacion.get("texto_completo", False):
                print(f"   ✅ Texto completo detectado")
            
            if evaluacion.get("cumple", False):
                print(f"   ✅ Escenario aceptado después de {intento + 1} intentos")
                return texto, evaluacion
            else:
                problemas = evaluacion.get("problemas", [])
                if problemas:
                    print(f"   ⚠️ Problemas detectados:")
                    for problema in problemas[:3]:
                        print(f"      - {problema}")
        
        print(f"   ⚠️ Se alcanzó el máximo de intentos. Usando el último escenario generado")
        return texto, evaluacion