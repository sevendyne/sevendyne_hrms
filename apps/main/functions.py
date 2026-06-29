import re
from apps.candidate.models import Candidate
from apps.main.models import Company, CompanyAccess
from django.utils.html import strip_tags


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
                errors[field_name] = strip_tags(str(field.errors))
                message += f"{field_name}: {strip_tags(str(field.errors))}|"  # Strip HTML tags
        for err in args.non_field_errors():
            errors['non_field_errors'] = strip_tags(str(err))
            message += f"non_field_errors: {strip_tags(str(err))}|"
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    field_name = field.label if field.label else str(field)
                    errors[field_name] = strip_tags(str(field.errors))
                    message += f"{field_name}: {strip_tags(str(field.errors))}|"
            for err in form.non_field_errors():
                errors['non_field_errors'] = strip_tags(str(err))
                message += f"non_field_errors: {strip_tags(str(err))}|"
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
        
def get_candidate_id():
    candidate_id = "SVD1001"  # default starting candidate ID

    # Check if there are existing candidates
    if Candidate.objects.filter(is_deleted=False).exists():
        latest_candidate = Candidate.objects.filter(is_deleted=False).latest('id')
        candidate_id = latest_candidate.candidateid

    # Extract the numeric part from the candidate ID    
    numeric_part = re.search(r'\d+', candidate_id)
    
    if numeric_part:
        next_number = int(numeric_part.group()) + 1
        candidate_id = f"SVD{next_number:04d}"  # Maintain the format "SVDXXXX"
    else:
        candidate_id = "SVD1001"  # Default value if no valid candidate ID exists
    
    # Ensure the candidate ID is unique
    while Candidate.objects.filter(candidateid=candidate_id).exists():
        next_number += 1
        candidate_id = f"SVD{next_number:04d}"
    
    return candidate_id
