import re

from bot.models import Answer


def train_bot(trainer):
    for answer in Answer.objects.all():
        # Modify the code snippet to HMTL to diplay it correctly in the
        # chatbot
        modify_code = re.sub(
            r" {4}", "&nbsp;&nbsp;&nbsp;&nbsp;", answer.answer
        )
        modify_code = re.sub(r"(\r\n){1}(?!\r\n)", "<br>", modify_code)
        for question in answer.question_set.all():
            trainer.train([question.title, modify_code])
