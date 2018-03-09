from autoslug import AutoSlugField
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class Setup(models.Model):
    name = models.CharField(max_length=200)
    engine = models.ForeignKey('car.Engine')
    power = models.IntegerField(default=None, blank=True, null=True)
    torque = models.IntegerField(default=None, blank=True, null=True)
    rev_limit = models.IntegerField(default=None, blank=True, null=True)
    weight = models.IntegerField(default=None, blank=True, null=True)
    weight_distribution = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=None, blank=True, null=True)
    boost = models.FloatField(default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    creator = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    car = GenericForeignKey('content_type', 'object_id')
    car_year = models.IntegerField(default=None, null=True, blank=True, verbose_name=_('Car Year'))
    views = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def get_main_image(self):
        try:
            return SetupImage.objects.filter(setup=self)[0]
        except IndexError:
            return None

    def get_additional_images(self):
        try:
            return SetupImage.objects.filter(setup=self)[1:]
        except IndexError:
            pass

    def get_all_images(self):
        return SetupImage.objects.filter(setup=self)

    def get_engine_fields(self):
        return SetupField.objects.filter(setup=self, category=0)

    def get_drivetrain_fields(self):
        return SetupField.objects.filter(setup=self, category=1)

    def get_suspension_fields(self):
        return SetupField.objects.filter(setup=self, category=2)

    def get_brakes_fields(self):
        return SetupField.objects.filter(setup=self, category=3)

    def get_wheels_fields(self):
        return SetupField.objects.filter(setup=self, category=4)

    def get_exterior_fields(self):
        return SetupField.objects.filter(setup=self, category=5)

    def get_interior_fields(self):
        return SetupField.objects.filter(setup=self, category=6)

    def get_votes_total(self):
        return SetupVote.objects.filter(setup=self).count()

    def get_up_votes_total(self):
        return SetupVote.objects.filter(setup=self, vote=1).count()

    def get_votes_percentage(self):
        votes_total = self.get_votes_total()
        votes_up = self.get_up_votes_total()
        if votes_total != 0 and votes_up != 0:
            percentage = votes_up / votes_total * 100
            return int(percentage)
        else:
            return 0

    def get_full_name(self):
        return self.car.name()

    def increase_views(self):
        self.views += 1
        self.save()

    def get_absolute_url(self):
        return reverse('setup_detail', args=[self.slug])

    def __str__(self):
        return self.name


class SetupImage(models.Model):
    image = models.ImageField(upload_to='setups/', blank=True, default=None, null=True)
    order = models.IntegerField(default=0)
    setup = models.ForeignKey(Setup)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.image.url


class SetupField(models.Model):
    CATEGORIES = (
        (0, _('Engine')),
        (1, _('Drivetrain')),
        (2, _('Steering/Suspension')),
        (3, _('Brakes')),
        (4, _('Wheels')),
        (5, _('Exterior')),
        (6, _('Interior')),

    )
    field = models.CharField(max_length=300)
    setup = models.ForeignKey(Setup)
    category = models.SmallIntegerField(choices=CATEGORIES)

    def __str__(self):
        return self.field


class SetupVote(models.Model):
    VOTES = (
        (0, _('Vote Down')),
        (1, _('Vote Up')),
    )
    vote = models.BooleanField(default=0, choices=VOTES)
    setup = models.ForeignKey(Setup)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.vote
