from django.contrib import messages

def notify(request, level, message):
    if level == "success":
        messages.success(request, message)
    elif level == "info":
        messages.info(request, message)
    elif level == "error":
        messages.error(request, message)
    else:
        messages.warning(request, message)