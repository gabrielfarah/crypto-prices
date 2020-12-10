# Create your views here.
import csv
import io
from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LoginView,
)
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import now as utc_now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


#
#
# from coins import settings
# from utils.csv import stream_csv_list_of_dicts_view
# from website.forms import (
#     CustomAuthenticationForm,
#     AccountUserForm,
#     UserForm,
#     AccountForm,
#     ServiceAPIKeyForm,
# )
# from website.forms import PipelineRunForm, CreatePipelineForm
#
#
# def index(request):
#     return render(request, "pages/index.html", {})
#
#
# class ServicesDocsView(TemplateView):
#     template_name = "docs/service_detail.html"
#     view_name = "service_doc_detail_view"
#
#     def get(self, request, *args, **kwargs):
#         service_name = kwargs["service_name"]
#         services = Service.objects.all()
#         service = get_object_or_404(Service, name=service_name)
#         return render(
#             request, self.template_name, {"service": service, "services": services}
#         )
#
#
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect(DashboardView.view_name)
#     if request.method == "POST":
#         user_form = UserForm(request.POST or None)
#         account_form = AccountForm(request.POST or None)
#         if user_form.is_valid() and account_form.is_valid():
#             # create a new user first
#             user = user_form.save()
#             user.refresh_from_db()  # load the profile instance created by the signal
#             # create an object in memory but not save it
#             account_obj = account_form.save(commit=False)
#             account_obj.admin = user
#             account_obj.accepted_terms = True
#             account_obj.validated = True
#             account_obj.active = True
#             account_obj.time_of_validation = utc_now()
#             account_obj.time_of_accepted_terms = utc_now()
#             account_obj.save()
#             raw_password = user_form.cleaned_data.get("password1")
#             user = authenticate(email=user.email, password=raw_password)
#             login(request, user)
#             return redirect(DashboardView.view_name)
#     else:
#         user_form = UserForm()
#         account_form = AccountForm()
#     return render(
#         request,
#         "auth/signup.html",
#         {"user_form": user_form, "account_form": account_form},
#     )
#
#
# class CustomPasswordReset(PasswordResetView):
#     email_template_name = "auth/password_reset_email.html"
#     template_name = "auth/password_reset_form.html"
#     success_url = reverse_lazy("custom_password_reset_done")
#
#
# class CustomLogoutView(LogoutView):
#     template_name = "auth/logged_out.html"
#
#
# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     template_name = "auth/password_reset_done.html"
#
#
# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = "auth/password_reset_confirm.html"
#     success_url = reverse_lazy("custom_password_reset_complete")
#
#
# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = "auth/password_reset_complete.html"
#
#
# class CustomLoginView(LoginView):
#     template_name = "auth/login.html"
#     form_class = CustomAuthenticationForm
#
#
# class CustomLogoutView(LogoutView):
#     template_name = "auth/logged_out.html"
#
#
# def obtain_api_calls(request, delta="Day", limit=100):
#     # Q(api_key=ServiceBaseView.get_api_key(request)) | Q(api_key__account__admin=request.user)
#     if delta == "Day":
#         return (
#             APICall.objects.filter(api_key__account__admin=request.user)
#             .annotate(day=TruncDay("created_at"))
#             .values("day")
#             .annotate(count=Count("id"))
#             .values("day", "count")
#         )
#     elif delta == "Month":
#         return (
#             APICall.objects.filter(api_key__account__admin=request.user)
#             .annotate(day=TruncMonth("created_at"))
#             .values("month")
#             .annotate(count=Count("id"))
#             .values("month", "count")
#         )
#     else:
#         return (
#             APICall.objects.filter(api_key__account__admin=request.user)
#             .order_by("-id")
#             .values("created_at", "state", "finished_at", "response_payload")[:limit]
#         )
#
#
# class DashboardView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     template_name = "dashboard/main.html"
#     view_name = "main_dashboard"
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         context["account"] = request.user
#         context["api_calls_agg"] = obtain_api_calls(request)
#         context["api_calls"] = obtain_api_calls(request, delta="full")
#         api_form = ServiceAPIKeyForm()
#         context["api_form"] = api_form
#         return self.render_to_response(context)
#
#
# @method_decorator(xframe_options_exempt, name="dispatch")
# @method_decorator(csrf_exempt, name="dispatch")
# class IOUSigningView(TemplateView):
#     template_name = "iou/signing.html"
#     view_name = "iou_signing"
#
#
# class PipelineFormDoneView(TemplateView):
#     view_name = "pipeline_form_done"
#     template_name = "pipeline/form_done.html"
#     form_class = CreatePipelineForm
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {"view_name": self.view_name})
#
#
# @method_decorator(xframe_options_exempt, name="dispatch")
# @method_decorator(csrf_exempt, name="dispatch")
# class PipelineFormDoneIFrameView(TemplateView):
#     view_name = "pipeline_form_done_iframe"
#     template_name = "pipeline/form_done_iframe.html"
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {"view_name": self.view_name})
#
#
# class PipelineRunFormView(TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     template_name = "pipeline/run-form.html"
#     view_name = "pipeline_run_form"
#     form_class = PipelineRunForm
#     redirect_done = PipelineFormDoneView
#
#     @staticmethod
#     def clean_presets(pipeline_schema, pipeline_form):
#         services = pipeline_form.pipeline.services.all()
#         contracts = ServiceContract.objects.filter(service__in=services).exclude(
#             presets__isnull=True
#         )
#         for contract in contracts:
#             for key in contract.presets.keys():
#                 if key in pipeline_schema["properties"]:
#                     pipeline_schema["properties"].pop(key, None)
#         return pipeline_schema
#
#     def get(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         pipeline_form = get_object_or_404(PipelineForm, link_id=link_id)
#         if pipeline_form.visibility == PipelineForm.PRIVATE:
#             if (
#                 pipeline_form.pipeline.account.admin != request.user
#                 and request.user not in pipeline_form.invited_users.all()
#             ):
#                 raise Http404("User %s is not allowed to this form." % request.user)
#         pipeline = pipeline_form.pipeline
#         schema = self.clean_presets(pipeline.pipeline_schema, pipeline_form)
#         form = self.form_class(schema=schema)
#         return render(
#             request,
#             self.template_name,
#             {
#                 "form": form,
#                 "view_name": self.view_name,
#                 "link_id": link_id,
#                 "pipeline_form": pipeline_form,
#             },
#         )
#
#     def post(self, request, *args, **kwargs):
#         link_id = kwargs.pop("link_id")
#         pipeline_form = get_object_or_404(PipelineForm, link_id=link_id)
#         pipeline = pipeline_form.pipeline
#         schema = self.clean_presets(pipeline.pipeline_schema, pipeline_form)
#         form = self.form_class(data=request.POST, schema=schema)
#         if form.is_valid():
#             request.data = form.cleaned_data
#             request.data["pipeline_id"] = str(pipeline.id)
#             request.META[str(settings.API_KEY_CUSTOM_HEADER)] = str(
#                 pipeline_form.secret_key
#             )
#             resp = PipelineRunCreateView().post(request)
#             pipeline_run = get_object_or_404(
#                 PipelineRun, run_id=resp.data.get("run_id")
#             )
#             pipeline_run.form = pipeline_form
#             pipeline_run.save()
#             return redirect(self.redirect_done.view_name)
#         return render(request, self.template_name, {"form": form})
#
#
# @method_decorator(xframe_options_exempt, name="dispatch")
# @method_decorator(csrf_exempt, name="dispatch")
# class PipelineRunFormIFrameView(PipelineRunFormView):
#     template_name = "pipeline/run_form_iframe.html"
#     view_name = "pipeline_run_form_iframe"
#     redirect_done = PipelineFormDoneIFrameView
#
#
# class PipelineFormListView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     view_name = "pipeline_form_list"
#     template_name = "pipeline/pipeline_form_list.html"
#     form_class = CreatePipelineForm
#
#     def get(self, request, *args, **kwargs):
#         pipeline_forms = PipelineForm.objects.filter(
#             Q(pipeline__account__admin=request.user) | Q(invited_users=request.user)
#         ).order_by("-created_at")
#         services = Service.objects.filter(
#             servicecontract__account__admin=request.user,
#             servicecontract__accepted_terms=True,
#             servicecontract__validated=True,
#         )
#         form = self.form_class(services)
#         paginator = Paginator(pipeline_forms, 10)  # Show 25 runs per page
#
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(
#             request,
#             self.template_name,
#             {
#                 "pipeline_forms": page_obj,
#                 "form": form,
#                 "view_name": self.view_name,
#                 "form_details_view": PipelineRunFormView.view_name,
#                 "form_responses_view": PipelineRunResponsesView.view_name,
#             },
#         )
#
#
# class PipelineFormCreateView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     view_name = "pipeline_form_create"
#     template_name = "pipeline/pipeline_form_create.html"
#     form_class = CreatePipelineForm
#
#     def get(self, request, *args, **kwargs):
#         services = Service.objects.filter(
#             servicecontract__account__admin=request.user,
#             servicecontract__accepted_terms=True,
#             servicecontract__validated=True,
#         )
#         form = self.form_class(services)
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request, *args, **kwargs):
#         services = Service.objects.filter(
#             servicecontract__account__admin=request.user,
#             servicecontract__accepted_terms=True,
#             servicecontract__validated=True,
#         )
#         form = self.form_class(services, data=request.POST)
#         if form.is_valid():
#             account = get_object_or_404(Account, admin=request.user)
#             pipeline = Pipeline.objects.create(account=account)
#             pipeline.services.add(*form.cleaned_data["services"])
#             pipeline.save()
#             pipeline_form = PipelineForm.objects.create(
#                 name=form.cleaned_data["name"],
#                 pipeline=pipeline,
#                 visibility=form.cleaned_data["visibility"],
#             )
#             url = reverse(
#                 PipelineRunFormView.view_name, kwargs={"link_id": pipeline_form.link_id}
#             )
#             return HttpResponseRedirect(url)
#         return render(request, self.template_name, {"form": form})
#
#
# def get_pipeline_run_admin_or_invited(request, link_id):
#     pipeline_runs = PipelineRun.objects.filter(
#         form__link_id=link_id, pipeline__account__admin=request.user
#     ).order_by("-created_at")
#     if not pipeline_runs:
#         pipeline_runs = PipelineRun.objects.filter(
#             created_by=request.user, form__link_id=link_id
#         ).order_by("-created_at")
#     if not pipeline_runs:
#         raise Http404("User %s is not allowed to this form." % request.user)
#     return pipeline_runs
#
#
# class PipelineRunResponsesView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     template_name = "pipeline/pipeline_form_responses.html"
#     view_name = "pipeline_run_response_view"
#
#     def get(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         pipeline_runs = get_pipeline_run_admin_or_invited(request, link_id)
#         paginator = Paginator(pipeline_runs, 25)  # Show 25 runs per page
#
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(
#             request,
#             self.template_name,
#             {
#                 "pipeline_runs": page_obj,
#                 "link_id": link_id,
#                 "view_name": PipelineRunResponseDetailView.view_name,
#             },
#         )
#
#
# class PipelineRunResponsesExportView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     view_name = "pipeline_run_response_export_view"
#     transform_dict = {"experian-hcpn-co": flatten_experian}
#
#     def get(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         pipeline_runs = get_pipeline_run_admin_or_invited(request, link_id)[:5000]
#         if pipeline_runs:
#             rows = []
#             global_dict = {
#                 "detail_url": "",
#                 "created_at": "",
#                 "state": "",
#                 "service_name": "",
#             }
#             for pipe in pipeline_runs:
#                 results = pipe.response_payload.get("result", [])
#                 for result in results:
#                     data = result.get("data", {})
#                     service_name = result.get("service_name")
#                     flattened = self.transform_dict.get(service_name, flatten_generic)(
#                         data
#                     )
#                     row = {
#                         "detail_url": pipe.run_id,
#                         "created_at": pipe.created_at,
#                         "state": pipe.state,
#                         "service_name": service_name,
#                     }
#                     for k, v in flattened.items():
#                         if k not in global_dict:
#                             global_dict[k] = ""
#                         row[k] = v
#                     rows.append(row)
#             response = stream_csv_list_of_dicts_view(
#                 rows, "export", headers=[str(k) for k in global_dict.keys()]
#             )
#             return response
#         return stream_csv_list_of_dicts_view([{}], "export", headers=[])
#
#
# class PipelineRunResponseDetailView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     template_name = "pipeline/pipeline_form_response_detail.html"
#     view_name = "pipeline_run_response_view_detail"
#
#     def get(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         run_id = kwargs["run_id"]
#         pipeline_run = get_object_or_404(
#             PipelineRun,
#             Q(pipeline__account__admin=request.user) | Q(created_by=request.user),
#             run_id=run_id,
#             form__link_id=link_id,
#         )
#         return render(
#             request,
#             self.template_name,
#             {
#                 "pipeline_run": pipeline_run,
#                 "view_name": self.view_name,
#             },
#         )
#
#
# class BatchFormFillView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     view_name = "pipeline_run_batch_upload_view"
#
#     # form_class = UploadPipelineRunFileForm
#
#     @staticmethod
#     def check_has_permission(request, pipeline_form):
#         if pipeline_form.visibility == PipelineForm.PRIVATE:
#             if (
#                 pipeline_form.pipeline.account.admin != request.user
#                 and request.user not in pipeline_form.invited_users.all()
#             ):
#                 raise PermissionDenied()
#
#     def get(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         pipeline_form = get_object_or_404(PipelineForm, link_id=link_id)
#         self.check_has_permission(request, pipeline_form)
#         pipeline = pipeline_form.pipeline
#         schema = PipelineRunFormView.clean_presets(
#             pipeline.pipeline_schema, pipeline_form
#         )
#         headers = []
#         for k in schema.get("properties").keys():
#             if str(k) in form_equivalences["labels"]:
#                 headers.append(form_equivalences["labels"][str(k)][0])
#             else:
#                 headers.append(to_clean(str(k)))
#         example = {}
#         for x in headers:
#             example[x] = _("<PASTE YOUR DATA HERE>")
#         rows = [example]
#         xls_name = "{} {}".format(pipeline_form.name, _("Template"))
#         return stream_csv_list_of_dicts_view(rows, xls_name, headers=headers)
#
#     @staticmethod
#     def transform_type(value, value_type, error_msg):
#         try:
#             return value_type(value)
#         except ValueError:
#             raise ValueError(error_msg)
#
#     def validate_fields_types(self, schema, value):
#         value = value.strip()
#         if "format" in schema:
#             # Then it must be a date, so lets check for the right YYYY-MM-DD format
#             try:
#                 return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
#             except ValueError:
#                 msg = _(
#                     'The value "%(val)s" is not a valid date. The correct format for dates is YYYY-MM-DD'
#                 ) % {"val": value}
#                 raise ValueError(msg)
#         elif "enum" in schema:
#             choices = schema.get("enum")
#             if value.lower() in choices:
#                 return value.lower()
#             msg = _('Change "%(val)s" for one of the correct options: %(choices)s') % {
#                 "val": value,
#                 "choices": ", ".join('"{0}"'.format(w) for w in choices),
#             }
#             raise ValueError(msg)
#         else:
#             type_item = schema.get("type")
#             if type_item == "integer":
#                 msg = '"{}" {}'.format(value, _("must be an integer"))
#                 return self.transform_type(value, int, msg)
#             elif type_item == "number":
#                 msg = '"{}" {}'.format(value, _("must be a number"))
#                 return self.transform_type(value, float, msg)
#             elif type_item == "boolean":
#                 true_values = [
#                     "true",
#                     "verdadero",
#                     "verdad",
#                     "verdade",
#                     "verdadeiro",
#                     "yes",
#                     "si",
#                     "sim",
#                 ]
#                 false_values = ["false", "falso", "no", "não"]
#                 if value is True or value.lower() in true_values:
#                     return True
#                 elif value is False or value.lower() in false_values:
#                     return False
#                 else:
#                     msg = _(
#                         'The value "%(val)s" must be one of the following options %(options)s'
#                     ) % {
#                         "val": value,
#                         "options": ", ".join(
#                             '"{0}"'.format(w) for w in (true_values + false_values)
#                         ),
#                     }
#                     raise ValueError(msg)
#             else:
#                 if "minLength" in schema:
#                     if len(value) < schema.get("minLength"):
#                         msg = _(
#                             'The value "%(val)s" must be longer than or equal to %(num)s characters'
#                         ) % {"val": value, "num": schema.get("minLength")}
#                         raise ValueError(msg)
#                 if "maxLength" in schema:
#                     if len(value) > schema.get("maxLength"):
#                         msg = _(
#                             'The value "%(val)s" must be less than or equal to %(num)s characters'
#                         ) % {"val": value, "num": schema.get("maxLength")}
#                         raise ValueError(msg)
#                 return str(value)
#
#     def validate_row(self, idx, row, equivalences, schema, form_keys):
#         cleaned = {}
#         for k, v in row.items():
#             if k and not v:
#                 msg = _(
#                     'In the row %(idx)s of your file, the value for the column "%(k)s" is empty'
#                 ) % {"idx": idx, "k": k}
#                 raise ValueError(msg)
#             elif v and not k:
#                 msg = _(
#                     'In the row %(idx)s of your file, the value "%(v)s" is not part of any column'
#                 ) % {"idx": idx, "v": v}
#                 raise ValueError(msg)
#             elif k and v:
#                 if k in equivalences:
#                     try:
#                         parsed_v = self.validate_fields_types(
#                             schema["properties"][equivalences[k]], v
#                         )
#                         cleaned[equivalences[k]] = parsed_v
#                     except ValueError as e:
#                         msg = _(
#                             'The value "%(v)s" for the column "%(k)s" for the row %(idx)s is not valid. %(e)s'
#                         ) % {"v": v, "k": k, "idx": idx, "e": e}
#                         raise ValueError(msg)
#                 else:
#                     valid_columns = []
#                     valid_columns_original = []
#                     for x in form_keys:
#                         valid_columns.append(form_equivalences["labels"][x][0])
#                         valid_columns_original.append(x)
#                     msg = _(
#                         'The column "%(k)s" does not match with the list of fields of this form. The possible values '
#                         "of the columns are %(col)s or %(col2)s. Please download the template for this form and "
#                         "make sure all the columns you are uploading match with the ones in the file "
#                     ) % {
#                         "k": k,
#                         "col": ", ".join('"{0}"'.format(w) for w in valid_columns),
#                         "col2": ", ".join(
#                             '"{0}"'.format(w) for w in valid_columns_original
#                         ),
#                     }
#                     raise ValueError(msg)
#             else:
#                 # there might be empty columns + values, we omit those
#                 pass
#         if sorted(cleaned.keys()) != form_keys:
#             msg = _("The row %(idx)s of your file is not valid") % {"idx": idx}
#             raise ValueError(msg)
#         return cleaned
#
#     def error_response(self, msg, request):
#         return render(
#             request,
#             PipelineFormDoneView.template_name,
#             {
#                 "errors": msg,
#                 "view_name": self.view_name,
#             },
#         )
#
#     @staticmethod
#     def create_run(request, data, pipeline, pipeline_form):
#         request.data = data
#         request.data["pipeline_id"] = str(pipeline.id)
#         request.META[str(settings.API_KEY_CUSTOM_HEADER)] = str(
#             pipeline_form.secret_key
#         )
#         resp = PipelineRunCreateView().post(request)
#         pipeline_run = get_object_or_404(PipelineRun, run_id=resp.data.get("run_id"))
#         pipeline_run.form = pipeline_form
#         pipeline_run.save()
#
#     def post(self, request, *args, **kwargs):
#         link_id = kwargs.pop("link_id")
#         pipeline_form = get_object_or_404(PipelineForm, link_id=link_id)
#         self.check_has_permission(request, pipeline_form)
#         pipeline = pipeline_form.pipeline
#         schema = pipeline.pipeline_schema
#         csv_file = request.FILES.get("file")
#         if not csv_file or not csv_file.name.endswith(".csv"):
#             msg = _(
#                 'The file you just uploaded named "%(val)s" is not a CSV. Make sure your file is a valid ".csv"'
#             ) % {"val": csv_file.name if csv_file else _("empty")}
#             return self.error_response(msg, request)
#         csv_file.seek(0)
#         rows = csv.DictReader(io.StringIO(csv_file.read().decode("utf-8")))
#         equivalences = {}
#         for k, v in form_equivalences["labels"].items():
#             if k not in equivalences:
#                 equivalences[k] = k
#             if v[0] not in equivalences:
#                 equivalences[str(v[0])] = k
#         form_keys = sorted([x for x in schema["properties"].keys()])
#         final_payload = []
#         idx = 1
#         for row in rows:
#             try:
#                 final_payload.append(
#                     self.validate_row(idx, row, equivalences, schema, form_keys)
#                 )
#             except ValueError as e:
#                 return self.error_response(str(e), request)
#             idx += 1
#         if not final_payload:
#             msg = _('The file you just uploaded named "%(val)s" is empty') % {
#                 "val": csv_file.name
#             }
#             return self.error_response(msg, request)
#         created_num = 0
#         for run in final_payload:
#             self.create_run(request, run, pipeline, pipeline_form)
#             created_num += 1
#         return render(
#             request,
#             PipelineFormDoneView.template_name,
#             {
#                 "view_name": self.view_name,
#                 "link_id": link_id,
#                 "forms_created": created_num,
#             },
#         )
#
#
# class PipelineFormInviteUsersView(LoginRequiredMixin, TemplateView):
#     login_url = "/login/"
#     redirect_field_name = "redirect_to"
#     view_name = "pipeline_form_invite_users"
#     template_name = "pipeline/form_invite_users.html"
#     form_class = AccountUserForm
#
#     def get(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         pipeline_form = get_object_or_404(
#             PipelineForm, link_id=link_id, pipeline__account__admin=request.user
#         )
#         paginator = Paginator(
#             pipeline_form.invited_users.all().order_by("-date_joined"), 50
#         )  # Show 50 runs per page
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         form = self.form_class()
#         return render(
#             request,
#             self.template_name,
#             {
#                 "form": form,
#                 "p_form": pipeline_form,
#                 "page_obj": page_obj,
#                 "link_id": link_id,
#             },
#         )
#
#     def post(self, request, *args, **kwargs):
#         link_id = kwargs["link_id"]
#         pipeline_form = get_object_or_404(
#             PipelineForm, link_id=link_id, pipeline__account__admin=request.user
#         )
#         form = self.form_class(data=request.POST)
#         if form.is_valid():
#             user = get_user_model().objects.create(email=form.cleaned_data["email"])
#             user.set_password(form.cleaned_data["password"])
#             user.save()
#             pipeline_form.invited_users.add(user)
#             pipeline_form.save()
#         paginator = Paginator(
#             pipeline_form.invited_users.all().order_by("-date_joined"), 50
#         )  # Show 50 runs per page
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(
#             request,
#             self.template_name,
#             {
#                 "form": form,
#                 "p_form": pipeline_form,
#                 "page_obj": page_obj,
#                 "link_id": link_id,
#             },
#         )
#
#
from utils.csv import stream_csv_list_of_dicts_view
from website.models import Rule, Coin


class ExampleTemplateCoinsView(LoginRequiredMixin, TemplateView):
    login_url = "/admin/"
    redirect_field_name = "redirect_to"
    view_name = "example_template_coins_view"

    def get(self, request, *args, **kwargs):
        headers = ['coin', 'json_rule']
        example = {}
        for x in headers:
            example[x] = _("<PASTE YOUR DATA HERE>")
        rows = [example]
        xls_name = "Coin Rules Template.csv"
        return stream_csv_list_of_dicts_view(rows, xls_name, headers=headers)


class UploadCoinsRulesView(LoginRequiredMixin, TemplateView):
    login_url = "/admin/"
    redirect_field_name = "redirect_to"
    view_name = "run_batch_upload_view"
    template_name = "pages/index.html"

    def get(self, request, *args, **kwargs):
        rules = Rule.objects.filter(owner=self.request.user)
        return render(
            request,
            self.template_name,
            {
                "view_name": self.view_name,
                "rules": rules
            },
        )

    def error_response(self, msg, request):
        return render(
            request,
            self.template_name,
            {
                "errors": msg,
                "view_name": self.view_name,
            },
        )

    def create_rule(self, logic, coin):
        coin = Coin.objects.get(name=coin)
        return Rule.objects.create(owner=self.request.user, logic=logic, coin=coin)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get("file")
        if not csv_file or not csv_file.name.endswith(".csv"):
            msg = _(
                'The file you just uploaded named "%(val)s" is not a CSV. Make sure your file is a valid ".csv"'
            ) % {"val": csv_file.name if csv_file else _("empty")}
            return self.error_response(msg, request)
        csv_file.seek(0)
        rows = csv.DictReader(io.StringIO(csv_file.read().decode("utf-8")))
        if not rows:
            msg = _('The file you just uploaded named "%(val)s" is empty') % {
                "val": csv_file.name
            }
            return self.error_response(msg, request)
        rules = []
        idx = 1
        for row in rows:
            try:
                rules.append(self.create_rule(row['json_rule'], row['coin']))
            except Exception as e:
                msg = _('The the row "%(val)s" is invalid: "%(err)s" - "%(row)s"') % {
                    "val": idx, "err": str(e), "row": 'Coin: {} - Logic: {}'.format(row['coin'], row['json_rule'])
                }
                return self.error_response(msg, request)
            idx += 1
        return render(
            request,
            self.template_name,
            {
                "view_name": self.view_name,
                "rules": rules
            },
        )