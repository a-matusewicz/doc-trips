from vanilla import UpdateView
from django import forms

from doc.permissions.views import ApplicationEditPermissionRequired
from doc.db.views import TripsYearMixin
from doc.applications.models import GeneralApplication
from doc.applications.forms import TripAssignmentForm


class AssignToTrip(ApplicationEditPermissionRequired, TripsYearMixin,
                   UpdateView):
    """
    Assign LEADER to a ScheduledTrip.

    Shows availability, preferences
    """

    model = GeneralApplication
    template_name = 'applications/trip_assignment_update.html'
    form_class = TripAssignmentForm

    def get_context_data(self, **kwargs):
        kwargs['preferred_trips'] = self.object.get_preferred_trips()
        kwargs['available_trips'] = self.object.get_available_trips()
        return super(AssignToTrip, self).get_context_data(**kwargs)