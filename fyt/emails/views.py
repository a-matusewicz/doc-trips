from collections import OrderedDict

from braces.views import SetHeadlineMixin
from django.core.exceptions import ImproperlyConfigured
from vanilla import TemplateView

from fyt.applications.models import Volunteer
from fyt.core.views import TripsYearMixin
from fyt.incoming.models import IncomingStudent, Registration
from fyt.permissions.views import DatabaseReadPermissionRequired
from fyt.trips.models import Section, TripType


class BaseEmailList(
    DatabaseReadPermissionRequired, TripsYearMixin, SetHeadlineMixin, TemplateView
):
    """
    Base class for email list view
    """

    template_name = 'emails/emails.html'

    def get_email_lists(self):
        """
        Should return an iterable of duples in the form
        (email_list_name, list_of_emails)
        """
        raise ImproperlyConfigured()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_lists'] = OrderedDict(self.get_email_lists())
        return context


def emails(qs):
    """
    Return a list of applicant emails from GenApp qs
    """
    return qs.values_list('applicant__email', flat=True)


def personal_emails(qs):
    """
    List of trippee emails from IncomingStudent qs
    """
    return qs.values_list('email', flat=True)


def blitz(qs):
    """
    List of trippee blitzes from IncomingStudent qs
    """
    return qs.values_list('blitz', flat=True)


class Applicants(BaseEmailList):

    headline = "Applicant Emails"

    def get_email_lists(self):
        return [
            (
                'all applicants',
                emails(Volunteer.objects.filter(trips_year=self.trips_year)),
            ),
            (
                'complete leader applications',
                emails(Volunteer.objects.leader_applications(self.trips_year)),
            ),
            (
                'complete croo applications',
                emails(Volunteer.objects.croo_applications(self.trips_year)),
            ),
            (
                'incomplete leader applications',
                emails(
                    Volunteer.objects.incomplete_leader_applications(self.trips_year)
                ),
            ),
            (
                'incomplete croo applications',
                emails(Volunteer.objects.incomplete_croo_applications(self.trips_year)),
            ),
            ('leaders', emails(Volunteer.objects.leaders(self.trips_year))),
            (
                'leader waitlist',
                emails(Volunteer.objects.leader_waitlist(self.trips_year)),
            ),
            ('croo members', emails(Volunteer.objects.croo_members(self.trips_year))),
            (
                'rejected applicants',
                emails(Volunteer.objects.rejected(self.trips_year)),
            ),
        ]


class LeadersByTripType(BaseEmailList):

    headline = "Leader Emails by TripType"

    def get_email_lists(self):
        leaders = Volunteer.objects.leaders(self.trips_year)
        triptypes = TripType.objects.filter(trips_year=self.trips_year)

        email_list = []
        for triptype in triptypes:
            email_list.append(
                (
                    '%s leaders' % triptype,
                    emails(
                        leaders.filter(trip_assignment__template__triptype=triptype)
                    ),
                )
            )
        return email_list


class LeadersBySection(BaseEmailList):

    headline = "Leader Emails by Section"

    def get_email_lists(self):
        leaders = Volunteer.objects.leaders(self.trips_year)
        sections = Section.objects.filter(trips_year=self.trips_year)

        email_list = []
        for section in sections:
            email_list.append(
                (
                    '%s leaders' % section,
                    emails(leaders.filter(trip_assignment__section=section)),
                )
            )
        return email_list


class IncomingStudents(BaseEmailList):

    headline = "Incoming Student Emails"

    def get_email_lists(self):
        unregistered = IncomingStudent.objects.unregistered(self.trips_year)
        registered = Registration.objects.filter(trips_year=self.trips_year)

        email_list = [
            ('unregistered personal emails', personal_emails(unregistered)),
            ('unregistered blitz', blitz(unregistered)),
            ('registrations', personal_emails(registered)),
        ]

        return email_list


class Trippees(BaseEmailList):

    headline = "Trippees"

    def get_email_lists(self):
        sections = Section.objects.filter(trips_year=self.trips_year)
        trippees = IncomingStudent.objects.with_trip(self.trips_year)

        email_list = [
            (
                "All Trippees (Incoming Students with a trip assignment)",
                personal_emails(trippees),
            ),
            ("All Trippees - blitz", blitz(trippees)),
        ]

        for sxn in sections:
            trpz = trippees.filter(trip_assignment__section=sxn)
            email_list.append(("Section %s trippees" % sxn.name, personal_emails(trpz)))
            email_list.append(("Section %s trippees - blitz" % sxn.name, blitz(trpz)))
        return email_list


class TrippeesByTripType(BaseEmailList):

    headline = "Trippee Emails by Trip Type"

    def get_email_lists(self):
        trippees = IncomingStudent.objects.with_trip(self.trips_year)
        triptypes = TripType.objects.filter(trips_year=self.trips_year)

        email_list = []
        for triptype in triptypes:
            email_list.append(
                (
                    '%s trippees' % triptype,
                    blitz(
                        trippees.filter(trip_assignment__template__triptype=triptype)
                    ),
                )
            )
        return email_list
