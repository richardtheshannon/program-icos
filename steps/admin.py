from django.contrib import admin

from steps.models import Question, Response, Step, StepProgress


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("number", "text", "question_type", "is_required")
    ordering = ("number",)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "spiritual_principle", "is_recurring")
    list_filter = ("is_recurring",)
    ordering = ("number",)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "question_type", "is_required")
    list_filter = ("step", "question_type")
    ordering = ("step__number", "number")


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "updated_at")
    list_filter = ("question__step",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(StepProgress)
class StepProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "step", "status", "updated_at")
    list_filter = ("status", "step")
    readonly_fields = ("created_at", "updated_at")
