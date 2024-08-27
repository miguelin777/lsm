from flask import Flask, request, jsonify
import difflib

app = Flask(__name__)

@app.route('/')
def index():
    return open('./chatbot.html').read()

# Diccionario de intenciones y respuestas
intenciones = {
    "¡Hola! ¿En qué puedo ayudarte?": ["Hola", "Buenos días", "Buenas tardes", "Buenas noches", "Saludo"],
    "Adiós, un gusto haberte ayudado. Si tienes alguna otra duda, házmela saber": ["Adiós", "Hasta luego", "Nos vemos", "Chao", "Despedida"],
    "Nuestro número de contacto es 411 127 1872": ["¿Cuál es su número de contacto?", "¿Cómo puedo llamarlos?", "Número de teléfono"],
    "El precio del servicio es de $7,000 - $8,000 MXN": ["¿Cuánto cuesta el servicio?", "¿Cuál es el precio?", "Costo del servicio"],
    "Ofrecemos terapias que pueden adaptarse a tus necesidades y puedes llevarlas a cabo en casa o en nuestro centro": ["¿Ofrecen terapias?", "¿Dónde puedo hacer terapia?", "¿Tienen terapias a domicilio?"],
    "Las terapias se realizan de forma presencial o a través de videollamadas, dependiendo de lo que prefieras": ["¿Cómo se realizan las terapias?", "¿Hay terapias en línea?", "Modalidad de las terapias"],
    "El equipo está compuesto por psicólogos, terapeutas ocupacionales y trabajadores sociales": ["¿Quiénes forman el equipo?", "¿Quién me atenderá?", "Equipo de profesionales"],
    "Tenemos grupos de apoyo y actividades recreativas que pueden ayudarte a conectarte con otros en situaciones similares": ["¿Tienen grupos de apoyo?", "¿Hay actividades en grupo?", "¿Puedo conocer a otros en mi situación?"],
    "Estamos en funcionamiento desde Mayo de 2023": ["¿Desde cuándo operan?", "¿Cuánto tiempo llevan?", "Inicio de operaciones"],
    "Puedes integrarte en diversos programas y actividades diseñados para mejorar tu bienestar y calidad de vida": ["¿Qué programas tienen?", "¿En qué actividades puedo participar?", "Programas y actividades disponibles"],
    "Ofrecemos asistencia en educación especial, actividades recreativas y apoyo en la vida diaria": ["¿Qué tipo de asistencia ofrecen?", "¿Cómo me pueden ayudar?", "Servicios disponibles"],
    "Puedes contactarnos a través de nuestro sitio web, por teléfono o visitando nuestras oficinas": ["¿Cómo puedo contactarlos?", "Formas de contacto", "¿Dónde están ubicados?"],
    "Tenemos recursos y guías para familiares y cuidadores para ayudarles a proporcionar el mejor apoyo posible": ["¿Tienen recursos para familiares?", "¿Cómo pueden ayudar a los cuidadores?", "Apoyo para familiares"],
    "Nuestros servicios están disponibles para todas las edades, desde niños hasta adultos mayores": ["¿Para quiénes son sus servicios?", "¿Atienden a todas las edades?", "¿Quién puede usar sus servicios?"],
    "Ofrecemos evaluaciones iniciales para personalizar el plan de atención según las necesidades individuales": ["¿Cómo es el proceso de evaluación?", "¿Qué necesito para empezar?", "Proceso inicial"],
    "Puedes participar en talleres de habilidades sociales, manejo del estrés y más": ["¿Qué talleres ofrecen?", "¿Tienen talleres?", "Actividades educativas"],
    "Contamos con personal capacitado para brindar atención especializada en salud mental y bienestar": ["¿Quiénes brindan la atención?", "¿Tienen personal capacitado?", "Especialización del personal"],
    "Soy David, tu asistente virtual. ¿En qué puedo ayudarte hoy?": ["¿Cómo te llamas?", "¿Cuál es tu nombre?", "¿Quién eres?"],
    "La Revolución Francesa comenzó en 1789 y fue un periodo de grandes cambios sociales y políticos en Francia": ["¿Cuándo comenzó la Revolución Francesa?", "Cuéntame sobre la Revolución Francesa", "Historia de la Revolución Francesa"],
    "Sócrates fue un filósofo griego clásico, considerado uno de los más grandes de la filosofía occidental": ["¿Quién fue Sócrates?", "Cuéntame sobre Sócrates", "Filosofía de Sócrates"],
    "La Segunda Guerra Mundial comenzó en 1939 y terminó en 1945, involucrando a muchos países de todo el mundo": ["¿Cuándo fue la Segunda Guerra Mundial?", "Información sobre la Segunda Guerra Mundial", "Historia de la Segunda Guerra Mundial"],
    "Platón fue un filósofo griego y discípulo de Sócrates, conocido por sus escritos sobre filosofía y política": ["¿Quién fue Platón?", "Filosofía de Platón", "Cuéntame sobre Platón"],
    "La Independencia de México se celebró el 16 de septiembre de 1810": ["¿Cuándo es la Independencia de México?", "Fecha de la Independencia de México", "Historia de la Independencia de México"],
    "Aristóteles fue un filósofo y científico griego, alumno de Platón y maestro de Alejandro Magno": ["¿Quién fue Aristóteles?", "Filosofía de Aristóteles", "Cuéntame sobre Aristóteles"],
    "La Primera Guerra Mundial tuvo lugar entre 1914 y 1918 y fue un conflicto global centrado en Europa": ["¿Cuándo fue la Primera Guerra Mundial?", "Información sobre la Primera Guerra Mundial", "Historia de la Primera Guerra Mundial"],
    "El Renacimiento fue un movimiento cultural que comenzó en Italia en el siglo XIV y se extendió por toda Europa": ["¿Qué fue el Renacimiento?", "Historia del Renacimiento", "Cuéntame sobre el Renacimiento"],
    "En filosofía, el término 'ética' se refiere al estudio de los valores morales y los principios de la conducta humana": ["¿Qué es la ética?", "Definición de ética", "Cuéntame sobre la ética"],
    "La Revolución Industrial comenzó en el siglo XVIII en Gran Bretaña y transformó la economía y la sociedad": ["¿Cuándo comenzó la Revolución Industrial?", "Historia de la Revolución Industrial", "Cuéntame sobre la Revolución Industrial"],
    "La Declaración de Independencia de los Estados Unidos fue adoptada el 4 de julio de 1776": ["¿Cuándo fue la Declaración de Independencia de los Estados Unidos?", "Fecha de la Independencia de los EE.UU.", "Historia de la Independencia de los EE.UU."],
    "La psicología es la ciencia que estudia la mente y el comportamiento humano": ["¿Qué es la psicología?", "Definición de psicología", "¿Qué estudia la psicología?"],
    "Sigmund Freud es conocido por desarrollar el psicoanálisis, una teoría y terapia para tratar los trastornos mentales": ["¿Quién fue Sigmund Freud?", "Psicoanálisis de Freud", "Teoría de Freud"],
    "La terapia cognitivo-conductual es una forma de tratamiento psicológico que se centra en cambiar patrones de pensamiento y comportamiento": ["¿Qué es la terapia cognitivo-conductual?", "Definición de terapia cognitivo-conductual", "Terapia cognitivo-conductual"],
    "La ansiedad es una emoción caracterizada por sentimientos de tensión, pensamientos preocupantes y cambios físicos como el aumento de la presión arterial": ["¿Qué es la ansiedad?", "Síntomas de ansiedad", "Definición de ansiedad"],
    "La depresión es un trastorno del estado de ánimo que causa una sensación persistente de tristeza y pérdida de interés": ["¿Qué es la depresión?", "Síntomas de depresión", "Definición de depresión"],
    "La esquizofrenia es un trastorno mental grave que afecta la forma en que una persona piensa, siente y se comporta": ["¿Qué es la esquizofrenia?", "Síntomas de esquizofrenia", "Definición de esquizofrenia"],
    "El trastorno bipolar es un trastorno del estado de ánimo que se caracteriza por episodios de manía y depresión": ["¿Qué es el trastorno bipolar?", "Síntomas del trastorno bipolar", "Definición de trastorno bipolar"],
    "La terapia ocupacional ayuda a las personas a desarrollar, recuperar o mantener las habilidades necesarias para la vida diaria y el trabajo": ["¿Qué es la terapia ocupacional?", "Definición de terapia ocupacional", "Beneficios de la terapia ocupacional"],
    "La psicoterapia es un tratamiento colaborativo basado en la relación entre un individuo y un psicólogo, para abordar problemas de salud mental": ["¿Qué es la psicoterapia?", "Definición de psicoterapia", "Beneficios de la psicoterapia"],
    "El trastorno por déficit de atención con hiperactividad (TDAH) es un trastorno del desarrollo neurológico que afecta la atención y el control de impulsos": ["¿Qué es el TDAH?", "Síntomas del TDAH", "Definición de TDAH"],
    "La terapia de exposición es una técnica utilizada en la terapia cognitivo-conductual para ayudar a las personas a enfrentar sus miedos": ["¿Qué es la terapia de exposición?", "Definición de terapia de exposición", "Beneficios de la terapia de exposición"],
    "El mindfulness es una técnica de meditación que se centra en estar presente y consciente del momento actual sin juzgarlo": ["¿Qué es el mindfulness?", "Definición de mindfulness", "Beneficios del mindfulness"],
    "La resiliencia es la capacidad de adaptarse bien a la adversidad, el trauma, la tragedia, las amenazas o fuentes significativas de estrés": ["¿Qué es la resiliencia?", "Definición de resiliencia", "Cómo desarrollar la resiliencia"],
    "La autoestima es la valoración general que una persona tiene de sí misma, influenciada por sus pensamientos, sentimientos y experiencias": ["¿Qué es la autoestima?", "Definición de autoestima", "Importancia de la autoestima"],
    "La terapia de grupo es una forma de psicoterapia en la que un pequeño grupo de personas se reúne bajo la guía de un terapeuta para hablar sobre sus problemas": ["¿Qué es la terapia de grupo?", "Beneficios de la terapia de grupo", "Definición de terapia de grupo"],
    "La terapia de pareja es un tipo de terapia psicológica diseñada para ayudar a las parejas a mejorar su relación": ["¿Qué es la terapia de pareja?", "Beneficios de la terapia de pareja", "Definición de terapia de pareja"],
    "La terapia familiar es una forma de tratamiento diseñada para abordar problemas específicos que afectan la salud y el funcionamiento de una familia": ["¿Qué es la terapia familiar?", "Beneficios de la terapia familiar", "Definición de terapia familiar"]
}

def get_response(texto):
    texto = texto.lower()
    mejor_coincidencia = None
    mejor_ratio = 0

    for intencion, respuestas in intenciones.items():
        for respuesta in respuestas:
            ratio = difflib.SequenceMatcher(None, texto, respuesta.lower()).ratio()
            if ratio > mejor_ratio:
                mejor_ratio = ratio
                mejor_coincidencia = intencion

    if mejor_ratio > 0.4:
        return mejor_coincidencia
    else:
        return "Lo siento, no entiendo tu pregunta."

@app.route('/get-response', methods=['POST'])
def get_bot_response():
    user_input = request.json['message']
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
