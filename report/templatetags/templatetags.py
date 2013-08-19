from django import template

register = template.Library()

@register.filter
def hash(h, key):
    try:
        return h[key]
    except KeyError:
        return ''

@register.filter
def emails_submitted(h):
    sum = 0
    for k in dict(h):
        if int(k) != 55555 and int(k) < 600:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def credits_used(h):
    sum = 0
    for k in dict(h):
        if int(k) == 5:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))

    return emails_submitted(h) - sum

@register.filter
def valid_email(h):
    sum = 0
    for k in dict(h):
        if int(k) >= 5 and int(k) <= 50:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def valid_email_percent(h):
    return float(valid_email(h) * 100.0 / emails_submitted(h))

@register.filter
def syntax_error_email(h):
    sum = 0
    for k in dict(h):
        if int(k) >= 100 and int(k) < 300:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def syntax_error_email_percent(h):
    return float(syntax_error_email(h) * 100.0 / emails_submitted(h))

@register.filter
def suppressed_email(h):
    sum = 0
    for k in dict(h):
        if int(k) >= 300 and int(k) < 400:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def suppressed_email_percent(h):
    return float(suppressed_email(h) * 100.0 / emails_submitted(h))

@register.filter
def invalid_domain_email(h):
    sum = 0
    for k in dict(h):
        if int(k) >= 400 and int(k) < 500:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def invalid_domain_email_percent(h):
    return float(invalid_domain_email(h) * 100.0 / emails_submitted(h))

@register.filter
def invalid_username_email(h):
    sum = 0
    for k in dict(h):
        if int(k) >= 500 and int(k) < 600:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def invalid_username_email_percent(h):
    return float(invalid_username_email(h) * 100.0 / emails_submitted(h))

@register.filter
def total_invalid_email(h):
    sum = 0
    for k in dict(h):
        if int(k) >= 100 and int(k) < 600:
            if hash(dict(h),int(k)) != '':
                sum += int(hash(dict(h),int(k)))
    return sum

@register.filter
def total_invalid_email_percent(h):
    return float(total_invalid_email(h) * 100.0 / emails_submitted(h))

@register.filter
def submitted_percent(h, key):
    if hash(dict(h), key) == '':
        return 0;
    return int(dict(h)[key]) * 100.0 / emails_submitted(h)

@register.filter
def invalid_percent(h, key):
    if hash(dict(h), key) == '':
        return 0;
    return int(dict(h)[key]) * 100.0 / total_invalid_email(h)

@register.filter
def corrected_email(h):
    if 55555 in dict(h):
        return int(dict(h)[55555])
    return 0

@register.filter
def corrected_email_percent(h):
    if 55555 in dict(h):
        return int(dict(h)[55555]) * 100.0 / total_invalid_email(h)
    return 0