from django.contrib import admin

from apps.authentication.models import APIUser, TokenBlacklist

# Register your models here.

admin.site.register(APIUser)


@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    list_display = ("jti", "user_id", "token_type", "revoked_at", "expires_at")
    list_filter = ("token_type", "revoked_at", "expires_at")
    search_fields = ("jti", "user_id", "token")
    readonly_fields = ("jti", "token", "user_id", "token_type", "revoked_at", "expires_at")
    ordering = ("-revoked_at",)
