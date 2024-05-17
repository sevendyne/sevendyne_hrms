from candidate.models import Candidate
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
    if user.groups.filter(name='hrms_clients').exists():
        pass
    else:
        pass
    return user.groups.filter(name='hrms_clients').exists() 


def has_employee_dashboard_permission(user):
    return user.groups.filter(name='employee_group').exists()


def has_admin_dashboard_permission(user):
    return user.groups.filter(name='sevendyne_admin').exists()


def get_current_company(request):
    company = None
    if request.user.is_authenticated:
        if "current_company" in request.session:
            pk =  request.session['current_company']
            if Company.objects.filter(pk=pk).exists():
                company = Company.objects.get(pk=pk)
        elif CompanyAccess.objects.filter(user=request.user).exists():
            company = CompanyAccess.objects.get(user=request.user).company  
    return company


def company_access(request):
    companies = []
    if request.user.is_authenticated:
        company_access = CompanyAccess.objects.filter(user=request.user,is_accepted=True)
        for access in company_access:
            if not access.company in companies:
                companies.append(access.company)        
    return companies
        
def get_candidate_id(request):
    candidate_id = "SVD1001" # user defined number
    if Candidate.objects.filter(is_deleted=False).exists():
        candidate_id = Candidate.objects.filter(is_deleted=False).latest('id').candidateid
    
    if candidate_id:
        rev_admn_no =  candidate_id[::-1]  
        length = len(rev_admn_no) 
        rev_numbers = "" 
        for i in range(length):
            if not rev_admn_no[i].isnumeric():
                break;
            else:
                rev_numbers += rev_admn_no[i]
        numbers = rev_numbers[::-1]
        
        int_number = int(numbers)
        length_number = len(numbers)
        
        code = rev_admn_no[length_number:]
        if numbers[:1]:
            a = length_number - len(str(int_number))
            b = numbers[:a]
            len0 = len(b)
        last_admn_code = code[::-1]
        next_no = int(int_number) + 1
        if len0 :
            candidate_id = str(last_admn_code) + str(b)+ str(next_no)
        else:
            candidate_id = str(last_admn_code) + str(next_no)    
    return candidate_id 