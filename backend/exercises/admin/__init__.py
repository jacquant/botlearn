from django.contrib import admin

from exercises.models.category import Category
from exercises.models.difficulty import Difficulty
from exercises.models.exercise import Exercise
from exercises.models.section import Section
from exercises.models.session import Session
from exercises.models.submission import Submission
from exercises.models.tag import Tag
from exercises.models.target_students import TargetStudents

admin.site.register(Category)
admin.site.register(Difficulty)
admin.site.register(Exercise)
admin.site.register(Section)
admin.site.register(Session)
admin.site.register(Submission)
admin.site.register(Tag)
admin.site.register(TargetStudents)
