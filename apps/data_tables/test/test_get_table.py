from django.test import TestCase, Client, RequestFactory
import strawberry.django
from django.contrib.auth import get_user_model
from apps.data_tables.models import DataTable, DataRow, DataColumn, DataCell, DataContent
from apps.data_tables.models import Classification, AccessAttribute
from strawberry import Schema
from apps.data_tables.schema import schema
from django.core.management import call_command

User = get_user_model()

class ContextWrapper:
    def __init__(self,request):
        self.request = request

class DataTableTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Loading test data...")
        call_command('loaddata', 'apps/data_tables/fixtures/test_get_table_sample_data.json', verbosity=0)
        cls.factory = RequestFactory()
        cls.query = """
            query{
                getTable(tableId: %d) {
                    id
                    name
                    accessAttributes {
                        id
                        name
                    }
                    classification {
                        level
                        name
                    }
                    columns {
                        accessAttributes {
                            id
                            name
                        }
                        classification {
                            level
                            name
                        }
                        id
                        name
                    }
                    rows {
                        id
                        accessAttributes {
                            id
                            name
                        }
                        classification {
                            level
                            name
                        }
                        cells {
                            accessAttributes {
                                id
                                name
                            }
                            classification {
                                level
                                name
                            }
                            data{
                                textData
                            }
                        }
                    }
                }
            }
        """ % 1

    def test_validate_classifications(self):
        """Validate that only the correct classifications are loaded nothing missing or extra"""
        classifications = Classification.objects.all()
        assert len(classifications) == 4
        unclassified = Classification.objects.get(name="UNCLASSIFIED")
        confidential = Classification.objects.get(name="CONFIDENTIAL")
        secret = Classification.objects.get(name="SECRET")
        top_secret = Classification.objects.get(name="TOP SECRET")
        assert unclassified in classifications
        assert confidential in classifications
        assert secret in classifications
        assert top_secret in classifications
        assert unclassified.id == 1
        assert confidential.id == 2
        assert secret.id == 3
        assert top_secret.id == 4

    def test_query_user_table_classification(self):
        """Validate that no test user gets access to anything above their clearance given varying table classifications"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_table_classification = test_table.classification
        users = User.objects.all()
        for classification in Classification.objects.all():
            test_table.classification = classification
            test_table.save()
            for user in users:
                request.user = user
                context = ContextWrapper(request)
                try:
                    result = schema.execute_sync(self.query, context_value=context)
                except Exception as e:
                    print(e)
                if not result.errors and result.data['getTable']:
                    table = result.data['getTable']
                    rows = table['rows']
                    columns = table['columns']

                    assert int(table['classification']['level']) <= user.clearance.level
                    for column in columns:
                        assert int(column['classification']['level']) <= user.clearance.level

                    for row in rows:
                        assert int(row['classification']['level']) <= user.clearance.level
                        for cell in row['cells']:
                            assert int(cell['classification']['level']) <= user.clearance.level
                else:
                    assert result.data['getTable'] == None

        test_table.classification = test_table_classification
        test_table.save()

    def test_query_user_row_classification(self):
        """Validate that no test user gets access to anything above their clearance given varying row classifications"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_rows = test_table.rows.all()
        users = User.objects.all()
        for classification in Classification.objects.all():
            for row in test_rows:
                test_row = row
                row.classification = classification
                row.save()
                for user in users:
                    request.user = user
                    context = ContextWrapper(request)
                    try:
                        result = schema.execute_sync(self.query, context_value=context)
                    except Exception as e:
                        print(e)
                    if not result.errors and result.data['getTable']:
                        table = result.data['getTable']
                        rows = table['rows']
                        columns = table['columns']

                        assert int(table['classification']['level']) <= user.clearance.level
                        for column in columns:
                            assert int(column['classification']['level']) <= user.clearance.level

                        for row in rows:
                            assert int(row['classification']['level']) <= user.clearance.level
                            for cell in row['cells']:
                                assert int(cell['classification']['level']) <= user.clearance.level
                    else:
                        assert result.data['getTable'] == None
                row = test_row
                row.save()
        test_table.rows.set(test_rows)
        test_table.save()
    def test_query_user_column_classification(self):
        """Validate that no test user gets access to anything above their clearance given varying column classifications"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_columns = test_table.columns.all()
        users = User.objects.all()
        for classification in Classification.objects.all():
            for column in test_columns:
                test_column = column
                column.classification = classification
                column.save()
                for user in users:
                    request.user = user
                    context = ContextWrapper(request)
                    try:
                        result = schema.execute_sync(self.query, context_value=context)
                    except Exception as e:
                        print(e)
                    if not result.errors and result.data['getTable']:
                        table = result.data['getTable']
                        rows = table['rows']
                        columns = table['columns']

                        assert int(table['classification']['level']) <= user.clearance.level
                        for column in columns:
                            assert int(column['classification']['level']) <= user.clearance.level

                        for row in rows:
                            assert int(row['classification']['level']) <= user.clearance.level
                            for cell in row['cells']:
                                assert int(cell['classification']['level']) <= user.clearance.level
                    else:
                        assert result.data['getTable'] == None
                column = test_column
                column.save()
        test_table.columns.set(test_columns)
        test_table.save()

    def test_query_user_cells_classification(self):
            """Validate that no test user gets access to anything above their clearance given varying cell classifications"""
            request = self.factory.get('/')

            test_table = DataTable.objects.get(name="Test Table")
            test_rows = test_table.rows.all()
            test_cells = []
            for row in test_rows:
                for cell in row.cells.all():
                    test_cells.append(cell)
            
            users = User.objects.all()
            for classification in Classification.objects.all():
                for cell in test_cells:
                    test_cell = cell
                    cell.classification = classification
                    cell.save()
                    for user in users:
                        request.user = user
                        context = ContextWrapper(request)
                        try:
                            result = schema.execute_sync(self.query, context_value=context)
                        except Exception as e:
                            print(e)
                        if not result.errors and result.data['getTable']:
                            table = result.data['getTable']
                            rows = table['rows']
                            columns = table['columns']

                            assert int(table['classification']['level']) <= user.clearance.level
                            for column in columns:
                                assert int(column['classification']['level']) <= user.clearance.level

                            for row in rows:
                                assert int(row['classification']['level']) <= user.clearance.level
                                for cell in row['cells']:
                                    assert int(cell['classification']['level']) <= user.clearance.level
                        else:
                            assert result.data['getTable'] == None
                    cell = test_cell
                    cell.save()
            for cell in test_cells:
                cell.save()

    def test_query_user_table_access_attributes(self):
        """Validate that no test user gets access to anything given varying table access attributes"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_table_attr = test_table.access_attributes.all()
        users = User.objects.all()
        for attr in AccessAttribute.objects.all():
            test_table.access_attributes.add(attr)
            test_table.save()
            for user in users:
                request.user = user
                context = ContextWrapper(request)
                try:
                    result = schema.execute_sync(self.query, context_value=context)
                except Exception as e:
                    print(e)
                if not result.errors and result.data['getTable']:
                    table = result.data['getTable']
                    rows = table['rows']
                    columns = table['columns']

                    for attr in table['accessAttributes']:
                        assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                    for column in columns:
                        for attr in column['accessAttributes']:
                            assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                    for row in rows:
                        for attr in row['accessAttributes']:
                            assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for cell in row['cells']:
                            for attr in cell['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                else:
                    assert result.data['getTable'] == None

        test_table.access_attributes.set(test_table_attr)
        test_table.save()

    def test_query_user_column_access_attributes(self):
        """Validate that no test user gets access to anything given varying column access attributes"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_columns = test_table.columns.all()
        users = User.objects.all()
        for attr in AccessAttribute.objects.all().values():
            attr_id = attr['id']
            for column in test_columns:
                column.access_attributes.add(AccessAttribute.objects.get(id=attr_id))
                column.save()
                for user in users:
                    request.user = user
                    context = ContextWrapper(request)
                    try:
                        result = schema.execute_sync(self.query, context_value=context)
                    except Exception as e:
                        print(e)
                    if not result.errors and result.data['getTable']:
                        table = result.data['getTable']
                        rows = table['rows']
                        columns = table['columns']

                        for attr in table['accessAttributes']:
                            assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for column in columns:
                            for attr in column['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for row in rows:
                            for attr in row['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                            for cell in row['cells']:
                                for attr in cell['accessAttributes']:
                                    assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                    else:
                        assert result.data['getTable'] == None
        for column in test_columns:
            column.access_attributes.set([])
            column.save()

    def test_query_user_row_access_attributes(self):
        """Validate that no test user gets access to anything given varying row access attributes"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_rows = test_table.rows.all()
        users = User.objects.all()
        for attr in AccessAttribute.objects.all().values():
            attr_id = attr['id']
            for row in test_rows:
                row.access_attributes.add(AccessAttribute.objects.get(id=attr_id))
                row.save()
                for user in users:
                    request.user = user
                    context = ContextWrapper(request)
                    try:
                        result = schema.execute_sync(self.query, context_value=context)
                    except Exception as e:
                        print(e)
                    if not result.errors and result.data['getTable']:
                        table = result.data['getTable']
                        rows = table['rows']
                        columns = table['columns']

                        for attr in table['accessAttributes']:
                            assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for column in columns:
                            for attr in column['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for row in rows:
                            for attr in row['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                            for cell in row['cells']:
                                for attr in cell['accessAttributes']:
                                    assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                    else:
                        assert result.data['getTable'] == None
        for row in test_rows:
            row.access_attributes.set([])
            row.save()

    def test_query_user_cell_access_attributes(self):
        """Validate that no test user gets access to anything given varying cell access attributes"""
        request = self.factory.get('/')

        test_table = DataTable.objects.get(name="Test Table")
        test_rows = test_table.rows.all()
        test_cells = []
        for row in test_rows:
            for cell in row.cells.all():
                test_cells.append(cell)
        users = User.objects.all()
        for attr in AccessAttribute.objects.all().values():
            attr_id = attr['id']
            for cell in test_cells:
                cell.access_attributes.add(AccessAttribute.objects.get(id=attr_id))
                cell.save()
                for user in users:
                    request.user = user
                    context = ContextWrapper(request)
                    try:
                        result = schema.execute_sync(self.query, context_value=context)
                    except Exception as e:
                        print(e)
                    if not result.errors and result.data['getTable']:
                        table = result.data['getTable']
                        rows = table['rows']
                        columns = table['columns']

                        for attr in table['accessAttributes']:
                            assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for column in columns:
                            for attr in column['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                        for row in rows:
                            for attr in row['accessAttributes']:
                                assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                            for cell in row['cells']:
                                for attr in cell['accessAttributes']:
                                    assert int(attr['id']) in [a.id for a in user.access_attributes.all()]
                    else:
                        assert result.data['getTable'] == None
        for cell in test_cells:
            cell.access_attributes.set([])
            cell.save()