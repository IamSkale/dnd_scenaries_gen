import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False
    print("⚠️ llama-cpp-python no instalado. Ejecuta: pip install llama-cpp-python")


class RAGGenerator:
    # Opciones de modelo para D&D
    MODEL_OPTIONS = {
        "qwen2.5-3b": {
            "name": "Qwen2.5-3B-Instruct",
            "gguf": "qwen2.5-3b-instruct-q4_k_m.gguf",
            "hf_id": "Qwen/Qwen2.5-3B-Instruct-GGUF",
            "context": 32768,
            "ram_gb": 3,
        },
        "qwen2.5-1.5b": {
            "name": "Qwen2.5-1.5B-Instruct",
            "gguf": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
            "hf_id": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
            "context": 32768,
            "ram_gb": 2,
        }
    }
    
    def __init__(self, model="qwen2.5-3b", model_path=None, use_gpu=False):
        self.model_name = model
        self.model = None
        self.use_gpu = use_gpu
        
        if model_path:
            self.model_path = Path(model_path)
        else:
            model_info = self.MODEL_OPTIONS.get(model, self.MODEL_OPTIONS["qwen2.5-3b"])
            self.model_path = Path("models") / model_info["gguf"]
            self.model_info = model_info
        
        print(f"\n🎲 Inicializando generador D&D con {self.model_info['name']}")
        print(f"   Model path: {self.model_path}")
        print(f"   GPU activada: {use_gpu}")
        
        self._cargar_modelo()

    def _cargar_modelo(self):
        if not LLAMA_AVAILABLE:
            print("⚠️ llama-cpp-python no instalado")
            return False
            
        try:
            if not self.model_path.exists():
                print(f"❌ Modelo no encontrado: {self.model_path}")
                print(f"\n📥 Para descargar el modelo:")
                print(f"   mkdir -p models")
                print(f"   cd models")
                print(f"   wget https://huggingface.co/{self.model_info['hf_id']}/resolve/main/{self.model_info['gguf']}")
                return False
            
            print(f"   📂 Cargando modelo...")
            
            n_gpu_layers = -1 if self.use_gpu else 0
            
            self.model = Llama(
                model_path=str(self.model_path),
                n_ctx=self.model_info.get("context", 8192),
                n_threads=4,
                n_gpu_layers=n_gpu_layers,
                verbose=False,
                seed=42,
            )
            print(f"   ✅ Modelo cargado exitosamente")
            return True
            
        except Exception as e:
            print(f"   ❌ Error cargando modelo: {e}")
            return False

    def generar_descripcion_dnd(self, raza, ambiente, extension, max_tokens=500, temperature=0.7):
        """Genera una descripción de escenario D&D basada en los selectores"""
        
        # Construir prompt específico para D&D
        prompt = self._build_dnd_prompt(raza, ambiente, extension)
        
        if self.model:
            try:
                response = self._generate(prompt, max_tokens, temperature)
                if response:
                    print(f"✅ Descripción D&D generada exitosamente")
                    return response
            except Exception as e:
                print(f"❌ Error generando: {e}")
        
        # Fallback si no hay modelo
        return self._fallback_descripcion(raza, ambiente, extension)
    
    def _generate(self, prompt, max_tokens, temperature):
        """Genera respuesta usando el modelo"""
        formatted_prompt = self._format_prompt(prompt)
        
        response = self.model(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["<|im_end|>", "<|endoftext|>"],
            echo=False,
        )
        
        return response['choices'][0]['text'].strip()
    
    def _format_prompt(self, user_message):
        """Formatea el prompt para Qwen"""
        return f"""<|im_start|>system
Eres un Dungeon Master experto en Dungeons & Dragons. Creas descripciones inmersivas y detalladas de escenarios para aventuras. Tus descripciones son evocadoras, atmosféricas y útiles para el juego.<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
"""
    
    def _build_dnd_prompt(self, raza, ambiente, extension):
        """Construye el prompt para el modelo"""
        return f"""Crea una descripción épica y detallada para un escenario de Dungeons & Dragons con estas características:

🏰 Raza predominante: {raza}
🌍 Ambiente: {ambiente}
🗺️ Extensión: {extension}

La descripción debe:
1. Pintar una imagen vívida del lugar (atmósfera, clima, geografía)
2. Explicar cómo la raza {raza} ha influenciado y moldeado este territorio
3. Incluir posibles puntos de interés, peligros o encuentros para los aventureros
4. Mencionar elementos únicos de este {extension} de {ambiente}
5. Tener un tono inmersivo y apropiado para D&D (2-3 párrafos)

Genera una descripción que un Dungeon Master pueda leer directamente en una sesión de juego:"""
    
    def _fallback_descripcion(self, raza, ambiente, extension):
        """Descripciones de respaldo cuando el modelo no está disponible"""
        
        biblioteca_descripciones = {
            "humanos": f"🏰 **El {extension} de {ambiente}**\n\nLas caravanas comerciales recorren los caminos de este territorio humano, donde castillos y aldeas salpican el paisaje. Los mercaderes ofrecen mercancías exóticas, mientras que los guardias patrullan las murallas protegiéndose de bandidos y monstruos. En las tabernas, los aventureros escuchan rumores sobre tesoros perdidos y mazmorras olvidadas.\n\n⚠️ **Posibles encuentros**: Bandidos en los caminos, gremios de ladrones en las ciudades, y bestias que atacan los rebaños.",
            
            "elfos": f"🧝 **El {extension} de {ambiente} élfico**\n\nEntre los antiguos árboles, luces mágicas parpadean como estrellas caídas. Los elfos han esculpido sus hogares en la madera viva, creando una ciudad que respira con el bosque. Puentes de cuerda conectan plataformas elevadas, y el canto de los bardos elfos se mezcla con el susurro de las hojas. Los visitantes deben demostrar respeto por la naturaleza para ser bienvenidos.\n\n⚠️ **Posibles encuentros**: Guardianes del bosque, criaturas feéricas y druidas protectores.",
            
            "enanos": f"⛏️ **El {extension} de {ambiente} enano**\n\nBajo la montaña, martillos resuenan contra el metal en interminables forjas. Grandes salas de piedra tallada albergan estatuas de héroes ancestrales, mientras ríos de lava iluminan pasadizos secretos. Los enanos comercian con gemas preciosas y armaduras de calidad legendaria, pero desconfían de los forasteros que se aventuran demasiado cerca de sus tesoros.\n\n⚠️ **Posibles encuentros**: Duergar en las profundidades, trampas enanas y criaturas de la oscuridad.",
            
            "orcos": f"👹 **El {extension} de {ambiente} orco**\n\nHogueras humeantes marcan los campamentos orcos que se extienden por este territorio agreste. Los guerreros pisan fuerte, probando su fuerza en combates rituales mientras los chamanes invocan a espíritus salvajes. Los no orcos rara vez son bienvenidos, y solo los más fuertes sobreviven el tiempo suficiente para ganarse un respeto rudimentario.\n\n⚠️ **Posibles encuentros**: Patrullas orcas, bestias de guerra y trampas de caza.",
            
            "dragones": f"🐉 **El {extension} de {ambiente} dragón**\n\nLas montañas humean donde el dragón duerme, y los lugareños evitan este lugar maldito. Leyendas hablan de un antiguo wyrm que exige tributo a quienes cruzan su territorio. A veces, su sombra oscurece el sol, y su rugido hace temblar la tierra. Aventureros codiciosos buscan su tesoro, pero pocos regresan para contar la historia.\n\n⚠️ **Posibles encuentros**: El dragón mismo, sus secuaces kobolds y peligros ambientales."
        }
        
        descripcion = biblioteca_descripciones.get(raza, f"📖 **El {extension} de {ambiente}**\n\nUn territorio misterioso dominado por los {raza}. Los viajeros cuentan historias de maravillas y peligros en igual medida. Quienes se aventuran aquí deben prepararse para lo inesperado.\n\n⚠️ **Posibles encuentros**: Criaturas locales, trampas naturales y habitantes desconfiados.")
        
        return descripcion