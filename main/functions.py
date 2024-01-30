from main.models import Company, CompanyAccess


def get_auto_id(model):
    auto_id = 1
    latest_auto_id = None
    if model.objects.all().exists():
        latest_auto_id =  model.objects.all().latest("date_added")
    if latest_auto_id:
        auto_id = latest_auto_id.auto_id + 1
    return auto_id


def get_a_id(model,request):
    a_id = 1 
    latest_a_id = None
    current_company = get_current_company(request)
    if model.objects.filter(company=current_company,is_deleted=False).exists():
        latest_a_id =  model.objects.filter(company=current_company,is_deleted=False).latest("date_added")
    if latest_a_id:
        a_id = latest_a_id.a_id + 1

    return a_id


# def generate_form_errors(args,formset=False):
#     message = ''
#     if not formset:
#         for field in args:
#             if field.errors:                
#                 message += str(field.errors)  + "|"
#         for err in args.non_field_errors():
#             message += str(err) + "|"
                
#     elif formset:
#         for form in args:
#             for field in form:
#                 if field.errors:
#                     message += str(field.errors) + "|"
#             for err in form.non_field_errors():
#                 message += str(err) + "|"
#     return message[:-1]

def generate_form_errors(args, formset=False):
    message = ''
    errors = {}

    if not formset:
        for field in args:
            if field.errors:
                field_name = field.label if field.label else str(field)
                errors[field_name] = str(field.errors)
                message += f"{field_name}: {str(field.errors)}|"  # Include field label in the message
        for err in args.non_field_errors():
            errors['non_field_errors'] = str(err)
            message += f"non_field_errors: {str(err)}|"

    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    field_name = field.label if field.label else str(field)
                    errors[field_name] = str(field.errors)
                    message += f"{field_name}: {str(field.errors)}|"
            for err in form.non_field_errors():
                errors['non_field_errors'] = str(err)
                message += f"non_field_errors: {str(err)}|"

    return errors, message[:-1]


def has_hrms_permission(user):
    # print("checking has_hrms_permission")
    if user.groups.filter(name='hrms_clients').exists():
        print("user exists in hrms clients group")
    else:
        print("user not exist in hrms client group")
    return user.groups.filter(name='hrms_clients').exists() 

def has_admin_dashboard_permission(user):
    print("checking admin permission")
    return user.groups.filter(name='sevendyne_admin').exists()


def get_current_company(request):
    # print("current company get request")
    company = None
    if request.user.is_authenticated:
        if "current_company" in request.session:
            # print("current company in request.session")
            pk =  request.session['current_company']
            if Company.objects.filter(pk=pk).exists():
                company = Company.objects.get(pk=pk)
                # print("company", company)
        elif CompanyAccess.objects.filter(user=request.user).exists():
            company = CompanyAccess.objects.get(user=request.user).company        
            # print("company in get current company",company)
    return company


def company_access(request):
    companies = []
    if request.user.is_authenticated:
        company_access = CompanyAccess.objects.filter(user=request.user,is_accepted=True)
        for access in company_access:
            if not access.company in companies:
                companies.append(access.company)
        
    return companies
        