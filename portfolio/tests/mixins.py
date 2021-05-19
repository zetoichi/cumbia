from django.core.exceptions import ImproperlyConfigured

class GeneralCBVMixin:
    url = None
    view_class = None
    expected_template = None

    error_msg = """You need to setup url, view_class
        and expected_template to inherit from GeneralCBVTestCase"""

    def test_url_resolves(self):
        print('executing test_url_resolves')
        if self.url is not None and self.view_class is not None:
            response = self.client.get(self.url)
            self.assertEqual(
                response.resolver_match.func.__name__,
                self.view_class.as_view().__name__
            )
        else:
            raise ImproperlyConfigured(self.error_msg)

    def test_uses_expected_template(self):
        print('executing test_uses_expected_template')
        if self.url is not None and self.expected_template is not None:
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.expected_template)
        else:
            raise ImproperlyConfigured(self.error_msg)
