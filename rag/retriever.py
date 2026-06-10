# Retriever simplificado - contextos predefinidos para D&D

class RAGRetriever:
    def __init__(self):
        print("🎲 Inicializando Retriever para D&D")
        self.contextos_dnd = self._cargar_contextos_dnd()
    
    def _cargar_contextos_dnd(self):
        """Carga contextos predefinidos para D&D para todas las razas y ambientes"""
        return {
            # ==================== RAZAS ====================
            "humanos": "Los humanos son adaptables y construyen civilizaciones diversas. Son conocidos por su ambición, su capacidad para unirse contra amenazas comunes y su tendencia a expandir sus territorios. Los reinos humanos suelen tener sistemas feudales, monarquías o repúblicas mercantiles.",
            
            "elfos": "Los elfos son seres mágicos y longevos que viven en armonía con la naturaleza. Tienen una conexión profunda con el mundo feérico y son excelentes arqueros, magos y artistas. Valoran la belleza, el arte y la tradición ancestral.",
            
            "alto elfo": "Los Altos Elfos son la élite de la sociedad élfica. Son más altos, más justos y más poderosos mágicamente que sus parientes. Habitan en ciudades de cristal y marfil en bosques ancestrales, gobernados por nobles casas que remontan su linaje milenios atrás.",
            
            "enanos": "Los enanos son maestros artesanos que viven bajo las montañas. Valoran el honor, la familia, los tesoros minerales y la artesanía perfecta. Sus reinos subterráneos son fortalezas inexpugnables llenas de grandes salas, forjas humeantes y pasadizos secretos.",
            
            "enano del valle": "Los Enanos del Valle son más adaptables que sus primos de la montaña. Viven en colinas y valles fértiles, combinando la artesanía enana con la agricultura y el comercio. Son más abiertos a los forasteros y suelen tener relaciones comerciales con otras razas.",
            
            "orcos": "Los orcos son guerreros feroces que valoran la fuerza bruta por encima de todo. Viven en tribus nómadas que recorren tierras agrestes, liderados por el más fuerte. Respetan el poder y la habilidad en combate más que cualquier otra cualidad.",
            
            "medio orco": "Los Medios Orcos son hijos de humanos y orcos, viviendo entre dos mundos. Heredan la fuerza de sus ancestros orcos y la astucia de sus ancestros humanos. Suelen ser marginados pero demuestran su valía como feroces guerreros o líderes pragmáticos.",
            
            "duendes": "Los Gnomos son inventores y alquimistas brillantes. Viven en comunidades subterráneas o en bosques, siempre experimentando con nuevas creaciones. Su curiosidad insaciable y su optimismo los llevan a crear artefactos maravillosos y a veces peligrosos.",
            
            "duende de roca": "Los Gnomos de Roca viven bajo las montañas y son expertos en joyería, mecánica y alquimia. Son los más prácticos de los gnomos, creando dispositivos ingeniosos y gemas mágicas. Valoran la tradición y el conocimiento transmitido por generaciones.",
            
            "halflings": "Los Halflings son una raza pequeña, alegre y hospitalaria. Prefieren una vida tranquila en pueblos agrícolas, valorando la comida, la amistad y las pequeñas aventuras. Son increíblemente afortunados y difíciles de atrapar cuando no quieren ser encontrados.",
            
            "medio elfo": "Los Medios Elfos combinan la gracia élfica con la ambición humana. Se sienten atraídos por las ciudades humanas donde su herencia élfica les da ventaja social, pero también valoran la conexión con la naturaleza. Son diplomáticos natos y adaptables.",
            
            "tieflings": "Los Tieflings tienen sangre infernal que marca su apariencia con cuernos, colas o ojos sin pupilas. Son marginados por su herencia pero desarrollan una gran determinación. Muchos se convierten en hechiceros, brujos o pícaros que desafían las expectativas.",
            
            "dragonborns": "Los Dragonborns son humanoides dragónicos orgullosos de su herencia. Valoran el honor, la lealtad y la fuerza. Sus clanes están organizados en castas, y cada miembro busca demostrar su valor para honrar a sus ancestros dragón.",
            
            "tritones": "Los Tritones son habitantes de las profundidades oceánicas. Son nobles guerreros que protegen los mares de amenazas como sahuagines y krakens. En tierra son torpes y desconfiados, pero en el agua son ágiles y poderosos.",
            
            # ==================== AMBIENTES NATURALES ====================
            "bosques": "Los bosques están llenos de vida y misterio. Los árboles antiguos ocultan secretos druídicos, criaturas feéricas y ruinas olvidadas. Son reinos de elfos, dríadas y bestias mágicas, donde cada claro puede esconder una maravilla o un peligro.",
            
            "montañas": "Las montañas son lugares peligrosos pero ricos en minerales. Sus picos nevados y profundas cavernas albergan enanos, gigantes, dragones y criaturas de las profundidades. Los pasos son traicioneros y los deslizamientos de roca son comunes.",
            
            "desiertos": "Los desiertos son implacables pero esconden ruinas antiguas y tesoros olvidados bajo la arena. Tribus nómadas recorren las dunas, y criaturas como dragones azules o lamias acechan en templos enterrados. Las noches son frías y los días abrasadores.",
            
            "junglas": "Las junglas son densas y húmedas, llenas de vida en cada hoja. Ruinas cubiertas de musgo albergan trampas mortales y artefactos poderosos. Tabaxi, yuan-ti y dinosaurios habitan entre la vegetación. Cada paso puede revelar una criatura que acecha.",
                        
            "cuevas": "Las cuevas son oscuras y húmedas, llenas de estalactitas y pasadizos que se bifurcan. Murciélagos, goblins, trogloditas y criaturas olvidadas acechan en las profundidades. Cada esquina puede revelar un tesoro o una muerte segura.",
            
            "pantanos": "Los pantanos son lugares tristes y enfermos, llenos de niebla venenosa y aguas estancadas. Brujas, hags y criaturas no muertas acechan entre los cipreses. Cada paso puede hundirte en el barro o despertar algo que debería haber quedado dormido.",
            
            "praderas": "Las praderas son extensiones de hierba dorada que se mecen con el viento. Tribus nómadas recorren la llanura cazando bisontes enormes. Los centauros galopan libres y las tormentas eléctricas barren el horizonte sin previo aviso.",
            
            "tundra": "La tundra es un páramo helado donde la supervivencia es una lucha constante. El viento corta como cuchillas y la nieve cubre ruinas de civilizaciones olvidadas. Yetis, osos polares y pueblos bárbaros resisten el frío implacable.",
            
            "costas": "Las costas son donde la tierra se encuentra con el mar. Acantilados escarpados, calas escondidas y puertos bulliciosos. Sirenas, piratas y criaturas marinas acechan entre las olas, mientras los pescadores cuentan historias de tormentas y naufragios.",
            
            # ==================== AMBIENTES TEMÁTICOS ====================
            "steampunk": "En este mundo steampunk, el vapor y los engranajes son la base de la tecnología. Dirigibles surcan los cielos y autómatas realizan trabajos pesados. La aristocracia vive en mansiones victorianas mientras los trabajadores se hacinan en barrios industriales llenos de humo. La magia se canaliza a través de artefactos mecánicos.",
            
            "postapocaliptico": "Un mundo devastado donde restos de civilizaciones antiguas yacen entre desiertos radiactivos. Los sobrevivientes luchan por recursos básicos mientras mutantes y máquinas olvidadas acechan en las ruinas. La magia salvaje distorsiona la realidad en zonas contaminadas.",
            
            "gotico": "Un mundo de castillos en ruinas, bosques neblinosos y oscuros secretos. Vampiros, hombres lobo y seres malditos acechan en la noche. La iglesia lucha contra lo sobrenatural mientras la nobleza decadente oculta terribles crímenes. La tristeza y la melancolía impregnan el ambiente.",
            
            "medieval": "Un mundo de castillos feudales, caballeros andantes y siervos de la gleba. La iglesia tiene un poder absoluto sobre las almas. Los bosques están llenos de bandidos, bestias y brujas. Las cruzadas y las guerras señoriales son constantes. La peste y el hambre acechan en cada invierno.",
            
            "japones feudal": "Tierras de samuráis, monjes guerreros y demonios. Castillos de madera se alzan sobre pueblos que cultivan arroz. Los señores feudales luchan por el poder mientras los shinobi ejecutan misiones secretas. Los kami y yokai habitan en bosques y montañas sagradas.",
            
            "cristal": "Cavernas maravillosas donde cristales gigantes emiten luz propia. Las formaciones minerales crean paisajes oníricos de colores brillantes. Habitan gnomos, elementales de tierra y criaturas que se alimentan de energía geomántica. El eco distorsiona el sonido y la magia se siente más potente.",
            
            "flotante": "Islas que desafían la gravedad suspendidas sobre un abismo infinito. Se conectan mediante puentes de cuerda o vuelos cortos. Habitan aarakocra, magos poderosos y criaturas aladas. El viento es constante y caer del borde es una muerte segura.",
            
            "volcanico": "Tierras de ceniza, ríos de lava y montañas que escupen fuego. Los cultistas adoran a elementales de fuego y dragones rojos. Los asentamientos se protegen en cuevas ignífugas. La agricultura es imposible pero los minerales son abundantes."
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
        
        # Si hay múltiples resultados, limitar a top_k
        if resultados:
            return resultados[:top_k]
        
        # Si no hay resultados específicos, devolver contextos generales
        generales = [
            {"id": "general1", "score": 0.5, "contexto": "En D&D, los escenarios pueden variar desde mazmorras oscuras hasta reinos mágicos. Cada ambiente tiene sus propias reglas y habitantes que moldean la vida en el lugar."},
            {"id": "general2", "score": 0.5, "contexto": "Los Dungeon Masters deben crear descripciones atmosféricas para inmersión, considerando la política local, economía y relaciones entre facciones."},
            {"id": "general3", "score": 0.5, "contexto": "La geografía, el clima y las criaturas nativas definen las oportunidades y peligros de un territorio para los aventureros."}
        ]
        
        return generales[:top_k]