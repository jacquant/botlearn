from django.contrib import admin

from exercises.admin.error.interface import ErrorAdmin
from exercises.admin.errors_template.interface import ErrorsTemplateAdmin
from exercises.admin.exercise.interface import ExerciseAdmin
from exercises.admin.submission.interface import SubmissionAdmin
from exercises.models.category import Category
from exercises.models.difficulty import Difficulty
from exercises.models.error import Error
from exercises.models.error_count import ErrorCount
from exercises.models.errors_template import ErrorsTemplate
from exercises.models.exercise import Exercise
from exercises.models.requirement import Requirement
from exercises.models.section import Section
from exercises.models.session import Session
from exercises.models.submission import Submission
from exercises.models.tag import Tag
from exercises.models.target_students import TargetStudents

admin.site.register(Category)
admin.site.register(Difficulty)
admin.site.register(Error, ErrorAdmin)
admin.site.register(ErrorCount)
admin.site.register(ErrorsTemplate, ErrorsTemplateAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Requirement)
admin.site.register(Section)
admin.site.register(Session)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Tag)
admin.site.register(TargetStudents)
