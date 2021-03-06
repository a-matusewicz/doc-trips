from model_mommy import mommy

from fyt.applications.models import Volunteer
from fyt.croos.models import Croo
from fyt.test import FytTestCase


class CrooModelTestCase(FytTestCase):
    def test_safety_leads(self):
        trips_year = self.init_trips_year()
        croo = mommy.make(Croo, trips_year=trips_year)
        CROO = Volunteer.CROO
        safety_lead = mommy.make(
            Volunteer,
            trips_year=trips_year,
            safety_lead=True,
            status=CROO,
            croo_assignment=croo,
        )
        other_member = mommy.make(
            Volunteer,
            trips_year=trips_year,
            safety_lead=False,
            status=CROO,
            croo_assignment=croo,
        )
        self.assertEqual([safety_lead], list(croo.safety_leads()))

    def test_non_safety_leads(self):
        trips_year = self.init_trips_year()
        croo = mommy.make(Croo, trips_year=trips_year)
        CROO = Volunteer.CROO
        safety_lead = mommy.make(
            Volunteer,
            trips_year=trips_year,
            safety_lead=True,
            status=CROO,
            croo_assignment=croo,
        )
        other_member = mommy.make(
            Volunteer,
            trips_year=trips_year,
            safety_lead=False,
            status=CROO,
            croo_assignment=croo,
        )
        self.assertEqual([other_member], list(croo.non_safety_leads()))
