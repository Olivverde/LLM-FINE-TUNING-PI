from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import openai

app = Flask(__name__)

openai.api_key='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'

def legal_sus(req):
    model_engine = "gpt-3.5-turbo-0125"
    system_prompt = 'Identifica si se trata de una consulta/caso con potencial relación a la ley de propiedad intelectual en guatemala, si es así, responde unicamente con un SI, de lo contrario con un NO'
    try:
        completion = openai.ChatCompletion.create(model=model_engine,#ft:gpt-3.5-turbo-0125:personal::9HlXk9TZ
                                            messages=[{'role':'system', 'content':system_prompt},
                                                {'role':'user','content':req}])

        answer = completion['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"
    

def help(req):
    model_engine = "gpt-3.5-turbo-0125"
    system_prompt = 'Identifica si el usuario busca ayuda o colocó "HELP" en el chat. Si es así, explicale que eres un chatbot que está para ayudarlo a encontrar los fragmentos de ley  relacionados a la ley de propiedad intelectual en guatemala. Si no identificas explicitamente ayuda, retorna NO '
    try:
        completion = openai.ChatCompletion.create(model=model_engine,#ft:gpt-3.5-turbo-0125:personal::9HlXk9TZ
                                            messages=[{'role':'system', 'content':system_prompt},
                                                {'role':'user','content':req}])

        answer = completion['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"

def non_legal_response(req):
    model_engine = "gpt-3.5-turbo-0125"
    system_prompt = 'Esta no es una consulta legal sobre la ley de propiedad intelectual en guatemala. Agradecele por su preferencia y comunicación, si es necesario saluda, y luego responde que solo puedes chatear sobre la ley de propiedad intelectual en guatemala. Además, indicale al usuario que si necesita ayuda para hacer consultas respecto a la ley de propiedad intelectual en guatemala coloque HELP en el chat'
    try:
        completion = openai.ChatCompletion.create(model=model_engine,#ft:gpt-3.5-turbo-0125:personal::9HlXk9TZ
                                            messages=[{'role':'system', 'content':system_prompt},
                                                {'role':'user','content':req}])

        answer = completion['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"

def justify(req, case):
    model_engine = "gpt-3.5-turbo-0125"
    system_prompt = 'esto es una respuesta tuya, encontrarás la ubicación de un fragmento de ley con algunas palabras claves del fragmento, y el caso. Retorna unicamente la justificación de porque crees que se relaciona el fragmento de ley con el caso'
    try:
        completion = openai.ChatCompletion.create(model=model_engine,#ft:gpt-3.5-turbo-0125:personal::9HlXk9TZ
                                            messages=[{'role':'system', 'content':system_prompt},
                                                {'role':'user','content':'respuesta: '+req+'\n caso'+case}])

        answer = completion['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"

def generate_answer(report):
    model_engine = "ft:gpt-3.5-turbo-0125:personal::9HlXk9TZ"
    system_prompt = "dado el siguiente caso, clasifica en alguna de estas categorias:  \n- titulo 2 capitulo 1 seccion 1 : marcas: normas, adquisicion, prioridad, derechos, inadmisibilidad en guatemala\n- titulo 2 capitulo 1 seccion 2 : registro de marcas: requisitos, procedimientos y efectos legales especificos\n- titulo 2 capitulo 1 seccion 3-5 : renovacion, correccion, limitacion, derechos y licencia en marcas registradas.\n- titulo 2 capitulo 2 no seccion : normas aplicables, solicitud, reglamento, examen, registro, cambios, licencia, uso.\n- titulo 2 capitulo 3 no seccion : normas, titularidad, registro, vigencia, uso, gravamen, enajenacion, reserva, extinguida.\n- titulo 2 capitulo 4-6 no seccion : extincion: vencimiento, caducidad, cancelacion, generizacion, falta de uso, sentencia.\n- titulo 2 capitulo 8 seccion 1 y 2 : proteccion de indicaciones geograficas y denominaciones de origen en guatemala.\n- titulo 3 capitulo 1 seccion 1 : proteccion legal para invenciones; requisitos y derechos del inventor.\n- titulo 3 capitulo 1 seccion 2 : tramite, prioridad, examen, requisitos, solicitud, invencion, descripcion, publicacion, resolucion, certificado.\n- titulo 3 capitulo 1 seccion 3 y 4 : division, modificacion, conversion, correccion, enajenacion, vigencia, ajuste, proteccion, limitaciones, agotamiento.\n- titulo 3 capitulo 1 seccion 5-7 : licencias contractuales y obligatorias para explotar patentes segun disposiciones legales.\n- titulo 4 capitulo 1-3 no seccion : registro publico de propiedad intelectual; tasas y clasificaciones definidas.\n- titulo 5 capitulo unico no seccion : represion de competencia desleal: actos prohibidos y proteccion de secretos.\n- titulo 6 capitulo 1 no seccion : proteccion judicial y medidas contra la competencia desleal.\n- titulo 6 capitulo 2 seccion 1 y 2 : procedimientos legales para proteger derechos industriales y combatir competencia desleal en guatemala.\n- titulo 6 capitulo 2 seccion 3-5 : acciones legales para proteger derechos industriales y combatir competencia desleal en guatemala.\n- titulo 6 capitulo 3 no seccion : acciones penales y medidas cautelares en casos de infracciones a la propiedad industrial en guatemala'\n- titulo 7 capitulo 1 y 2 no seccion : disposiciones transitorias y finales para la implementacion de la ley de propiedad industrial en guatemala."

    try:
        completion = openai.ChatCompletion.create(model=model_engine,#ft:gpt-3.5-turbo-0125:personal::9HlXk9TZ
                                            messages=[{'role':'system', 'content':system_prompt},
                                                {'role':'user','content':report}])

        answer = completion['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"
    
    
@app.route('/gptfinetuning', methods=['POST'])
def gptfinetuning():
    incoming_que = request.values.get('Body', '').lower()
    print(incoming_que)
    
    h = help(incoming_que)
    if legal_sus(incoming_que) == 'SI':
        answer = generate_answer(incoming_que)
        j = justify(answer, incoming_que)
        answer = answer + '\n\n'+j
        
    elif h != 'NO':
        print(h)
        answer = h+'. Para comenzar a consultar, puedes escribir un caso sencillo como este: \n\n"Una compañia farmaceutica desarrolla un nuevo medicamento para el tratamiento del cancer, pero se le rechaza la patente."\n\n o puedes seguir la siguiente estructura: [Introducción al caso] + [Descripción de la acción legal] + [Autoridades o entidades involucradas] + [Procedimiento legal] + [Fundamento legal] + [Resolución o resultado]\n\nCon gusto te indicaré en que fragmento de la ley intelectual de Guatemala se te facilitará la resolución :)'
    else:
        answer = non_legal_response(incoming_que)
    answer = answer
    print(answer)

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)

    return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)