# Retriever simplificado - como no tenemos base de datos de canciones,
# este retriever usa contexto predefinido para D&D

class RAGRetriever:
    def __init__(self):
        print("🎲 Inicializando Retriever para D&D")
        self.contextos_dnd = self._cargar_contextos_dnd()
    
    def _cargar_contextos_dnd(self):
        """Carga contextos predefinidos para D&D"""
        return {
            "humanos": "Los humanos son adaptables y construyen civilizaciones diversas. Son conocidos por su ambición y capacidad para unirse contra amenazas comunes.",
            "elfos": "Los elfos son seres mágicos que viven en armonía con la naturaleza. Tienen una conexión profunda con el mundo feérico y son excelentes arqueros y magos.",
            "enanos": "Los enanos son maestros artesanos que viven bajo las montañas. Valoran el honor, la familia y los tesoros minerales.",
            "orcos": "Los orcos son guerreros feroces que valoran la fuerza bruta. Viven en tribus nómadas y respetan solo al más fuerte.",
            "dragones": "Los dragones son criaturas ancestrales de gran poder. Acumulan tesoros y son temidos por toda la tierra.",
            "bosques": "Los bosques están llenos de vida y misterio. Los árboles antiguos ocultan secretos druídicos y criaturas feéricas.",
            "montañas": "Las montañas son lugares peligrosos pero ricos en minerales. Habitadas por enanos, gigantes y dragones.",
            "desiertos": "Los desiertos son implacables pero esconden ruinas antiguas y tesoros olvidados bajo la arena.",
            "ciudades": "Las ciudades son centros de comercio e intriga. Gremios, templos y tabernas ofrecen tanto peligros como oportunidades."
        }
    
    def retrieve(self, query, top_k=3):
        """Recupera contextos relevantes para la consulta"""
        resultados = []
        
        # Extraer palabras clave de la consulta
        query_lower = query.lower()
        
        for clave, contexto in self.contextos_dnd.items():
            if clave in query_lower:
                resultados.append({
                    "id": clave,
                    "score": 1.0,
                    "contexto": contexto
                })
        
        # Si no hay resultados específicos, devolver contextos generales
        if not resultados:
            generales = [
                {"id": "general1", "score": 0.5, "contexto": "En D&D, los escenarios pueden variar desde mazmorras oscuras hasta reinos mágicos."},
                {"id": "general2", "score": 0.5, "contexto": "Los Dungeon Masters deben crear descripciones atmosféricas para inmersión."}
            ]
            resultados = generales[:top_k]
        
        return resultados[:top_k]