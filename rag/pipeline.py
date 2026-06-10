from .retriever import RAGRetriever
from .generator import RAGGenerator
from .evaluator import RAGEvaluator

class RAGPipeline:
    def __init__(self, model="qwen2.5-1.5b", model_path=None, use_gpu=False, auto_evaluar=True, max_intentos=3):
        print(f"\n🎲 Inicializando RAG Pipeline para D&D")
        print(f"   Modelo: {model}")
        print(f"   Auto-evaluación con IA: {'✅ Activada' if auto_evaluar else '❌ Desactivada'}")
        
        self.auto_evaluar = auto_evaluar
        self.max_intentos = max_intentos
        
        self.retriever = RAGRetriever()
        self.generator = RAGGenerator(
            model=model,
            model_path=model_path,
            use_gpu=use_gpu
        )
        
        if auto_evaluar:
            self.evaluator = RAGEvaluator(self.generator)
    
    def generar_escenario(self, raza, ambiente, extension):
        """Genera un escenario completo usando evaluación con IA"""
        print(f"\n🏰 Generando escenario D&D")
        print(f"   Raza: {raza}")
        print(f"   Ambiente: {ambiente}")
        print(f"   Extensión: {extension}")
        
        if self.auto_evaluar and hasattr(self, 'evaluator'):
            # Usar evaluación con IA y corrección automática
            descripcion, evaluacion = self.evaluator.regenerar_si_necesario(
                raza, ambiente, extension, self.max_intentos
            )
            
            # Recuperar contextos
            consulta = f"{raza} {ambiente} {extension}"
            contextos = self.retriever.retrieve(consulta, top_k=3)
            
            return descripcion, contextos, evaluacion
        else:
            # Modo simple sin evaluación
            consulta = f"{raza} {ambiente} {extension}"
            contextos = self.retriever.retrieve(consulta, top_k=3)
            descripcion = self.generator.generar_descripcion_dnd(raza, ambiente, extension)
            return descripcion, contextos, None