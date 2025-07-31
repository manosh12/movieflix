def dashboard_callback(request, context):
    context.update({
        "title": "Dashboard",
    })
    return context