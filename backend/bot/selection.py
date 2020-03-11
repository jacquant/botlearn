import logging

try:
    from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
except ImportError:
    from difflib import SequenceMatcher


# A developper Own selection logic
def select_response(statement, response_list, storage=None):

    logger = logging.getLogger(__name__)
    logger.info('Selecting first response from list of {} options.'.format(
        len(response_list)
    ))
    print("CHECKING")
    print(response_list[0].confidence)
    print(dir(statement))
    return response_list[len(response_list)-1]

class Comparator:

    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    def compare(self, statement_a, statement_b):
        return 0

class OwnCompare(Comparator):

  def compare(self, statement, other_statement):
        """
        Compare the two input statements.

        :return: The percent of similarity between the text of the statements.
        :rtype: float
        """
        #print("---COMPARAISON---")
        if ("supprimer" in other_statement.text):
            print("---COMPARAISON---")
            print(statement)
            print(other_statement)
            print("-----------")
        print("---COMPARAISON---")
        print(other_statement)
        print("-----------")
        # Return 0 if either statement has a falsy text value
        if not statement.text or not other_statement.text:
            return 0

        # Get the lowercase version of both strings
        statement_text = str(statement.text.lower())
        other_statement_text = str(other_statement.text.lower())

        similarity = SequenceMatcher(
            None,
            statement_text,
            other_statement_text
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent

owncompare = OwnCompare()