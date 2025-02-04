from climmob.views.classes import privateView
from climmob.processes import getActiveProject, getJSONResult


class test_view(privateView):
    def processView(self):
        activeProjectData = getActiveProject(self.user.login, self.request)
        return getJSONResult(
            self.user.login, activeProjectData["project_cod"], self.request
        )
