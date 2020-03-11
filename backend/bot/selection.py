import logging

# A developper Own selection logic
def select_response(statement, response_list, storage=None):

    logger = logging.getLogger(__name__)
    logger.info('Selecting first response from list of {} options.'.format(
        len(response_list)
    ))
    confidence = 0
    return_statement = response_list[0]
    return_statement.text = "<p>Désolé mais je n'ai pas compris la question :( Pourrais-tu la reformuler s'il te plait.</p><p> <div style='color:red;'>Attention !</div> Il faut savoir que je réponds aux questions liées à la programmation en générale, pas sur l'exercice.</p>"
    return return_statement

