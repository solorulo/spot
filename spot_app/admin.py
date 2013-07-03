from spot_app.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = Info_Usuario
    can_delete = False
    verbose_name_plural = 'Perfil'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Crew)
admin.site.register(Comparte)
admin.site.register(Foto)
admin.site.register(Comentario)
admin.site.register(Ruta)
admin.site.register(Orden)
