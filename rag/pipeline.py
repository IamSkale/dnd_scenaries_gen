from .retriever import RAGRetriever
from .generator import RAGGenerator
from .evaluator import RAGEvaluator

class RAGPipeline:
    def __init__(self, model="qwen2.5-1.5b", model_path=None, use_gpu=False, auto_evaluar=True, max_intentos=3):
        print(f"\n🎲 Inicializando RAG Pipeline para D&D")
        print(f"   Modelo: {model}")
        print(f"   Auto-evaluación: {'✅ Activada' if auto_evaluar else '❌ Desactivada'}")
        
        self.auto_evaluar = auto_evaluar
        self.max_intentos = max_intentos
        
        self.retriever = RAGRetriever()
        self.generator = RAGGenerator(
            model=model,
            model_path=model_path,
            use_gpu=use_gpu
        )
        
        if auto_evaluar:
            self.evaluator = RAGEvaluator()
    
    def generar_escenario(self, raza, ambiente, extension):
        """Genera un escenario completo usando los selectores con evaluación automática"""
        print(f"\n🏰 Generando escenario D&D")
        print(f"   Raza: {raza}")
        print(f"   Ambiente: {ambiente}")
        print(f"   Extensión: {extension}")
        
        if self.auto_evaluar and hasattr(self, 'evaluator'):
            # Usar evaluación automática con regeneración
            descripcion, evaluacion = self.evaluator.regenerar_si_necesario(
                self.generator, raza, ambiente, extension, self.max_intentos
            )
            
            # Mostrar resumen de evaluación
            print(f"\n📊 Resumen de evaluación final:")
            print(f"   Puntuación total: {evaluacion['puntuacion']:.1f}%")
            print(f"   - Raza: {evaluacion['detalles']['raza']['puntuacion']:.0f}%")
            print(f"   - Ambiente: {evaluacion['detalles']['ambiente']['puntuacion']:.0f}%")
            print(f"   - Extensión: {evaluacion['detalles']['extension']['puntuacion']:.0f}%")
            print(f"   - Longitud: {evaluacion['detalles']['longitud']['puntuacion']:.0f}%")
            print(f"   - Coherencia: {evaluacion['detalles']['coherencia']['puntuacion']:.0f}%")
            
            # Recuperar contextos (opcional)
            consulta = f"{raza} {ambiente} {extension}"
            contextos = self.retriever.retrieve(consulta, top_k=3)
            
            return descripcion, contextos, evaluacion
        else:
            # Modo simple sin evaluación
            consulta = f"{raza} {ambiente} {extension}"
            contextos = self.retriever.retrieve(consulta, top_k=3)
            descripcion = self.generator.generar_descripcion_dnd(raza, ambiente, extension)
            return descripcion, contextos, None