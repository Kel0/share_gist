from django.contrib import admin

from .models import Lexer, Paste

admin.site.register(Paste)
admin.site.register(Lexer)
