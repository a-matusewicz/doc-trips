import io
import csv
import tempfile

from django.core.urlresolvers import reverse
from model_mommy import mommy

from doc.test.fixtures import WebTestCase
from doc.applications.tests import ApplicationTestMixin
from doc.applications.models import GeneralApplication


class ReportViewsTestCase(WebTestCase, ApplicationTestMixin):

    def test_volunteer_csv(self):
        trips_year = self.init_current_trips_year()
        application = self.make_application(trips_year=trips_year)
        non_applicant = self.make_application(trips_year=trips_year)
        non_applicant.croo_supplement.document = ''
        non_applicant.croo_supplement.save()
        non_applicant.leader_supplement.document = ''
        non_applicant.leader_supplement.save()
        res = self.app.get(reverse('db:reports:application_csv',
                                   kwargs={'trips_year': trips_year}),
                           user=self.mock_director())
        self.assertTrue(res['Content-Disposition'].startswith('attachment; filename="'))
        # convolutedly save file content
        f = tempfile.NamedTemporaryFile()
        f.write(res.content)
        f = open(f.name) # open in non-binary mode
        reader = csv.reader(f)
        row = next(reader)
        self.assertEqual(row[0], application.applicant.name)
        self.assertEqual(row[1], application.applicant.netid)
        with self.assertRaises(StopIteration):
            next(reader)
        
