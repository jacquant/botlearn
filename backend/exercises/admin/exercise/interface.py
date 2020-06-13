from django.contrib import admin


class ExerciseAdmin(admin.ModelAdmin):
    readonly_fields = ("docker_image",)
