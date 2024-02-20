from django.template import Library

register = Library()


@register.filter
def get_attendance(att,date):
    print("att- template tag",att['attendance'])
    if att['attendance'].filter(date__day=date,is_fn=True,is_an=True).exists():
        return True
    elif att['attendance'].filter(date__day=date,is_fn=False,is_an=True).exists():
        return "AnHalf"
    elif att['attendance'].filter(date__day=date,is_fn=True,is_an=False).exists():
        return "FnHalf"
    elif att['attendance'].filter(date__day=date,is_fn=False,is_an=False).exists():
        return False
    elif att['attendance'].filter(date__day=date,is_attended=True).exists():
        return True
    elif att['attendance'].filter(date__day=date,is_attended=False).exists():
        return False
    else:
        return "-"

