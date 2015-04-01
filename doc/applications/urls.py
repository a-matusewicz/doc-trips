
from django.conf.urls import patterns, url, include

from doc.db.urlhelpers import DB_REGEX
from doc.applications.views.application import (
    NewApplication, ContinueApplication, 
    SetupApplication,
    ApplicationDatabaseListView, 
    ApplicationDatabaseDetailView,
    ApplicationDatabaseUpdateView,
    ApplicationAdminUpdateView,
    LeaderApplicationAdminUpdateView)
from doc.applications.views.grading import(
    RedirectToNextGradableCrooApplication,
    RedirectToNextGradableCrooApplicationForQualification,
    GradeCrooApplication,
    GradeCrooApplicationForQualification,
    NoCrooApplicationsLeftToGrade,
    RedirectToNextGradableLeaderApplication,
    GradeLeaderApplication,
    NoLeaderApplicationsLeftToGrade,
    GraderLandingPage)
from doc.applications.views.graders import GraderListView
from doc.applications.views.portal import VolunteerPortalView
from doc.applications.views.reports import VolunteerCSV

  
grade_urlpatterns = patterns(
    '',
    url(r'^$', GraderLandingPage.as_view(), name='graders'),
    url(r'^croos/$', RedirectToNextGradableCrooApplication.as_view(), name='next_croo'),
    url(r'^croos/(?P<pk>[0-9]+)/$', GradeCrooApplication.as_view(), name='croo'),
    url(r'^croos/for/(?P<qualification_pk>[0-9]+)/$', RedirectToNextGradableCrooApplicationForQualification.as_view(), name='next_croo'),
    url(r'^croos/for/(?P<qualification_pk>[0-9]+)/(?P<pk>[0-9]+)/$', GradeCrooApplicationForQualification.as_view(), name='croo'),
    url(r'^croos/none/$', NoCrooApplicationsLeftToGrade.as_view(), name='no_croo_left'),    
    url(r'^leaders/$', RedirectToNextGradableLeaderApplication.as_view(), name='next_leader'),
    url(r'^leaders/(?P<pk>[0-9]+)$', GradeLeaderApplication.as_view(), name='leader'),
    url(r'^leaders/none/$', NoLeaderApplicationsLeftToGrade.as_view(), name='no_leaders_left'),
)

urlpatterns = patterns(
    '',
    url(r'^$', VolunteerPortalView.as_view(), name='portal'),
    url(r'^apply/$', NewApplication.as_view(), name='apply'),
    url(r'^apply/continue/$', ContinueApplication.as_view(), name='continue'),
    url(r'^setup/$', SetupApplication.as_view(), name='setup'),
    url(r'^grade/', include(grade_urlpatterns, namespace='grade')),
)


# ----- protected database views ----------
# TODO: fix leaderapplication, leadersupplement mismatch

application_urlpatterns = patterns(
    '',
    url(DB_REGEX['LIST'], ApplicationDatabaseListView.as_view(), name='application_index'),
    url(DB_REGEX['DETAIL'], ApplicationDatabaseDetailView.as_view(), name='generalapplication_detail'),
    url(DB_REGEX['UPDATE'], ApplicationDatabaseUpdateView.as_view(), name='generalapplication_update'),
    url(r'^(?P<pk>[0-9]+)/update/status', ApplicationAdminUpdateView.as_view(), name='update_application_status'),
    url(r'^(?P<pk>[0-9]+)/update/trainings', LeaderApplicationAdminUpdateView.as_view(), name='update_application_trainings'),
    url(r'^export/$', VolunteerCSV.as_view(), name='application_csv'),
)

grader_urlpatterns = patterns(
    '',
    url(DB_REGEX['LIST'], GraderListView.as_view(), name='graders_index'),
)
