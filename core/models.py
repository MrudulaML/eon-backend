"""
Creating all models related to core here
"""
from django.db import models

# Create your models here.
from authentication.models import ModelBase, User, Role, ActiveModel


class EventType(ActiveModel):
    """Event type model add here """
    type = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.type


class Event(ActiveModel):
    """
    Event model added here
    """
    name = models.CharField(max_length=32)
    type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=512)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=512)
    images = models.CharField(max_length=512, default='events/default.jpeg')
    subscription_fee = models.PositiveIntegerField()
    no_of_tickets = models.PositiveIntegerField()
    sold_tickets = models.PositiveIntegerField(default=0)
    is_cancelled = models.BooleanField(default=False)
    external_links = models.CharField(max_length=1024, null=True, blank=True)
    event_created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        """
        To override the database table name, use the db_table parameter in class Meta.
        """
        unique_together = ("name", "type", "date", "time")

    def __str__(self):
        return "{}".format(self.name)


class Invitation(ActiveModel):
    """
    Invitation model created here
    """
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    discount_percentage = models.PositiveIntegerField()
    email = models.EmailField()

    def __str__(self):
        return "{}-{}-{}".format(self.event, self.user, self.discount_percentage)


class WishList(ActiveModel):
    """
    Added wish list model here
    """
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        """
        To override the database table name, use the db_table parameter in class Meta.
        """
        unique_together = ("event", "user")

    def __str__(self):
        return "{}-{}-{}".format(self.user, self.event, self.is_active)


class Subscription(ActiveModel):
    """
    Added subscription model here
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    no_of_tickets = models.FloatField()
    id_payment = models.PositiveIntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Save method for subscription model
        """
        self.event.sold_tickets += self.no_of_tickets
        self.event.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}-{}-{}".format(self.user, self.event, self.no_of_tickets)


class UserInterest(ActiveModel):
    """
    User interest model created here
    """
    event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.user, self.event_type)


class UserProfile(ModelBase):
    """
    Created user profile model here
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    organization = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return "{}-{}-{}".format(self.user, self.name, self.contact_number)


class Notification(ModelBase):
    """
    Notification Model created here
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=512)
    has_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}-{}-{}".format(self.user, self.event, self.message)


class Question(ActiveModel):
    """
    Question model created here
    """
    question = models.CharField(max_length=1024)

    def __str__(self):
        return "{}".format(self.question)


class UserFeedback(ActiveModel):
    """
        User Feedback model created here
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

    class Meta:
        """
        To override the database table name, use the db_table parameter in class Meta.
        """
        unique_together = ("user", "event")

    def __str__(self):
        return "{}-{}".format(self.user, self.event)


class Feedback(ActiveModel):
    """
        Feedback model created here
    """
    user_feedback = models.ForeignKey(UserFeedback, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    answer = models.CharField(max_length=1024, default="")
    image = models.CharField(max_length=1024, default="")

    class Meta:
        """
        To override the database table name, use the db_table parameter in class Meta.
        """
        unique_together = ("user_feedback", "question")

    def __str__(self):
        return "{}-{}".format(self.user_feedback, self.question)
