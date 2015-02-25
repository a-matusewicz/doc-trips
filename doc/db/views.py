import logging

from django.db import models
from django.http import Http404, HttpResponseRedirect
from django.conf.urls import url
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import modelform_factory
from django.db import IntegrityError, transaction
from django.core.exceptions import NON_FIELD_ERRORS, ImproperlyConfigured, PermissionDenied
from vanilla import (ListView, UpdateView, CreateView, DeleteView, 
                     TemplateView, DetailView, RedirectView)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, ButtonHolder, Layout

from doc.db.models import DatabaseModel, TripsYear
from doc.db.forms import tripsyear_modelform_factory
from doc.permissions.views import DatabasePermissionRequired

logger = logging.getLogger(__name__)


class PassesTestMixin():

    def test_func(self):
        msg = 'Implement test_func'
        raise ImproperlyConfigured(msg)
        
    def dispatch(self, request, *args, **kwargs):
        
        if not self.test_func():
            raise PermissionDenied
        
        return super(PassesTestMixin, self).dispatch(request, *args, **kwargs)

class RedirectIfPassesTest():

    redirect_url = None
    
    def test_func(self):
        msg = 'Implement test_func'
        raise ImproperlyConfigured(msg)

    def get_redirect_url(self):
        
        if redirect_url is None:
            msg = "Add 'redirect_url' or implement 'get_redirect_url'"
            raise ImproperlyConfigurd(msg)
        
        return redirect_url

    def dispatch(self, request, *args, **kwargs):
        
        if self.test_func():
            return HttpResponseRedirect(self.get_redirect_url())
        
        return super(PassesTestMixin, self).dispatch(request, *args, **kwargs)
    


class CrispyFormMixin():
    """
    Class view mixin which adds support for crispy_forms.

    TODO: needs tests.
    """
    
    def get_form_helper(self, form):
        """ Return a configured crispy FormHelper. """

        return FormHelper(form)

    def get_form(self, **kwargs):
        """ 
        Attach a crispy form helper to the form, if it does not already have one.
        """

        form = super(CrispyFormMixin, self).get_form(**kwargs)

        if not hasattr(form, 'helper'):
            form.helper = self.get_form_helper(form)

        self.validate_crispy_layout(form)

        return form

    def validate_crispy_layout(self, form):
        """
        Validates that all fields in the form appear in the crispy layout.
        Catches a tricky bug wherein some required fields specified on the form
        are accidentally left out of an explicit layout, causing POSTS to fail.
        """
        
        if hasattr(form.helper, 'layout'):
            # all fields in the layout
            layout_fields = set(map(lambda f: f[1], form.helper.layout.get_field_names()))
            # and in the form
            form_fields = set(form.fields.keys())

            if form_fields - layout_fields:
                msg = ('whoa there, make sure you include ALL fields specified by '
                       '%s in the Crispy Form layout. %r are missing')
                raise ImproperlyConfigured(msg % (self.__class__.__name__, form_fields-layout_fields))
        

class TripsYearMixin():
    """ 
    Mixin for trips_year.

    Filters objects by the trips_year named group in the url.

    Plugs into ModelViews. The url is a database url of the form
    /something/{{trips_year}}/something. The ListView will only display 
    objects for the specified trips_year.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Make sure the request is for a valid trips year.
        
        Requesting trips_years that don't exist in the db will
        cause problems. Block 'em here. 
        
        TODO: test cases.
        """
        
        trips_year = self.kwargs['trips_year']
        if not TripsYear.objects.filter(year=trips_year).exists():
            msg = 'Trips %s does not exist in the database'
            raise Http404(msg % trips_year)

        return super(TripsYearMixin, self).dispatch(request, *args, **kwargs)
            

    def get_queryset(self):
        """ Get objects for requested trips_year """

        qs = super(TripsYearMixin, self).get_queryset()
        return qs.filter(trips_year=self.kwargs['trips_year'])


    def get_form_class(self):
        """ 
        Restricts the choices in foreignkey form fields to objects with the
        same trips year.

        Because we can't use an F() object in limit_choices_to.

        formfield_callback is responsible for constructing a FormField 
        from a passed ModelField. Our callback intercepts the usual ForeignKey
        implementation, and only lists choices which have trips_year == to 
        the trips_year matched in the url.
        """

        if self.form_class is not None:
            msg = ('Specifying form_class on %s means that ForeignKey querysets will'
                   'contain objects for ALL trips_years. You must explicitly restrict'
                   'the querysets for these fields, or bad things will happen')
            logger.warn(msg % self.__class__.__name__)
            return self.form_class

        if self.model is not None:
            trips_year = self.kwargs['trips_year']
            return tripsyear_modelform_factory(self.model, trips_year,
                                               fields=self.fields)
        
        msg = "'%s' must either define 'form_class' or 'model' " \
            "Or CAREFULLY override 'get_form_class()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def form_valid(self, form):
        """ 
        Called for valid forms - specifically Create and Update
 
        This deals with a corner case of form validation. Uniqueness 
        constraints don't get caught til the object is saved and raises 
        an IntegrityError.

        We catch this error and pass it to form_valid.

        TODO: parse and prettify the error message. Can we look at 
        object._meta.unique_together? Can we make sure it is a uniqueness
        error?
        """
        try:
            with transaction.atomic():
                return super(TripsYearMixin, self).form_valid(form)
        except IntegrityError as e:
            form.errors[NON_FIELD_ERRORS] = form.error_class([e.__cause__])
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """ Add the trips_year for this request to the context. """
        context = super(TripsYearMixin, self).get_context_data(**kwargs)
        context['trips_year'] = self.kwargs['trips_year']
        return context


class DatabaseMixin(DatabasePermissionRequired, TripsYearMixin):
    """
    If the user is not logged in, redirect 
    the login page. If the user is logged in, but does not have
    database-viewing privileges, display a 403 Forbidden page.
    """

    @classmethod
    def urlpattern(cls):
        """ 
        Return the default urlpattern for this view 

        Implemented on subclass, this is just an interface stub
        """
        msg = 'Not implemented. Implement urlpattern() method on {}'
        raise ImproperlyConfigured(msg.format(cls))

    @classmethod
    def view_name(cls):
        
        msg = 'Not implemented'
        raise ImproperlyConfigured(msg)

    def get_context_data(self, **kwargs):
        """
        Adds the 'model' of the modelview to the context.

        This along with 'trips_year' add by TripsYearMixin, 
        is useful for adding 'create' links to templates.
        """
        
        context = super(DatabaseMixin, self).get_context_data(**kwargs)
        context['model'] = self.model
        return context

    def form_invalid(self, form):
        
        messages.error(self.request, 'Uh oh! There seems to be an error in the form.')
        return super(DatabaseMixin, self).form_invalid(form)

class DatabaseListView(DatabaseMixin, ListView):

    def get_template_names(self):
        """ Get the template for the ListView """
        if self.template_name:
            return [self.template_name]
        
        # auto-generate    TODO: use super() conventions?
        template_name = '{}/{}_index.html'.format(
            self.model.get_app_name(), 
            self.model.get_model_name_lower()
        )
        return [template_name]
    
    @classmethod
    def urlpattern(cls):
        name = '{}_index'.format(cls.model.get_model_name_lower())
        return url(r'^$', cls.as_view(), name=name)


class DatabaseCreateView(DatabaseMixin, CrispyFormMixin, CreateView):
    template_name = 'db/create.html'

    @classmethod
    def urlpattern(cls):
        name = '{}_create'.format(cls.model.get_model_name_lower())
        return url(r'^create$', cls.as_view(), name=name)

    def post(self, request, *args, **kwargs):
        """ 
        Add trips_year to created object.

        This is the vanilla CreateView, verbatim, with the addition
        of the trips_year.
        """
        form = self.get_form(data=request.POST, files=request.FILES)
        form.instance.trips_year_id = self.kwargs['trips_year']
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_helper(self, form):
        """ Add 'Create' button to crispy form. """
        helper = FormHelper(form)
        helper.add_input(Submit('submit', 'Create'))

        
        return helper

    def get_success_url(self):
        """ TODO: for now... """
        from doc.db.urlhelpers import reverse_detail_url
        return reverse_detail_url(self.object)


class DatabaseUpdateView(DatabaseMixin, CrispyFormMixin, UpdateView):
    template_name ='db/update.html'

    @classmethod
    def urlpattern(cls):
        name = '{}_update'.format(cls.model.get_model_name_lower())
        return url(r'^(?P<pk>[0-9]+)/update', cls.as_view(), name=name)

    def get_success_url(self):
        """ Redirect to same update page for now. """
        from doc.db.urlhelpers import reverse_detail_url
        return reverse_detail_url(self.object)

    def get_form_helper(self, form):
        """ Add Submit and delete buttons to the form. """

        from doc.db.urlhelpers import reverse_delete_url
        helper = FormHelper(form)
        helper.layout.append(
            ButtonHolder(
                Submit('submit', 'Update'),
                HTML('<a href="{}" class="btn btn-danger" role="button">Delete</a>'.format(
                    reverse_delete_url(self.object)))
            )
        )
        return helper
    

class DatabaseDeleteView(DatabaseMixin, DeleteView):
    template_name = 'db/delete.html'

    success_url_pattern = None

    def get_success_url(self):
        """ Helper method for getting the success url based on 
        succes_url_pattern. 

        CreateView and UpdateView use the models get_absolute_url
        to find the success_url. DeleteView cannot do this because the
        target object hsa been deleted.
        """

        if self.success_url_pattern:
            kwargs = {'trips_year': self.kwargs['trips_year']}
            return reverse(self.success_url_pattern, kwargs=kwargs)

        return super(DatabaseDeleteView, self).get_success_url()

    def post(self, request, *args, **kwargs):

        try:
            return super(DatabaseDeleteView, self).post(request, *args, **kwargs)

        except models.ProtectedError as e:
            msg = "Oops, you can't delete {} {} because the following objects reference it: {}." 
            msg = msg.format(self.object._meta.model.__name__, self.object, e.protected_objects)
            messages.error(request, msg)

            return HttpResponseRedirect(request.path)

    @classmethod
    def urlpattern(cls):
        name = '{}_delete'.format(cls.model.get_model_name_lower())
        return url(r'^(?P<pk>[0-9]+)/delete', cls.as_view(), name=name)


class DatabaseDetailView(DatabaseMixin, DetailView):

    template_name = 'db/detail.html'
    
    # Fields to display in the view. Passed in the template.
    fields = None
    
    @classmethod
    def urlpattern(cls):
        name = '{}_detail'.format(cls.model.get_model_name_lower())
        return url(r'^(?P<pk>[0-9]+)/$', cls.as_view(), name=name)
        

class DatabaseIndexView(DatabasePermissionRequired, TripsYearMixin, TemplateView):
    """ 
    Index page of a particular trips year. 

    TODO: should this display the ScheduledTrips index? 
    """
    template_name = 'db/db_index.html'


class RedirectToCurrentDatabase(DatabasePermissionRequired, RedirectView):
    """ 
    Redirect to the trips database for the current year. 

    This view is the target of database urls.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        
        trips_year = TripsYear.objects.current()
        return reverse('db:db_index', kwargs={'trips_year': trips_year.pk})
    
