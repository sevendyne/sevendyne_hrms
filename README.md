# sevendyne_hrms

1. virtualenv venv
2. source venv/bin/activate (on windows use "venv\Scripts\activate)
3. Add the below lines to venv-lib-python 3.10 -> site-packages -> dal -> widgets.py

   if self.forward:
           attrs.setdefault('data-autocomplete-light-forward',
                            ','.join(self.forward))

Like this, 
    def build_attrs(self, *args, **kwargs):
       """Build HTML attributes for the widget."""
       attrs = super(WidgetMixin, self).build_attrs(*args, **kwargs)


       if self.url is not None:
           attrs['data-autocomplete-light-url'] = self.url


       autocomplete_function = getattr(self, 'autocomplete_function', None)
       if autocomplete_function:
           attrs.setdefault('data-autocomplete-light-function',
                            autocomplete_function)      


       if self.forward:
           attrs.setdefault('data-autocomplete-light-forward',
                            ','.join(self.forward))
       return attrs

4. pip install -r requirements.txt
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py loaddata states countries
8.Create user groups and permissions:

    ```bash
    python manage.py create_groups_and_permissions
    ```

9. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to set up the superuser account. For example:
    
    - Username: admin
    - Email: [leave blank]
    - Password: admin

    For Windows
    
    ```bash
    python manage.py createsuperuser --username yourusername --email youremail@example.com --noinput - Add username and email address
    ```
10. sevendyne admin --- username - admin , password - admin
11. hrms client --- username - hrmsclient1 , password - password@123 , hrmsclient1@example.com 