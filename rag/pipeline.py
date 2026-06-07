from .retriever import RAGRetriever
from .generator import RAGGenerator

class RAGPipeline:
    def __init__(self, model="qwen2.5-1.5b", model_path=None, use_gpu=False):
        print(f"\n🎲 Inicializando RAG Pipeline para D&D")
        print(f"   Modelo: {model}")
        
        self.retriever = RAGRetriever()
        self.generator = RAGGenerator(
            model=model,
            model_path=model_path,
            use_gpu=use_gpu
        )
    
    def generar_escenario(self, raza, ambiente, extension):
        """Genera un escenario completo usando los selectores"""
        print(f"\n🏰 Generando escenario D&D")
        print(f"   Raza: {raza}")
        print(f"   Ambiente: {ambiente}")
        print(f"   Extensión: {extension}")
        
        # Construir consulta para el retriever
        consulta = f"{raza} {ambiente} {extension}"
        
        # Recuperar contextos relevantes
        contextos = self.retriever.retrieve(consulta, top_k=3)
        textos_contexto = [ctx["contexto"] for ctx in contextos]
        
        # Generar descripción con el modelo
        descripcion = self.generator.generar_descripcion_dnd(
            raza, ambiente, extension
        )
        
        print(f"✅ Escenario generado exitosamente")
        return descripcion, contextos