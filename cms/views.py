# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
    SuperuserRequiredMixin,
)

from base.view_utils import BaseMixin
from block.views import (
    Page,
    PageDesignView,
    PageView,
    Section,
)

from .forms import (
    HeaderFooterForm,
    PageForm,
    SectionForm,
    TemplateForm,
    TemplateSectionEmptyForm,
    TemplateSectionForm,
)
from .models import (
    HeaderFooter,
    Template,
    TemplateSection,
)


class CmsPageView(PageView):

    def get_context_data(self, **kwargs):
        context = super(CmsPageView, self).get_context_data(**kwargs)
        context.update(dict(header_footer=HeaderFooter.load()))
        return context


class CmsPageDesignView(PageDesignView):

    def get_context_data(self, **kwargs):
        context = super(CmsPageDesignView, self).get_context_data(**kwargs)
        context.update(dict(header_footer=HeaderFooter.load()))
        return context


class HeaderFooterUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = HeaderFooterForm
    model = HeaderFooter

    def get_object(self, queryset=None):
        return HeaderFooter.load()

    def get_success_url(self):
        return reverse('cms.page.list')


class PageCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = PageForm
    model = Page

    def form_valid(self, form):
        template = form.cleaned_data.get('template')
        with transaction.atomic():
            self.object = form.save()
            template.setup_page(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('cms.page.list')


class PageListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Page
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        context.update(dict(
            pages=Page.objects.menu(),
        ))
        return context


class PageUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = PageForm
    model = Page

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""
        try:
            template = Template.objects.get(
                template_name=self.object.template_name
            )
            return dict(template=template)
        except Template.DoesNotExist:
            return dict()

    def form_valid(self, form):
        template = form.cleaned_data.get('template')
        with transaction.atomic():
            self.object = form.save(commit=False)
            template.setup_page(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('cms.page.list')


class SectionCreateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, CreateView):

    form_class = SectionForm
    model = Section

    def get_success_url(self):
        return reverse('cms.section.list')


class SectionListView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, ListView):

    model = Section
    paginate_by = 15


class SectionUpdateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, UpdateView):

    form_class = SectionForm
    model = Section

    def get_success_url(self):
        return reverse('cms.section.list')


class TemplateCreateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, CreateView):

    form_class = TemplateForm
    model = Template

    def get_success_url(self):
        return reverse('cms.template.list')


class TemplateListView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, ListView):

    model = Template
    paginate_by = 15


class TemplateSectionCreateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, CreateView):

    form_class = TemplateSectionForm
    model = TemplateSection

    def _get_template(self):
        pk = self.kwargs.get('pk', None)
        template = Template.objects.get(pk=pk)
        return template

    def get_context_data(self, **kwargs):
        context = super(
            TemplateSectionCreateView, self
        ).get_context_data(**kwargs)
        context.update(dict(template=self._get_template()))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.template = self._get_template()
        return super(TemplateSectionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cms.template.list')


class TemplateSectionRemoveView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TemplateSectionEmptyForm
    model = TemplateSection
    template_name = 'cms/templatesection_remove_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('cms.template.list')


class TemplateUpdateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TemplateForm
    model = Template

    def get_success_url(self):
        return reverse('cms.template.list')
