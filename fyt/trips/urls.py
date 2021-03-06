from django.conf.urls import url

from .views import *

from fyt.core.urlhelpers import DB_REGEX


"""
OOdles of urls. These patterns all included in the main
database urlpatterns.
"""

trip_urlpatterns = [
    url(DB_REGEX['LIST'], TripList.as_view(), name='index'),
    url(DB_REGEX['CREATE'], TripCreate.as_view(), name='create'),
    url(DB_REGEX['DETAIL'], TripDetail.as_view(), name='detail'),
    url(DB_REGEX['UPDATE'], TripUpdate.as_view(), name='update'),
    url(DB_REGEX['DELETE'], TripDelete.as_view(), name='delete'),
    url(r'^counts/', TrippeeLeaderCounts.as_view(), name='people_counts'),
]

template_urlpatterns = [
    url(DB_REGEX['LIST'], TripTemplateList.as_view(), name='index'),
    url(DB_REGEX['CREATE'], TripTemplateCreate.as_view(), name='create'),
    url(DB_REGEX['DETAIL'], TripTemplateDetail.as_view(), name='detail'),
    url(DB_REGEX['UPDATE'], TripTemplateUpdate.as_view(), name='update'),
    url(DB_REGEX['DELETE'], TripTemplateDelete.as_view(), name='delete'),
    url(
        r'^(?P<triptemplate_pk>[0-9]+)/upload/file$',
        UploadTripTemplateDocument.as_view(),
        name='upload_file',
    ),
    url(
        r'^(?P<triptemplate_pk>[0-9]+)/documents/delete/(?P<pk>[0-9]+)/$',
        TripTemplateDocumentDelete.as_view(),
        name='document_delete',
    ),
    url(
        r'^(?P<pk>[0-9]+)/documents/list',
        TripTemplateDocumentList.as_view(),
        name='document_list',
    ),
]

triptype_urlpatterns = [
    url(DB_REGEX['LIST'], TripTypeList.as_view(), name='index'),
    url(DB_REGEX['CREATE'], TripTypeCreate.as_view(), name='create'),
    url(DB_REGEX['DETAIL'], TripTypeDetail.as_view(), name='detail'),
    url(DB_REGEX['UPDATE'], TripTypeUpdate.as_view(), name='update'),
    url(DB_REGEX['DELETE'], TripTypeDelete.as_view(), name='delete'),
]

campsite_urlpatterns = [
    url(DB_REGEX['LIST'], CampsiteMatrix.as_view(), name='index'),
    url(DB_REGEX['CREATE'], CampsiteCreate.as_view(), name='create'),
    url(DB_REGEX['DETAIL'], CampsiteDetail.as_view(), name='detail'),
    url(DB_REGEX['UPDATE'], CampsiteUpdate.as_view(), name='update'),
    url(DB_REGEX['DELETE'], CampsiteDelete.as_view(), name='delete'),
]

section_urlpatterns = [
    url(DB_REGEX['LIST'], SectionList.as_view(), name='index'),
    url(DB_REGEX['CREATE'], SectionCreate.as_view(), name='create'),
    url(DB_REGEX['DETAIL'], SectionDetail.as_view(), name='detail'),
    url(DB_REGEX['UPDATE'], SectionUpdate.as_view(), name='update'),
    url(DB_REGEX['DELETE'], SectionDelete.as_view(), name='delete'),
]

leader_urlpatterns = [
    url(r'^$', LeaderTrippeeIndexView.as_view(), name='leader_index'),
    url(
        r'^assign/trippee/(?P<trip_pk>[0-9]+)$',
        AssignTrippee.as_view(),
        name='assign_trippee',
    ),
    url(
        r'^assign/trippee/(?P<trippee_pk>[0-9]+)/update/$',
        AssignTrippeeToTrip.as_view(),
        name='assign_trippee_to_trip',
    ),
    url(
        r'^assign/leader/(?P<trip_pk>[0-9]+)$',
        AssignLeader.as_view(),
        name='assign_leader',
    ),
    url(
        r'^assign/leader/(?P<leader_pk>[0-9]+)/update/$',
        AssignLeaderToTrip.as_view(),
        name='assign_leader_to_trip',
    ),
    url(
        r'^remove/leader/(?P<leader_pk>[0-9]+)$',
        RemoveAssignedTrip.as_view(),
        name='remove_leader_from_trip',
    ),
]

foodbox_urlpatterns = [
    url(r'^rules/$', FoodboxRules.as_view(), name='rules'),
    url(r'^counts/$', FoodboxCounts.as_view(), name='counts'),
]

packet_urlpatterns = [
    url(r'^for/trip/(?P<pk>[0-9]+)/$', LeaderPacket.as_view(), name='trip'),
    url(
        r'^for/section/(?P<section_pk>[0-9]+)/$',
        PacketsForSection.as_view(),
        name='section',
    ),
    url(
        r'^medical/for/section/(?P<section_pk>[0-9]+)/$',
        MedicalInfoForSection.as_view(),
        name='medical',
    ),
]

checklist_urlpatterns = [
    url(r'^$', Checklists.as_view(), name='all'),
    url(
        r'^trippees/(?P<section_pk>[0-9]+)/$',
        TrippeeChecklist.as_view(),
        name='trippees',
    ),
    url(
        r'^leaders/(?P<section_pk>[0-9]+)/$', LeaderChecklist.as_view(), name='leaders'
    ),
]
