from climmob.products.climmob_products import (
    createProductDirectory,
    registerProductInstance,
)
from .celerytasks import createReports


def create_analysis(locale, user, project, data, info, infosheet, request, pathScript):
    # We create the plugin directory if it does not exists and return it
    # The path user.repository in development.ini/user/project/products/product and
    # user.repository in development.ini/user/project/products/product/outputs
    path = createProductDirectory(request, user, project, "reports")
    if infosheet == "TRUE":
        pathInfosheets = createProductDirectory(request, user, project, "infosheets")
    else:
        pathInfosheets = ""
    # We call the Celery task that will generate the output packages.pdf
    task = createReports.apply_async(
        (locale, path, pathInfosheets, user, project, data, info, infosheet, pathScript),
        queue="ClimMob",
    )
    # We register the instance of the output with the task ID of celery
    # This will go to the products table that then you can monitor and use
    # in the nice product interface
    # u.registerProductInstance(user, project, 'cards', 'cards.pdf', task.id, request)
    registerProductInstance(
        user,
        project,
        "reports",
        "Report_" + project + ".docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "reports",
        task.id,
        request,
    )

    if infosheet == "TRUE":
        registerProductInstance(
            user,
            project,
            "infosheets",
            "Infosheets_" + project + ".docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "infosheets",
            task.id,
            request,
            newTask=False
        )
