# # Create your api_tests here.
# import csv
# import datetime
# from io import StringIO
#
# from api.models import Account, Service, ServiceContract, Pipeline, PipelineForm
# from django.contrib.auth import get_user_model
# from django.forms import TextInput, BooleanField, DateInput, Select
# from django.urls import reverse
# from rest_framework.test import APITestCase
#
# from website.forms import PipelineRunForm
# from website.views import BatchFormFillView
#
#
# class PipelineFormTests(APITestCase):
#     def setUp(self):
#         user = get_user_model().objects.create(email="test3@email.com")
#         user.set_password("testpass")
#         user.save()
#         account = Account.objects.create(
#             name="test",
#             business_registration_id="1234",
#             admin=user,
#             accepted_terms=True,
#             validated=True,
#             active=True,
#             time_of_validation=datetime.date(2010, 1, 1),
#             time_of_accepted_terms=datetime.date(2010, 1, 1))
#         services = [('registraduria-co', {
#             "type": "object",
#             "properties": {
#                 "date_expedition": {
#                     "type": "string",
#                     "format": "date"
#                 },
#                 "document_number": {
#                     "type": "string",
#                     "maxLength": 15,
#                     "minLength": 5
#                 }
#             },
#             "required": ["date_expedition", "document_number"]
#         }),
#                     ('icij', {
#                         "type":
#                         "object",
#                         "anyOf": [{
#                             "required": ["name", "last_name"]
#                         }, {
#                             "required": ["document_number"]
#                         }],
#                         "properties": {
#                             "name": {
#                                 "type": "string",
#                                 "maxLength": 128,
#                                 "minLength": 2
#                             },
#                             "last_name": {
#                                 "type": "string",
#                                 "maxLength": 128,
#                                 "minLength": 3
#                             },
#                             "document_number": {
#                                 "type": "string",
#                                 "maxLength": 15,
#                                 "minLength": 5
#                             }
#                         }
#                     }),
#                     ('policia-co', {
#                         "type": "object",
#                         "properties": {
#                             "document_type": {
#                                 "enum": [
#                                     "numero_comparendo_o_expediente", "cedula",
#                                     "cedula_extranjeria", "tarjeta_identidad",
#                                     "pasaporte"
#                                 ],
#                                 "type":
#                                 "string"
#                             },
#                             "document_number": {
#                                 "type": "string",
#                                 "minLength": 5,
#                                 "maxLength": 15
#                             }
#                         },
#                         "required": ["document_type", "document_number"]
#                     }),
#                     ('inpec-co', {
#                         "type":
#                         "object",
#                         "properties": {
#                             "last_name": {
#                                 "type": "string",
#                                 "maxLength": 32,
#                                 "minLength": 3
#                             },
#                             "document_number": {
#                                 "type": "string",
#                                 "maxLength": 15,
#                                 "minLength": 5
#                             },
#                             "legal_adult": {
#                                 "type": "boolean"
#                             }
#                         },
#                         "required":
#                         ["last_name", "document_number", "legal_adult"]
#                     })]
#         created_services = []
#         for n, s in services:
#             new = Service.objects.create(name=n,
#                                          module_name="test",
#                                          file_name="test",
#                                          function_name="test",
#                                          input_schema=s)
#             self.n = new
#             created_services.append(new)
#             ServiceContract.objects.create(account=account, service=new)
#         pipeline = Pipeline.objects.create(account=account)
#         pipeline.services.set(created_services)
#         pipeline.save()
#         form = PipelineForm.objects.create(name='test-form',
#                                            pipeline=pipeline,
#                                            visibility='private')
#         self.form = form
#         self.user = user
#         self.account = account
#         self.pipeline = pipeline
#         self.form = form
#
#     def test_check_pipeline_schema(self):
#         self.assertEquals(
#             self.pipeline.pipeline_schema, {
#                 "type": "object",
#                 "properties": {
#                     "name": {
#                         "type": "string",
#                         "maxLength": 128,
#                         "minLength": 2
#                     },
#                     "last_name": {
#                         "type": "string",
#                         "maxLength": 32,
#                         "minLength": 3
#                     },
#                     "document_number": {
#                         "type": "string",
#                         "maxLength": 15,
#                         "minLength": 5
#                     },
#                     "document_type": {
#                         'enum': [
#                             'numero_comparendo_o_expediente', 'cedula',
#                             'cedula_extranjeria', 'tarjeta_identidad',
#                             'pasaporte'
#                         ],
#                         'type':
#                         'string'
#                     },
#                     "date_expedition": {
#                         "type": "string",
#                         "format": "date"
#                     },
#                     "legal_adult": {
#                         "type": "boolean"
#                     }
#                 }
#             })
#
#     def test_form_not_valid_data_empty(self):
#         form = PipelineRunForm(data={}, schema=self.pipeline.pipeline_schema)
#         self.assertEquals(form.is_valid(), False)
#
#     def test_form_not_valid_data_missing_fields(self):
#         form = PipelineRunForm(data={
#             "name": "name test",
#             "last_name": "test last name",
#             "document_number": "12345"
#         },
#                                schema=self.pipeline.pipeline_schema)
#         self.assertEquals(form.is_valid(), False)
#
#     def test_form_not_valid_data_wrong_fields(self):
#         form = PipelineRunForm(data={
#             "name": "name test",
#             "last_name": "test last name",
#             "document_number": "12",
#             "document_type": "12",
#             "date_expedition": "",
#             "legal_adult": True
#         },
#                                schema=self.pipeline.pipeline_schema)
#         self.assertEquals(form.is_valid(), False)
#
#     def test_form_not_valid_data_wrong_field_date(self):
#         form = PipelineRunForm(data={
#             "name": "name test",
#             "last_name": "test last name",
#             "document_number": "1234567",
#             "document_type": "cedula",
#             "date_expedition": "20-JAN-2020",
#             "legal_adult": True
#         },
#                                schema=self.pipeline.pipeline_schema)
#         self.assertEquals(form.is_valid(), False)
#
#     def test_form_valid_input(self):
#         form = PipelineRunForm(data={
#             "name": "name test",
#             "last_name": "test last name",
#             "document_number": "1234567",
#             "document_type": "cedula",
#             "date_expedition": "2019-12-01",
#             "legal_adult": True
#         },
#                                schema=self.pipeline.pipeline_schema)
#         self.assertEquals(form.is_valid(), True)
#
#     def test_form_valid_widgets(self):
#         form = PipelineRunForm(data={
#             "name": "name test",
#             "last_name": "test last name",
#             "document_number": "1234567",
#             "document_type": "cedula",
#             "date_expedition": "2019-12-01",
#             "legal_adult": True
#         },
#                                schema=self.pipeline.pipeline_schema)
#
#         match = sorted([
#             "name", "last_name", "document_number", "document_type",
#             "date_expedition", "legal_adult"
#         ]) == sorted([field.name for field in form])
#         self.assertTrue(match)
#         field = form['date_expedition']
#         self.assertTrue(isinstance(field.field.widget, DateInput))
#         # self.assertTrue((str(field.field.widget.input_type) == 'date'))
#         field = form['document_type']
#         self.assertTrue(isinstance(field.field.widget, Select))
#         self.assertEqual(
#             field.field.choices,
#             list(
#                 PipelineRunForm.create_choices([
#                     "numero_comparendo_o_expediente", "cedula",
#                     "cedula_extranjeria", "tarjeta_identidad", "pasaporte"
#                 ])))
#         field = form['legal_adult']
#         self.assertTrue(isinstance(field.field, BooleanField))
#         self.assertTrue(field.value())
#         field = form['name']
#         self.assertTrue(isinstance(field.field.widget, TextInput))
#         self.assertEqual(field.field.widget.attrs['maxlength'], '128')
#         self.assertEqual(field.field.widget.attrs['minlength'], '2')
#         field = form['last_name']
#         self.assertTrue(isinstance(field.field.widget, TextInput))
#         self.assertEqual(field.field.widget.attrs['maxlength'], '32')
#         self.assertEqual(field.field.widget.attrs['minlength'], '3')
#         field = form['document_number']
#         self.assertTrue(isinstance(field.field.widget, TextInput))
#         self.assertEqual(field.field.widget.attrs['maxlength'], '15')
#         self.assertEqual(field.field.widget.attrs['minlength'], '5')
#         self.assertEquals(form.is_valid(), True)
#
#     @staticmethod
#     def create_csv(file_name, headers, rows):
#         """
#         Generate a test csv, returning the filename that it was saved as.
#         """
#         data = StringIO()
#         data.name = file_name
#         writer = csv.writer(data)
#         writer.writerows(headers)
#         writer.writerows(rows)
#         data.seek(0)
#         return data
#
#     def test_upload_form_batch_wrong_extension(self):
#         buffer_file = self.create_csv('test', [['a', 'b']], [[1, 2], [3, 4]])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The file you just uploaded named "test" is not a CSV. Make sure your file '
#             'is a valid ".csv"')
#
#     def test_upload_form_batch_empty(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[]], [[]])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The file you just uploaded named "test.csv" is empty')
#
#     def test_upload_form_batch_all_data_is_empty(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [['', '']],
#                                       [['', ''], ['', '']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(body['errors'], 'The row 1 of your file is not valid')
#
#     def test_upload_form_batch_wrong_columns(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [['a', 'b']],
#                                       [['1', '2'], ['3', '4']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The column "a" does not match with the list of fields of this form. The possible values of the columns '
#             'are "Fecha de expedicion de tu documento de identidad", "Document Number", "Document Type", '
#             '"Primer apellido", "Legal Adutl/Minor", "Nombres" or "date_expedition", "document_number", '
#             '"document_type", "last_name", "legal_adult", "name". Please download the template for this form and make '
#             'sure all the columns you are uploading match with the ones in the file '
#         )
#
#     def test_upload_form_batch_type_boolean_fail(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[
#             "legal_adult",
#         ]], [['1']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "1" for the column "legal_adult" for the row 1 is not valid. The '
#             'value "1" must be one of the following options "true", "verdadero", '
#             '"verdad", "verdade", "verdadeiro", "yes", "si", "sim", "false", "falso", '
#             '"no", "não"')
#
#     def test_upload_form_batch_type_date_fail(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv',
#                                       [["legal_adult", "date_expedition"]],
#                                       [['verdad', '1']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "1" for the column "date_expedition" for the row 1 is not valid. The value "1" is not a valid '
#             'date. The correct format for dates is YYYY-MM-DD')
#
#     def test_upload_form_batch_type_date_fail_format(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv',
#                                       [["legal_adult", "date_expedition"]],
#                                       [['verdad', '01/07/2100']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "01/07/2100" for the column "date_expedition" for the row 1 is not valid. The value '
#             '"01/07/2100" is not a valid date. The correct format for dates is YYYY-MM-DD'
#         )
#
#     def test_upload_form_batch_type_enum(self):
#         # set up form data
#         buffer_file = self.create_csv(
#             'test.csv', [["legal_adult", "date_expedition", "document_type"]],
#             [['verdad', '2100-07-01', 'One ring to rule them all']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "One ring to rule them all" for the column "document_type" for '
#             'the row 1 is not valid. Change "One ring to rule them all" for one of the '
#             'correct options: "numero_comparendo_o_expediente", "cedula", '
#             '"cedula_extranjeria", "tarjeta_identidad", "pasaporte"')
#
#     def test_upload_form_batch_type_missing_columns(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv',
#                                       [["legal_adult", "date_expedition"]],
#                                       [['verdad', '2100-07-01']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(body['errors'], 'The row 1 of your file is not valid')
#
#     def test_upload_form_batch_empty_spaces(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[
#             "legal_adult", "name", "date_expedition", "document_number",
#             "document_type", "last_name"
#         ]], [['si', 'pedro', '2100-07-01', '43210', 'cedula', '     ']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "     " for the column "last_name" for the row 1 is not valid. The value "" must be longer '
#             'than or equal to 3 characters')
#
#     def test_upload_form_batch_v_not_k(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[
#             "legal_adult", "name", "date_expedition", "document_number",
#             "document_type", "last_name"
#         ]], [['si', 'pedro', '2100-07-01', '43210', 'cedula', 'perez'],
#              ['si', 'pedro', '2100-07-01', '43210', 'cedula', 'perez', '', '']
#              ])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertEqual(
#             body['errors'],
#             'In the row 2 of your file, the value "[\'\', \'\']" is not part of any column'
#         )
#
#     def test_upload_form_batch_missing_min_length(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[
#             "legal_adult", "name", "date_expedition", "document_number",
#             "document_type", "last_name"
#         ]], [['si', 'pedro', '2100-07-01', '4', 'cedula', 'perez'],
#              ['no', 'pedro2', '2100-07-01', '4', 'cedula', 'perez2']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertFalse('forms_created' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "4" for the column "document_number" for the row 1 is not valid. The value "4" must be longer '
#             'than or equal to 5 characters')
#
#     def test_upload_form_batch_missing_max_length(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[
#             "legal_adult", "name", "date_expedition", "document_number",
#             "document_type", "last_name"
#         ]], [['si', 'pedro', '2100-07-01', '43210', 'cedula', 'perez'],
#              [
#                  'no', 'pedro2', '2100-07-01', '43210', 'cedula',
#                  'perez very long long long long value overpassing the '
#                  'max allowed'
#              ]])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertTrue('errors' in body)
#         self.assertFalse('forms_created' in body)
#         self.assertEqual(
#             body['errors'],
#             'The value "perez very long long long long value overpassing the max allowed" for the column "last_name" '
#             'for the row 2 is not valid. The value "perez very long long long long value overpassing the max allowed" '
#             'must be less than or equal to 32 characters')
#
#     def test_upload_form_batch_correct(self):
#         # set up form data
#         buffer_file = self.create_csv('test.csv', [[
#             "legal_adult", "name", "date_expedition", "document_number",
#             "document_type", "last_name"
#         ]], [['si', 'pedro', '2100-07-01', '43210', 'cedula', 'perez'],
#              ['no', 'pedro2', '2100-07-01', '01234', 'cedula', 'perez2']])
#         form_data = {'file': buffer_file}
#
#         url = reverse(BatchFormFillView.view_name,
#                       kwargs={'link_id': self.form.link_id})
#         self.client.login(email=self.user.email, password="testpass")
#         response = self.client.post(url, data=form_data, follow=True)
#         body = response.context[0]
#         self.assertFalse('errors' in body)
#         self.assertTrue('forms_created' in body)
#         self.assertEqual(body['forms_created'], 2)
