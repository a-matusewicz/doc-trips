from collections import namedtuple

import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Row, Submit
from django.db.models import Q
from django.forms import Select

from fyt.applications.models import Volunteer
from fyt.training.models import Attendee
from fyt.trips.models import Section, TripType
from fyt.utils.choices import AVAILABLE, PREFER
from fyt.utils.query import pks


class AvailableSectionFilter(django_filters.ModelChoiceFilter):
    """Filter leaders based on the trips sections they are available for."""
    def __init__(self, trips_year):
        qs = Section.objects.filter(trips_year=trips_year)
        super().__init__(queryset=qs)

    def filter(self, qs, value):
        if not value:
            return qs

        return qs.filter(
            Q(leader_supplement__leadersectionchoice__preference=PREFER) |
            Q(leader_supplement__leadersectionchoice__preference=AVAILABLE),
            leader_supplement__leadersectionchoice__section=value)


class AvailableTripTypeFilter(django_filters.ModelChoiceFilter):
    """Filter leaders based on the trip types they are available for."""
    def __init__(self, trips_year):
        qs = TripType.objects.filter(trips_year=trips_year)
        super().__init__(queryset=qs)

    def filter(self, qs, value):
        if not value:
            return qs

        return qs.filter(
            Q(leader_supplement__leadertriptypechoice__preference=PREFER) |
            Q(leader_supplement__leadertriptypechoice__preference=AVAILABLE),
            leader_supplement__leadertriptypechoice__triptype=value)


_Choice = namedtuple('_Choice', ['value', 'display', 'action'])


class ApplicationTypeFilter(django_filters.ChoiceFilter):
    """Filter for different types of applications."""
    def __init__(self, trips_year):
        self.trips_year = trips_year
        self.actions = {c.value: c.action for c in self.choices}
        filter_choices = [(c.value, c.display) for c in self.choices]
        super().__init__(self, choices=filter_choices)

    # (query value, display name, action/method)
    choices = [
        _Choice('any', 'All Applications', None),
        _Choice('leader', 'Leader Applications', 'leader_applications'),
        _Choice('croo', 'Croo Applications', 'croo_applications'),
        _Choice('either', 'Leader OR Croo Applications', 'either_applications'),
        _Choice('both', 'Leader AND Croo Applications', 'both_applications'),
        _Choice('incomplete_leader', 'Incomplete Leader Applications',
                'incomplete_leader_applications'),
        _Choice('incomplete_croo', 'Incomplete Croo Applications',
                'incomplete_croo_applications'),
    ]

    def croo_applications(self, qs):
        return qs & Volunteer.objects.croo_applications(
            self.trips_year)

    def leader_applications(self, qs):
        return qs & Volunteer.objects.leader_applications(
            self.trips_year)

    def either_applications(self, qs):
        return qs & Volunteer.objects.leader_or_croo_applications(
            self.trips_year)

    def both_applications(self, qs):
        return qs & Volunteer.objects.leader_and_croo_applications(
            self.trips_year)

    def incomplete_leader_applications(self, qs):
        return qs & Volunteer.objects.incomplete_leader_applications(
            self.trips_year)

    def incomplete_croo_applications(self, qs):
        return qs & Volunteer.objects.incomplete_croo_applications(
            self.trips_year)

    def filter(self, qs, value):
        if not value or not self.actions[value]:
            return qs

        action = getattr(self, self.actions[value])
        if not action:
            return qs

        return action(qs)


class FirstAidFilter(django_filters.ChoiceFilter):
    def __init__(self, trips_year, *args, **kwargs):
        self.trips_year = trips_year
        kwargs.update({
            'choices': (
                ('', BLANK),
                ('missing', 'Missing'),
                ('complete', 'Complete')),
            'label': 'First Aid Training'
        })
        super().__init__(self, *args, **kwargs)

    def filter(self, qs, value):
        if value == 'missing':
            return qs.filter(attendee__pk__in=pks(
                Attendee.objects.first_aid_incomplete(self.trips_year)))
        elif value == 'complete':
            return qs.filter(attendee__pk__in=pks(
                Attendee.objects.first_aid_complete(self.trips_year)))
        else:
            return qs


class TrainingFilter(django_filters.ChoiceFilter):
    def __init__(self, trips_year, *args, **kwargs):
        self.trips_year = trips_year
        kwargs.update({
            'choices': (
                ('', BLANK),
                ('incomplete', 'Incomplete'),
                ('complete', 'Complete')),
            'label': 'Training'
        })
        super().__init__(self, *args, **kwargs)

    def filter(self, qs, value):
        if value == 'incomplete':
            return qs.filter(attendee__pk__in=pks(
                Attendee.objects.training_incomplete(self.trips_year)))
        elif value == 'complete':
            return qs.filter(attendee__pk__in=pks(
                Attendee.objects.training_complete(self.trips_year)))
        else:
            return qs


STATUS = 'status'
CLASS_YEAR = 'class_year'
COMPLETE = 'complete'
FIRST_AID = 'first_aid'
TRAINING = 'training'
AVAILABLE_SECTIONS = 'available_sections'
AVAILABLE_TRIPTYPES = 'available_triptypes'
CLASS_2_3 = 'leader_supplement__class_2_3_paddler'
LEDYARD_LEVEL_1 = 'leader_supplement__ledyard_level_1'
LEDYARD_LEVEL_2 = 'leader_supplement__ledyard_level_2'
CLIMBING_COURSE = 'leader_supplement__climbing_course'
DMC_LEADER = 'leader_supplement__dmc_leader'
DMBC_LEADER = 'leader_supplement__dmbc_leader'
CNT_LEADER = 'leader_supplement__cnt_leader'
SAFETY_LEAD = 'croo_supplement__safety_lead_willing'
KITCHEN_LEAD = 'croo_supplement__kitchen_lead_willing'

SHORT_LABELS = {
    STATUS: 'Status',
    CLASS_YEAR: 'Class Year',
    CLASS_2_3: 'Class II/III Paddler',
    LEDYARD_LEVEL_1: 'Ledyard Level 1',
    LEDYARD_LEVEL_2: 'Ledyard Level 2',
    CLIMBING_COURSE: 'DOC Climbing Course',
    DMC_LEADER: 'DMC Leader',
    DMBC_LEADER: 'DMBC Leader',
    CNT_LEADER: 'CNT Leader',
    SAFETY_LEAD: 'Safety Lead Willing',
    KITCHEN_LEAD: 'Kitchen Magician Willing',
    AVAILABLE_SECTIONS: 'Available Sections',
    AVAILABLE_TRIPTYPES: 'Available Trip Types',
}

BLANK = '--------'

class ApplicationFilterSet(django_filters.FilterSet):

    class Meta:
        model = Volunteer
        fields = [
            STATUS,
            CLASS_YEAR,
            CLASS_2_3,
            LEDYARD_LEVEL_1,
            LEDYARD_LEVEL_2,
            CLIMBING_COURSE,
            DMC_LEADER,
            DMBC_LEADER,
            CNT_LEADER,
            SAFETY_LEAD,
            KITCHEN_LEAD
        ]

    name = django_filters.MethodFilter(action='lookup_user_by_name')
    netid = django_filters.MethodFilter(action='lookup_user_by_netid')

    def lookup_user_by_name(self, qs, value):
        if not value:
            return qs

        return qs.filter(applicant__name__icontains=value)

    def lookup_user_by_netid(self, qs, value):
        if not value:
            return qs

        return qs.filter(applicant__netid__iexact=value)

    def __init__(self, trips_year, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters[COMPLETE] = ApplicationTypeFilter(trips_year)
        self.filters[AVAILABLE_SECTIONS] = AvailableSectionFilter(trips_year)
        self.filters[AVAILABLE_TRIPTYPES] = AvailableTripTypeFilter(trips_year)
        self.filters[FIRST_AID] = FirstAidFilter(trips_year)
        self.filters[TRAINING] = TrainingFilter(trips_year)

        # Add blank choices
        default_blank = [
            STATUS,
            CLASS_2_3,
            LEDYARD_LEVEL_1,
            LEDYARD_LEVEL_2,
            CLIMBING_COURSE,
            DMC_LEADER,
            DMBC_LEADER,
            CNT_LEADER,
        ]
        for field in default_blank:
            self.filters[field].field.choices.insert(0, (None, BLANK))
            self.filters[field].field.default = None

        # Provide a better default to NullBooleanFields
        for field in [SAFETY_LEAD, KITCHEN_LEAD]:
            self.filters[field].field.widget = Select(
                choices=[(None, BLANK),
                         (True, 'Yes'),
                         (False, 'No')])

        # Use abbreviated labels
        for field, label in SHORT_LABELS.items():
            self.filters[field].field.label = label

        self.form.helper = FilterSetFormHelper(self.form)


class FilterSetFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def filter_row(filter):
            return Row(Div(filter, css_class='col-lg-12'))

        self.form_method = 'GET'
        self.layout = Layout(
            filter_row(COMPLETE),
            filter_row(STATUS),
            filter_row(FIRST_AID),
            filter_row(TRAINING),
            filter_row(CLASS_YEAR),
            filter_row('name'),
            filter_row('netid'),
            filter_row(AVAILABLE_SECTIONS),
            filter_row(AVAILABLE_TRIPTYPES),
            filter_row(CLASS_2_3),
            filter_row(LEDYARD_LEVEL_1),
            filter_row(LEDYARD_LEVEL_2),
            filter_row(CLIMBING_COURSE),
            filter_row(DMC_LEADER),
            filter_row(DMBC_LEADER),
            filter_row(CNT_LEADER),
            filter_row(SAFETY_LEAD),
            filter_row(KITCHEN_LEAD),
            filter_row(Submit('submit', 'Filter', css_class='btn-block'))
        )
