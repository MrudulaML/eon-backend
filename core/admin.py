from daterangefilter.filters import PastDateRangeFilter
from django.contrib import admin

# Register your models here.
from core import filters
from core.models import EventType, Event, Invitation, Subscription, UserProfile, WishList, \
    UserInterest

"""
Register all the core related model here
"""


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """
    added event type model in admin
    """
    list_display = ("id", "type")
    search_fields = ("type",)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Added event model in admin
    """
    list_display = (
        "id", "name", "type", "date", "time", "location", "subscription_fee", "no_of_tickets", "sold_tickets",
        "is_cancelled", "event_created_by")
    search_fields = ("name", "type__type", "event_created_by__email", "event_created_by__userprofile__name")
    list_filter = (
        "type", "is_cancelled", "event_created_by", ("date", PastDateRangeFilter), filters.PaidFreeEventFilter)
    readonly_fields = (
        "name", "type", "description", "date", "time", "location", "images", "subscription_fee",
        "no_of_tickets", "external_links", "event_created_by", "sold_tickets", "is_cancelled")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """
    Added invitation in admin
    """
    list_display = ("id", "event", "discount_percentage", "email")
    list_filter = ('event', )
    search_fields = ('email', )
    readonly_fields = ('event', 'user', 'discount_percentage', 'email')
    fieldsets = (
        (
            "", {
                "fields": ("event", "discount_percentage", "email")}
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    """
    Added event preference in admin
    """
    list_display = ("id", "event_type", "user")
    list_filter = ('event_type',)
    search_fields = ('user__email',)
    readonly_fields = ('user', 'event_type', 'is_active')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Added subscription model in admin
    """
    list_display = ("id", "event", "user", "no_of_tickets", "amount", 'is_active')
    search_fields = ("event__name", "user__email")
    readonly_fields = ('is_active', 'user', 'event', 'no_of_tickets', 'amount')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Added user profile model in admin
    """
    list_display = ("id", "user", "name", "contact_number", "organization", "role")
    search_fields = ("user__email", "user__userprofile__name", "contact_number", "organization",)
    list_filter = ("role",)
    readonly_fields = ('user', 'name', 'contact_number', 'organization', 'address', 'role')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    """
    Added user profile model in admin
    """
    list_display = ("id", "user", "event")
    search_fields = ("user__email",)
    list_filter = ("event",)
    readonly_fields = ('user', 'event')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
