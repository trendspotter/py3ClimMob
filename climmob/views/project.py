# -*- coding: utf-8 -*-

from .classes import privateView
from ..processes import (
    projectInDatabase,
    addProject,
    getProjectData,
    modifyProject,
    projectExists,
    deleteProject,
    changeTheStateOfCreateComb,
    getCountryList,
    addToLog,
)
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
import json
import qrcode
import zlib
import base64
from pyramid.response import FileResponse
import uuid
import os
import datetime
import climmob.plugins as p


class newProject_view(privateView):
    def processView(self):

        dataworking = {}
        newproject = False
        error_summary = {}
        dataworking["project_cod"] = ""
        dataworking["project_name"] = ""
        dataworking["project_abstract"] = ""
        dataworking["project_tags"] = ""
        dataworking["project_pi"] = ""
        dataworking["project_piemail"] = ""
        dataworking["project_numobs"] = 0
        dataworking["project_numcom"] = 3
        dataworking["project_regstatus"] = 0
        dataworking["project_localvariety"] = "on"
        dataworking["project_cnty"] = None
        dataworking["project_registration_and_analysis"] = 0

        if self.request.method == "POST":
            if "btn_addNewProject" in self.request.POST:
                dataworking = self.getPostDict()
                dataworking["project_registration_and_analysis"] = int(
                    dataworking["project_registration_and_analysis"]
                )
                continue_creation = True
                for plugin in p.PluginImplementations(p.IProject):
                    (
                        continue_creation,
                        error_message,
                        modified_dataworking,
                    ) = plugin.before_adding_project(
                        self.request, self.user.login, dataworking
                    )
                    if not continue_creation:
                        error_summary["plugin_error"] = error_message
                    else:
                        dataworking = modified_dataworking
                    break  # Only one plugging will be called to extend before_create
                if continue_creation:
                    dataworking, error_summary, added = createProjectFunction(
                        dataworking, error_summary, self
                    )
                    if added:
                        for plugin in p.PluginImplementations(p.IProject):
                            plugin.after_adding_project(
                                self.request, self.user.login, dataworking
                            )
                        self.request.session.flash(
                            self._("The project was created successfully")
                        )
                        self.returnRawViewResult = True
                        return HTTPFound(
                            location=self.request.route_url(
                                "dashboard",
                                _query={"project": dataworking["project_cod"]},
                            )
                        )

        return {
            "activeUser": self.user,
            "indashboard": True,
            "dataworking": dataworking,
            "newproject": newproject,
            "countries": getCountryList(self.request),
            "error_summary": error_summary,
        }


def createProjectFunction(dataworking, error_summary, self):
    added = False
    dataworking["user_name"] = self.user.login
    dataworking["project_regstatus"] = 0
    dataworking["project_lat"] = ""
    dataworking["project_lon"] = ""

    dataworking["project_localvariety"] = 1

    if int(dataworking["project_numobs"]) > 0:
        if dataworking["project_cod"] != "":
            exitsproject = projectInDatabase(
                self.user.login, dataworking["project_cod"], self.request
            )
            if not exitsproject:
                added, message = addProject(dataworking, self.request)
                if not added:
                    error_summary = {"dberror": message}
                else:
                    addToLog(
                        self.user.login,
                        "PRF",
                        "Created a new project",
                        datetime.datetime.now(),
                        self.request,
                    )

            else:
                error_summary = {
                    "exitsproject": self._("A project already exists with this code.")
                }
        else:
            error_summary = {"codempty": self._("The project code can't be empty")}
    else:
        error_summary = {
            "observations": self._("The number of observations must be greater than 0.")
        }

    if int(dataworking["project_localvariety"]) == 1:
        dataworking["project_localvariety"] = "on"
    else:
        dataworking["project_localvariety"] = "off"

    return dataworking, error_summary, added


class modifyProject_view(privateView):
    def processView(self):
        projectid = self.request.matchdict["projectid"]
        if not projectExists(self.user.login, projectid, self.request):
            raise HTTPNotFound()

        newproject = False
        error_summary = {}
        data = getProjectData(self.user.login, projectid, self.request)
        if int(data["project_localvariety"]) == 1:
            data["project_localvariety"] = "on"
        else:
            data["project_localvariety"] = "off"

        if self.request.method == "POST":
            if "btn_addNewProject" in self.request.POST:
                # get the field value
                cdata = getProjectData(self.user.login, projectid, self.request)
                data = self.getPostDict()
                data["user_name"] = self.user.login
                data["project_cod"] = projectid
                data["project_regstatus"] = cdata["project_regstatus"]
                if cdata["project_regstatus"] != 0:
                    data["project_numobs"] = cdata["project_numobs"]
                    data["project_numcom"] = cdata["project_numcom"]

                data["project_registration_and_analysis"] = int(
                    data["project_registration_and_analysis"]
                )

                data["project_localvariety"] = 1

                isNecessarygenerateCombinations = False
                if int(data["project_numobs"]) != int(cdata["project_numobs"]):
                    isNecessarygenerateCombinations = True

                if int(data["project_numcom"]) != int(cdata["project_numcom"]):
                    isNecessarygenerateCombinations = True

                if isNecessarygenerateCombinations:
                    changeTheStateOfCreateComb(self.user.login, projectid, self.request)

                continue_modify = True
                for plugin in p.PluginImplementations(p.IProject):
                    (
                        continue_modify,
                        error_message,
                        modified_data,
                    ) = plugin.before_modifying_project(
                        self.request, self.user.login, data
                    )
                    if not continue_modify:
                        error_summary["plugin_error"] = error_message
                    else:
                        data = modified_data
                    break  # Only one plugging will be called to extend before_create
                if continue_modify:
                    modified, message = modifyProject(
                        self.user.login, projectid, data, self.request
                    )
                    if not modified:
                        error_summary = {"dberror": message}
                    else:
                        for plugin in p.PluginImplementations(p.IProject):
                            plugin.after_modifying_project(
                                self.request, self.user.login, data
                            )

                        self.request.session.flash(
                            self._("The project was modified successfully")
                        )
                        self.returnRawViewResult = True
                        return HTTPFound(location=self.request.route_url("dashboard"))

                    if int(data["project_localvariety"]) == 1:
                        data["project_localvariety"] = "on"
                    else:
                        data["project_localvariety"] = "off"
        return {
            "activeUser": self.user,
            "indashboard": True,
            "data": data,
            "newproject": newproject,
            "countries": getCountryList(self.request),
            "error_summary": error_summary,
        }


class deleteProject_view(privateView):
    def processView(self):
        projectid = self.request.matchdict["projectid"]
        if not projectExists(self.user.login, projectid, self.request):
            raise HTTPNotFound()
        redirect = False
        error_summary = {}
        data = getProjectData(self.user.login, projectid, self.request)
        if self.request.method == "POST":
            deleted, message = deleteProject(self.user.login, projectid, self.request)
            if not deleted:
                error_summary = {"dberror": message}
                self.returnRawViewResult = True
                return {"status": 400, "error": message}
            else:
                self.returnRawViewResult = True
                return {"status": 200}
                self.request.session.flash(
                    self._("The project was deleted successfully")
                )

        return {
            "activeUser": self.user,
            "redirect": redirect,
            "data": data,
            "error_summary": error_summary,
        }


class ProjectQRView(privateView):
    def processView(self):
        project_id = self.request.matchdict["projectid"]

        path = os.path.join(
            self.request.registry.settings["user.repository"],
            *[self.user.login, project_id, "tmp"]
        )
        url = self.request.application_url + "/" + self.user.login
        odk_settings = {
            "admin": {"change_server": True, "change_form_metadata": False},
            "general": {
                "change_server": True,
                "navigation": "buttons",
                "server_url": url,
            },
        }
        qr_json = json.dumps(odk_settings).encode()
        zip_json = zlib.compress(qr_json)
        serialization = base64.b64encode(zip_json)
        serialization = serialization.decode()
        serialization = serialization.replace("\n", "")
        img = qrcode.make(serialization)

        unique_id = str(uuid.uuid4())
        temp_path = os.path.join(path, *[unique_id])
        os.makedirs(temp_path)

        qr_file = os.path.join(temp_path, *[project_id + ".png"])
        img.save(qr_file)
        response = FileResponse(qr_file, request=self.request, content_type="image/png")
        response.content_disposition = 'attachment; filename="' + project_id + '.png"'
        self.returnRawViewResult = True
        return response
