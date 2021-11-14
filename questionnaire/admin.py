from django.contrib import admin
from .models import Quiz, Answer, Question, Result

admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Result)
