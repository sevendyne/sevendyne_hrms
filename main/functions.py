
def get_auto_id(model):
    auto_id = 1
    latest_auto_id = None
    if model.objects.all().exists():
        latest_auto_id =  model.objects.all().latest("date_added")
    if latest_auto_id:
        auto_id = latest_auto_id.auto_id + 1
    return auto_id


def generate_form_errors(args,formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += str(field.errors)  + "|"
        for err in args.non_field_errors():
            message += str(err) + "|"
                
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += str(field.errors) + "|"
            for err in form.non_field_errors():
                message += str(err) + "|"
    return message[:-1]


def has_hrms_permission(user):
    print("checking has_hrms_permission")
    if user.groups.filter(name='hrms_clients').exists():
        print("user exists in hrms clients group")
    else:
        print("user not exist in hrms client group")
    return user.groups.filter(name='hrms_clients').exists() 

def has_admin_dashboard_permission(user):
    print("checking admin permission")
    return user.groups.filter(name='sevendyne_admin').exists()

