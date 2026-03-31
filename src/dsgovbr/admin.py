from django import urls
from django.utils.translation import gettext as _
from django.http import HttpRequest, HttpResponse
from dataclasses import dataclass
from functools import update_wrapper
from django.conf import settings
from django.forms import Media
from django.utils.text import capfirst
from django.urls import path, reverse
from django.db.models import Model
from django.contrib.admin import ModelAdmin, action
from django.contrib.admin.exceptions import NotRegistered
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.utils import quote, unquote
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR, flatten_fieldsets
from django.contrib.admin.helpers import AdminErrorList, AdminForm, InlineAdminFormSet
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.core.exceptions import PermissionDenied
from import_export.admin import ImportExportMixin, ExportActionMixin


@dataclass(frozen=True)
class ActionSpec:
    label: str
    handler: str
    icon: str = ""
    css_class: str = ""
    permission: str | None = None


@dataclass(frozen=True)
class ObjectToolSpec(ActionSpec):
    pass


@dataclass(frozen=True)
class InstanceActionSpec(ActionSpec):
    authorize: callable|None = None


class DSGovBrChangeList(ChangeList):
    def __init__(
            self,
            request,
            model,
            list_display,
            list_display_links,
            list_filter,
            date_hierarchy,
            search_fields,
            list_select_related,
            list_per_page,
            list_max_show_all,
            list_editable,
            model_admin,
            sortable_by,
            search_help_text,
        ):
        super().__init__(
            request,
            model,
            list_display,
            list_display_links,
            list_filter,
            date_hierarchy,
            search_fields,
            list_select_related,
            list_per_page,
            list_max_show_all,
            list_editable,
            model_admin,
            sortable_by,
            search_help_text,
        )
        self.title = str(capfirst(model_admin.opts.verbose_name_plural))

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse(
            "admin:%s_%s_view" % (self.opts.app_label, self.opts.model_name),
            args=(quote(pk),),
            current_app=self.model_admin.admin_site.name,
        )


class DSGovBrBaseModelAdmin(ModelAdmin):
    list_filter = []
    object_tools: list[ObjectToolSpec]|None = None
    instance_actions: list[InstanceActionSpec]|None = None

    def validate_object_tools(self):
        for object_tool in self.object_tools:
            if not isinstance(object_tool, ObjectToolSpec):
                raise TypeError(f"{object_tool} precisa ser ObjectToolSpec")
            if not hasattr(self, object_tool.handler):
                raise AttributeError(f"Handler '{object_tool.handler}' não existe em {self.__class__.__name__}")

    def get_custom_urls(self):
        # Gera rotas para todos métodos do self que terminam com _customview
        urls = []
        for attr_name in dir(self):
            if attr_name.endswith('_customview') and callable(getattr(self, attr_name)):
                urls.append(
                    path(
                        f"{attr_name}/",
                        self.admin_site.admin_view(getattr(self, attr_name)),
                        name=f"{self.opts.app_label}_{self.opts.model_name}_{attr_name}",
                    )
                )
        return urls

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        self.validate_object_tools()
        urls = [url for url in super().get_urls() if url.pattern.name is not None]
        prefix = f"{self.opts.app_label}_{self.opts.model_name}"
        urls.append(path("<path:object_id>/", wrap(self.preview_view), name=f"{prefix}_view"))
        
        return urls + self.get_custom_urls()

    def get_object_tool_actions(self, request: HttpRequest) -> list[ObjectToolSpec]:
        return [
            ObjectToolSpec(
                label=_("Change"),
                handler="change_view",
                css_class="change-link",
                permission=f"{self.opts.app_label}.change_{self.opts.model_name}",
            )
        ]

    def get_changelist(self, request, **kwargs):
        return DSGovBrChangeList

    def changelist_view(self, request: HttpRequest, extra_context: dict|None=None) -> HttpResponse:
        extra_context = extra_context or {}
        extra_context["object_tool_actions"] = self.get_object_tool_actions(request)
        return super().changelist_view(request, extra_context=extra_context)

    def preview_view(self, request: HttpRequest, object_id: str, form_url: str="", extra_context: dict|None=None) -> HttpResponse:
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(f"The field {to_field} cannot be referenced.")

        obj = self.get_object(request, unquote(object_id), to_field)
        try:
            related_modeladmin = self.admin_site.get_model_admin(obj.__class__)
        except NotRegistered as e:
            wrapper_kwargs = {}
        else:
            wrapper_kwargs = {
                "can_add_related": related_modeladmin.has_add_permission(request),
                "can_change_related": related_modeladmin.has_change_permission(request),
                "can_delete_related": related_modeladmin.has_delete_permission(request),
                "can_view_related": related_modeladmin.has_view_permission(request),
            }        

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied

        request.in_view_mode = True

        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(request, obj, change=False, fields=flatten_fieldsets(fieldsets))
        form = ModelForm(instance=obj)
        formsets, inline_instances = self._create_formsets(request, obj, change=True)

        # form = self._get_form_for_get_fields(request, obj)
        # return [*form.base_fields, *self.get_readonly_fields(request, obj)]
        readonly_fields = [*form.base_fields, *self.get_readonly_fields(request, obj)]
        admin_form = AdminForm(form, list(fieldsets), {}, readonly_fields, model_admin=self)
        media = self.media + admin_form.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        # inline_formsets = []
        for inline_formset in inline_formsets:
            media += inline_formset.media
            inline_formset.readonly_fields = flatten_fieldsets(inline_formset.fieldsets)

        can_add_related = wrapper_kwargs.get('can_add_related', False)
        can_delete_related = wrapper_kwargs.get('can_delete_related', False)
        can_change_related = wrapper_kwargs.get('can_change_related', False)
        can_view_related = wrapper_kwargs.get('can_view_related', False)

        context = {
            **self.admin_site.each_context(request),
            "title": str(capfirst(self.opts.verbose_name_plural)),
            "subtitle": str(obj) if obj else None,
            "adminform": admin_form,
            "object_id": object_id,
            "original": obj,
            "is_popup": IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            "to_field": to_field,
            "media": media,
            "inline_admin_formsets": inline_formsets,
            "errors": AdminErrorList(form, formsets),
            "preserved_filters": self.get_preserved_filters(request),

            "has_delete_permission": can_delete_related,
            "show_delete": can_delete_related,
            'show_delete_link': can_delete_related,
            'can_delete_related': can_delete_related,

            "has_add_permission": can_add_related,

            "show_change": can_change_related,
            "can_change_related": can_change_related,

            'show_save': False,
            'show_save_as_new': False,
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
            'show_change_form_export': True,

            'can_view_related': can_view_related,
        }


        context.update(extra_context or {})

        return self.render_change_form(request, context, add=False, change=False, obj=obj, form_url=form_url)

    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        # Edit permissions on parent model are required for editable inlines.
        if getattr(request, "in_view_mode", False):
            can_edit_parent = False
        else:
            can_edit_parent = self.has_change_permission(request, obj) if obj else self.has_add_permission(request)

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            if can_edit_parent:
                has_add_permission = inline.has_add_permission(request, obj)
                has_change_permission = inline.has_change_permission(request, obj)
                has_delete_permission = inline.has_delete_permission(request, obj)
            else:
                # Disable all edit-permissions, and override formset settings.
                has_add_permission = has_change_permission = has_delete_permission = False
                formset.extra = formset.max_num = 0
            has_view_permission = inline.has_view_permission(request, obj)
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = InlineAdminFormSet(
                inline,
                formset,
                fieldsets,
                prepopulated,
                readonly,
                model_admin=self,
                has_add_permission=has_add_permission,
                has_change_permission=has_change_permission,
                has_delete_permission=has_delete_permission,
                has_view_permission=has_view_permission,
            )
            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets

    def get_instance_action_allowed(self, request: HttpRequest, instance: Model, action: InstanceActionSpec) -> bool:
        return (action.permission is None or request.user.has_perm(action.permission)) and (action.authorize is None or action.authorize(request, instance))

    def get_instance_actions(self, request: HttpRequest, instance: Model) -> list[InstanceActionSpec]|None:
        return [a for a in (self.instance_actions or []) if self.is_valid_handler(a) and self.get_instance_action_allowed(request, instance, a)]

    def is_valid_handler(self, a: ActionSpec) -> bool:
        return hasattr(self, a.handler) and callable(getattr(self, a.handler))

    def get_handler(self, spec: ActionSpec) -> callable|None:
        return getattr(self, spec.handler) if hasattr(self, spec.handler) and callable(getattr(self, spec.handler)) else None

    @property
    def media(self):
        parent_media = super().media if hasattr(super(), 'media') else Media()
        extra = "" if settings.DEBUG else ".min"
        js = [
            "vendor/jquery/jquery%s.js" % extra,
            "jquery.init.js",
            "core.js",
            "admin/RelatedObjectLookups.js",
            # "actions.js", # Este arquivo causa problema pois não usamos neste tema o padrão do django admin de actions
            "urlify.js",
            "prepopulate.js",
            "vendor/xregexp/xregexp%s.js" % extra,
            # JS customizado dos filtros DSGovBR
            "dsgovbr_admin_filters.js",
            "dsgovbr_admin_actions.js",
            "dsgovbr_admin_submit_line.js",
        ]
        return parent_media + Media(js=["admin/js/%s" % url for url in js])


class DSGovBrModelAdmin(ImportExportMixin, ExportActionMixin, DSGovBrBaseModelAdmin):
    pass
