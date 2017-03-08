
from model_mommy import mommy

from django.core.urlresolvers import reverse

from . import ApplicationTestMixin
from ..models import Volunteer, Score, Skip
from fyt.test import FytTestCase


class VolunteerManagerTestCase(ApplicationTestMixin, FytTestCase):

    def setUp(self):
        self.init_trips_year()
        self.user = self.mock_user()

    def test_only_score_apps_for_this_year(self):
        last_year = self.init_previous_trips_year()

        app1 = self.make_application(trips_year=self.trips_year)
        app2 = self.make_application(trips_year=last_year)

        self.assertEqual(app1, Volunteer.objects.next_to_score(self.user))

    def test_only_score_complete_apps(self):
        self.make_application(leader_willing=False, croo_willing=False)
        self.assertIsNone(Volunteer.objects.next_to_score(self.user))

    def test_user_only_scores_application_once(self):
        app = self.make_application()
        app.add_score(self.user, 4)
        self.assertIsNone(Volunteer.objects.next_to_score(self.user))

    def test_only_score_pending_applications(self):
        app = self.make_application()  # PENDING
        for status, _ in Volunteer.STATUS_CHOICES:
            if status != Volunteer.PENDING:
                self.make_application(status=status)

        self.assertEqual(app, Volunteer.objects.next_to_score(self.user))

    def test_only_score_3_times(self):
        app = self.make_application()
        for i in range(Volunteer.NUM_SCORES):
            mommy.make(Score, trips_year=self.trips_year, application=app)

        self.assertIsNone(Volunteer.objects.next_to_score(self.user))


class ScoreViewsTestCase(ApplicationTestMixin, FytTestCase):

    def setUp(self):
        self.init_trips_year()
        self.mock_director()
        self.mock_user()

    score_urls = [
        reverse('applications:score:next'),
        reverse('applications:score:no_applications_left'),
    ]

    not_available = 'applications/scoring_not_available.html'

    def test_cant_score_before_application_deadline(self):
        self.open_application()
        for url in self.score_urls:
            resp = self.app.get(url, user=self.director).maybe_follow()
            self.assertTemplateUsed(resp, self.not_available)

    def test_can_score_after_application_deadline(self):
        self.close_application()
        for url in self.score_urls:
            resp = self.app.get(url, user=self.director).maybe_follow()
            self.assertTemplateNotUsed(resp, self.not_available)

    def test_scoring_permissions(self):
        self.open_application()
        for url in self.score_urls + [reverse('applications:score:scoring')]:
            self.app.get(url, user=self.director)
            self.app.get(url, user=self.user, status=403)
