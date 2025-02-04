from climmob.views.classes import apiView
from climmob.processes import (
    projectInDatabase,
    addProject,
    projectExists,
    deleteProject,
    getUserProjects,
    getProjectData,
    modifyProject,
    changeTheStateOfCreateComb,
    existsCountryByCode,
    getCountryList,
    getTheProjectIdForOwner,
    getAccessTypeForProject,
    theUserBelongsToTheProject,
    add_project_collaborator,
    getUserInfo,
    remove_collaborator,
    get_collaborators_in_project,
    getProjectIsTemplate,
    getProjectAssessments,
    deleteRegistryByProjectId,
    deleteProjectAssessments,
    getProjectTemplates,
)
from climmob.views.project import functionCreateClone
from pyramid.response import Response
import json
import datetime
import re


class readListOfTemplates_view(apiView):
    def processView(self):
        if self.request.method == "GET":

            obligatory = [u"project_type"]

            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):

                dataInParams = True
                for key in dataworking.keys():
                    if dataworking[key] == "":
                        dataInParams = False

                if dataInParams:

                    response = Response(
                        status=200,
                        body=json.dumps(
                            getProjectTemplates(
                                self.request, dataworking["project_type"]
                            )
                        ),
                    )
                    return response

                else:

                    response = Response(
                        status=401, body=self._("Not all parameters have data.")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts GET method."))
            return response


class readListOfCountries_view(apiView):
    def processView(self):

        if self.request.method == "GET":

            response = Response(
                status=200, body=json.dumps(getCountryList(self.request)),
            )
            return response
        else:
            response = Response(status=401, body=self._("Only accepts GET method."))
            return response


class createProject_view(apiView):
    def processView(self):

        if self.request.method == "POST":

            obligatory = [
                u"project_cod",
                u"project_name",
                u"project_abstract",
                u"project_tags",
                u"project_pi",
                u"project_piemail",
                u"project_numobs",
                u"project_cnty",
                u"project_registration_and_analysis",
                u"project_label_a",
                u"project_label_b",
                u"project_label_c",
            ]

            possibles = [
                u"user_owner",
                u"project_cod",
                u"project_name",
                u"project_abstract",
                u"project_tags",
                u"project_pi",
                u"project_piemail",
                u"project_numobs",
                u"project_cnty",
                u"project_registration_and_analysis",
                u"project_clone",
                u"project_label_a",
                u"project_label_b",
                u"project_label_c",
                u"project_template",
            ]

            dataworking = json.loads(self.body)

            permitedKeys = True
            for key in dataworking.keys():
                if key not in possibles:
                    permitedKeys = False

            obligatoryKeys = True

            for key in obligatory:
                if key not in dataworking.keys():
                    obligatoryKeys = False

            if obligatoryKeys:
                if permitedKeys:

                    dataworking["user_name"] = self.user.login
                    dataworking["project_localvariety"] = 1
                    dataworking["project_regstatus"] = 0
                    dataworking["project_numcom"] = 3

                    dataInParams = True
                    for key in dataworking.keys():
                        if dataworking[key] == "":
                            dataInParams = False

                    if dataInParams:

                        if (
                            "project_clone" in dataworking.keys()
                            and "project_template" in dataworking.keys()
                        ):
                            response = Response(
                                status=401,
                                body=self._(
                                    "You cannot create a clone and use a template at the same time."
                                ),
                            )
                            return response

                        if "project_template" in dataworking.keys():
                            existsTemplate = getProjectIsTemplate(
                                self.request, dataworking["project_template"]
                            )
                            if existsTemplate:
                                if str(
                                    dataworking["project_registration_and_analysis"]
                                ) == str(
                                    existsTemplate["project_registration_and_analysis"]
                                ):
                                    dataworking["usingTemplate"] = dataworking[
                                        "project_template"
                                    ]
                                    dataworking["project_template"] = 0
                                else:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "You are trying to use a template that does not correspond to the type of project you are creating."
                                        ),
                                    )
                                    return response
                            else:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "There is no template with this identifier."
                                    ),
                                )
                                return response

                        if "project_clone" in dataworking.keys():
                            existsproject = projectInDatabase(
                                self.user.login,
                                dataworking["project_clone"],
                                self.request,
                            )
                            if not existsproject:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "The project to be cloned does not exist."
                                    ),
                                )
                                return response

                        dataworking["project_lat"] = ""
                        dataworking["project_lon"] = ""
                        if re.search("^[A-Za-z0-9]*$", dataworking["project_cod"]):
                            if dataworking["project_cod"][0].isdigit() == False:
                                exitsproject = projectInDatabase(
                                    self.user.login,
                                    dataworking["project_cod"],
                                    self.request,
                                )
                                if not exitsproject:

                                    try:
                                        dataworking["project_numobs"] = int(
                                            dataworking["project_numobs"]
                                        )
                                    except:
                                        response = Response(
                                            status=401,
                                            body=self._(
                                                "The parameter project_numobs must be a number."
                                            ),
                                        )
                                        return response

                                    if (
                                        dataworking["project_numobs"] > 0
                                        and dataworking["project_numcom"] > 0
                                    ):
                                        if str(
                                            dataworking[
                                                "project_registration_and_analysis"
                                            ]
                                        ) not in ["0", "1",]:
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "The possible values in the parameter 'project_registration_and_analysis' are: ['0':' Registration is done first, followed by one or more data collection moments (with different forms)','1':'Requires registering participants and immediately asking questions to analyze the information']"
                                                ),
                                            )
                                            return response

                                        if str(
                                            dataworking["project_localvariety"]
                                        ) not in ["0", "1",]:
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "The possible values in the parameter 'project_localvariety' are: ['0':'No','1':'Yes']"
                                                ),
                                            )
                                            return response

                                        if not existsCountryByCode(
                                            self.request, dataworking["project_cnty"]
                                        ):
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "The country assigned to the project does not exist in the ClimMob list."
                                                ),
                                            )
                                            return response

                                        if (
                                            dataworking["project_label_a"]
                                            != dataworking["project_label_b"]
                                            and dataworking["project_label_a"]
                                            != dataworking["project_label_c"]
                                            and dataworking["project_label_b"]
                                            != dataworking["project_label_c"]
                                        ):

                                            added, message = addProject(
                                                dataworking, self.request
                                            )

                                            if added:

                                                if (
                                                    "project_clone"
                                                    in dataworking.keys()
                                                ):
                                                    dataworking[
                                                        "slt_project_cod"
                                                    ] = dataworking["project_clone"]

                                                    ok = functionCreateClone(
                                                        self, dataworking
                                                    )

                                                    response = Response(
                                                        status=200,
                                                        body=self._(
                                                            "Project successfully cloned."
                                                        ),
                                                    )
                                                    return response

                                                if (
                                                    "usingTemplate"
                                                    in dataworking.keys()
                                                ):
                                                    listOfElementToInclude = [
                                                        "registry"
                                                    ]

                                                    assessments = getProjectAssessments(
                                                        dataworking["usingTemplate"],
                                                        self.request,
                                                    )
                                                    for assess in assessments:
                                                        listOfElementToInclude.append(
                                                            assess["ass_cod"]
                                                        )

                                                    newProjectId = getTheProjectIdForOwner(
                                                        self.user.login,
                                                        dataworking["project_cod"],
                                                        self.request,
                                                    )

                                                    functionCreateClone(
                                                        self,
                                                        dataworking["usingTemplate"],
                                                        newProjectId,
                                                        listOfElementToInclude,
                                                    )

                                            if not added:
                                                response = Response(
                                                    status=401, body=message
                                                )
                                                return response
                                            else:
                                                response = Response(
                                                    status=200,
                                                    body=self._(
                                                        "Project created successfully."
                                                    ),
                                                )
                                                return response
                                        else:
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "The names that the items will receive should be different."
                                                ),
                                            )
                                            return response
                                    else:
                                        response = Response(
                                            status=401,
                                            body=self._(
                                                "The number of combinations and observations must be greater than 0."
                                            ),
                                        )
                                        return response
                                else:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "A project already exists with this code."
                                        ),
                                    )
                                    return response
                            else:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "The project code must start with a letter."
                                    ),
                                )
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "For the project code only letters and numbers are allowed. The project code must start with a letter."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401, body=self._("Not all parameters have data.")
                        )
                        return response
                else:
                    response = Response(
                        status=401,
                        body=self._(
                            "You are trying to use a parameter that is not allowed.."
                        ),
                    )
                    return response
            else:
                response = Response(
                    status=401,
                    body=self._("It is not complying with the obligatory keys."),
                )
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class readProjects_view(apiView):
    def processView(self):
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        if self.request.method == "GET":

            response = Response(
                status=200,
                body=json.dumps(
                    getUserProjects(self.user.login, self.request), default=myconverter
                ),
            )
            return response
        else:
            response = Response(status=401, body=self._("Only accepts GET method."))
            return response


class updateProject_view(apiView):
    def processView(self):

        if self.request.method == "POST":

            possibles = [
                u"user_owner",
                u"project_cod",
                u"project_name",
                u"project_abstract",
                u"project_tags",
                u"project_pi",
                u"project_piemail",
                u"project_numobs",
                u"project_cnty",
                u"project_registration_and_analysis",
                u"user_name",
                u"project_numcom",
                u"project_label_a",
                u"project_label_b",
                u"project_label_c",
                u"project_template",
            ]
            obligatory = [u"project_cod", u"user_owner"]

            dataworking = json.loads(self.body)
            dataworking["user_name"] = self.user.login
            dataworking["project_numcom"] = 3

            permitedKeys = True
            for key in dataworking.keys():
                if key not in possibles:
                    permitedKeys = False

            obligatoryKeys = True

            for key in obligatory:
                if key not in dataworking.keys():
                    obligatoryKeys = False

            if obligatoryKeys:
                if permitedKeys:

                    dataInParams = True
                    for key in dataworking.keys():
                        if dataworking[key] == "":
                            dataInParams = False

                    if dataInParams:
                        dataworking["project_lat"] = ""
                        dataworking["project_lon"] = ""
                        exitsproject = projectExists(
                            self.user.login,
                            dataworking["user_owner"],
                            dataworking["project_cod"],
                            self.request,
                        )
                        if exitsproject:

                            activeProjectId = getTheProjectIdForOwner(
                                dataworking["user_owner"],
                                dataworking["project_cod"],
                                self.request,
                            )
                            accessType = getAccessTypeForProject(
                                self.user.login, activeProjectId, self.request
                            )

                            if accessType == 4:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "The access assigned for this project does not allow you to make modifications."
                                    ),
                                )
                                return response

                            cdata = getProjectData(activeProjectId, self.request)

                            if "project_template" in dataworking.keys():
                                existsTemplate = getProjectIsTemplate(
                                    self.request, dataworking["project_template"]
                                )
                                if existsTemplate:
                                    if (
                                        "project_registration_and_analysis"
                                        in dataworking.keys()
                                    ):
                                        if str(
                                            dataworking[
                                                "project_registration_and_analysis"
                                            ]
                                        ) == str(
                                            existsTemplate[
                                                "project_registration_and_analysis"
                                            ]
                                        ):
                                            dataworking["usingTemplate"] = dataworking[
                                                "project_template"
                                            ]
                                            dataworking["project_template"] = 0
                                        else:
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "You are trying to use a template that does not correspond to the type of project you are creating."
                                                ),
                                            )
                                            return response
                                    else:
                                        if str(
                                            cdata["project_registration_and_analysis"]
                                        ) == str(
                                            existsTemplate[
                                                "project_registration_and_analysis"
                                            ]
                                        ):
                                            dataworking["usingTemplate"] = dataworking[
                                                "project_template"
                                            ]
                                            dataworking["project_template"] = 0
                                        else:
                                            response = Response(
                                                status=401,
                                                body=self._(
                                                    "You are trying to use a template that does not correspond to the type of project you are creating."
                                                ),
                                            )
                                            return response
                                else:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "There is no template with this identifier."
                                        ),
                                    )
                                    return response

                            if cdata["project_regstatus"] != 0:
                                dataworking["project_numobs"] = cdata["project_numobs"]
                                dataworking["project_numcom"] = cdata["project_numcom"]

                            if "project_numobs" in dataworking.keys():
                                isNecessarygenerateCombinations = False
                                if int(dataworking["project_numobs"]) != int(
                                    cdata["project_numobs"]
                                ):
                                    isNecessarygenerateCombinations = True

                                if int(dataworking["project_numcom"]) != int(
                                    cdata["project_numcom"]
                                ):
                                    isNecessarygenerateCombinations = True

                                if isNecessarygenerateCombinations:
                                    changeTheStateOfCreateComb(
                                        activeProjectId, self.request,
                                    )

                            if (
                                "project_registration_and_analysis"
                                in dataworking.keys()
                            ):
                                if str(
                                    dataworking["project_registration_and_analysis"]
                                ) not in ["0", "1",]:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "The possible values in the parameter 'project_registration_and_analysis' are: ['0':' Registration is done first, followed by one or more data collection moments (with different forms)','1':'Requires registering participants and immediately asking questions to analyze the information']"
                                        ),
                                    )
                                    return response

                            if "project_localvariety" in dataworking.keys():
                                if str(dataworking["project_localvariety"]) not in [
                                    "0",
                                    "1",
                                ]:
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "The possible values in the parameter 'project_localvariety' are: ['0':'No','1':'Yes']"
                                        ),
                                    )
                                    return response

                            if "project_cnty" in dataworking.keys():
                                if not existsCountryByCode(
                                    self.request, dataworking["project_cnty"]
                                ):
                                    response = Response(
                                        status=401,
                                        body=self._(
                                            "The country assigned to the project does not exist in the ClimMob list."
                                        ),
                                    )
                                    return response
                            if not "project_label_a" in dataworking.keys():
                                dataworking["project_label_a"] = cdata[
                                    "project_label_a"
                                ]

                            if not "project_label_b" in dataworking.keys():
                                dataworking["project_label_b"] = cdata[
                                    "project_label_b"
                                ]

                            if not "project_label_c" in dataworking.keys():
                                dataworking["project_label_c"] = cdata[
                                    "project_label_c"
                                ]

                            if (
                                dataworking["project_label_a"]
                                != dataworking["project_label_b"]
                                and dataworking["project_label_a"]
                                != dataworking["project_label_c"]
                                and dataworking["project_label_b"]
                                != dataworking["project_label_c"]
                            ):

                                modified, message = modifyProject(
                                    activeProjectId, dataworking, self.request,
                                )

                                if modified:
                                    if (
                                        str(cdata["project_registration_and_analysis"])
                                        == "1"
                                        and str(
                                            dataworking[
                                                "project_registration_and_analysis"
                                            ]
                                        )
                                        == "0"
                                    ):
                                        deleteRegistryByProjectId(
                                            activeProjectId, self.request
                                        )

                                    if "usingTemplate" in dataworking.keys():
                                        deleteRegistryByProjectId(
                                            activeProjectId, self.request
                                        )
                                        deleteProjectAssessments(
                                            activeProjectId, self.request
                                        )

                                        listOfElementToInclude = ["registry"]

                                        assessments = getProjectAssessments(
                                            dataworking["usingTemplate"], self.request
                                        )
                                        for assess in assessments:
                                            listOfElementToInclude.append(
                                                assess["ass_cod"]
                                            )

                                        newProjectId = getTheProjectIdForOwner(
                                            self.user.login,
                                            dataworking["project_cod"],
                                            self.request,
                                        )

                                        functionCreateClone(
                                            self,
                                            dataworking["usingTemplate"],
                                            newProjectId,
                                            listOfElementToInclude,
                                        )

                                if not modified:
                                    response = Response(status=401, body=message)
                                    return response
                                else:
                                    response = Response(
                                        status=200,
                                        body=self._(
                                            "The project was modified successfully."
                                        ),
                                    )
                                    return response
                            else:
                                response = Response(
                                    status=401,
                                    body=self._(
                                        "The names that the items will receive should be different."
                                    ),
                                )
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._("There is no a project with that code."),
                            )
                            return response
                    else:
                        response = Response(
                            status=401, body=self._("Not all parameters have data.")
                        )
                        return response
                else:
                    response = Response(
                        status=401,
                        body=self._("Error in the parameters that you want to modify."),
                    )
                    return response
            else:
                response = Response(
                    status=401,
                    body=self._("It is not complying with the obligatory keys."),
                )
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class deleteProject_view_api(apiView):
    def processView(self):

        if self.request.method == "POST":

            obligatory = [u"project_cod", u"user_owner"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):

                if not projectExists(
                    self.user.login,
                    dataworking["user_owner"],
                    dataworking["project_cod"],
                    self.request,
                ):
                    response = Response(
                        status=401, body=self._("This project does not exist.")
                    )
                    return response

                activeProjectId = getTheProjectIdForOwner(
                    dataworking["user_owner"], dataworking["project_cod"], self.request
                )
                accessType = getAccessTypeForProject(
                    self.user.login, activeProjectId, self.request
                )

                if accessType in [4]:
                    response = Response(
                        status=401,
                        body=self._(
                            "The access assigned for this project does not allow you to delete the project."
                        ),
                    )
                    return response

                deleted, message = deleteProject(activeProjectId, self.request)
                if not deleted:
                    response = Response(status=401, body=message)
                    return response
                else:
                    response = Response(
                        status=200, body=self._("The project was deleted successfully")
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class readCollaborators_view(apiView):
    def processView(self):
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        if self.request.method == "GET":

            obligatory = [u"project_cod", u"user_owner"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):

                if not projectExists(
                    self.user.login,
                    dataworking["user_owner"],
                    dataworking["project_cod"],
                    self.request,
                ):
                    response = Response(
                        status=401, body=self._("This project does not exist.")
                    )
                    return response

                activeProjectId = getTheProjectIdForOwner(
                    dataworking["user_owner"], dataworking["project_cod"], self.request
                )

                response = Response(
                    status=200,
                    body=json.dumps(
                        get_collaborators_in_project(self.request, activeProjectId),
                        default=myconverter,
                    ),
                )
                return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts GET method."))
            return response


class addCollaborator_view(apiView):
    def processView(self):

        if self.request.method == "POST":

            obligatory = [
                u"project_cod",
                u"user_owner",
                "user_collaborator",
                "access_type",
            ]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):

                if not projectExists(
                    self.user.login,
                    dataworking["user_owner"],
                    dataworking["project_cod"],
                    self.request,
                ):
                    response = Response(
                        status=401, body=self._("This project does not exist.")
                    )
                    return response

                activeProjectId = getTheProjectIdForOwner(
                    dataworking["user_owner"], dataworking["project_cod"], self.request
                )
                accessType = getAccessTypeForProject(
                    self.user.login, activeProjectId, self.request
                )

                if accessType in [4]:
                    response = Response(
                        status=401,
                        body=self._(
                            "The access assigned for this project does not allow you to add collaborators to the project."
                        ),
                    )
                    return response

                if getUserInfo(self.request, dataworking["user_collaborator"]):

                    if not theUserBelongsToTheProject(
                        dataworking["user_collaborator"], activeProjectId, self.request,
                    ):
                        if dataworking["access_type"] in [2, 3, 4]:

                            dataworking["project_id"] = activeProjectId
                            dataworking["user_name"] = dataworking["user_collaborator"]
                            dataworking["project_dashboard"] = 0
                            added, message = add_project_collaborator(
                                self.request, dataworking
                            )

                            if added:
                                response = Response(
                                    status=200,
                                    body=self._("Collaborator added successfully."),
                                )
                                return response

                            else:
                                response = Response(status=401, body=message)
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "The types of access for collaborators are as follows: 2=Admin, 3=Editor, 4=Member."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._(
                                "The collaborator you want to add already belongs to the project."
                            ),
                        )
                        return response
                else:
                    response = Response(
                        status=401,
                        body=self._(
                            "The user you want to add as a collaborator does not exist."
                        ),
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response


class deleteCollaborator_view(apiView):
    def processView(self):

        if self.request.method == "POST":

            obligatory = [u"project_cod", u"user_owner", "user_collaborator"]
            dataworking = json.loads(self.body)

            if sorted(obligatory) == sorted(dataworking.keys()):

                if not projectExists(
                    self.user.login,
                    dataworking["user_owner"],
                    dataworking["project_cod"],
                    self.request,
                ):
                    response = Response(
                        status=401, body=self._("This project does not exist.")
                    )
                    return response

                activeProjectId = getTheProjectIdForOwner(
                    dataworking["user_owner"], dataworking["project_cod"], self.request
                )
                accessType = getAccessTypeForProject(
                    self.user.login, activeProjectId, self.request
                )

                if accessType in [4]:
                    response = Response(
                        status=401,
                        body=self._(
                            "The access assigned for this project does not allow you to delete collaborators from the project."
                        ),
                    )
                    return response

                if getUserInfo(self.request, dataworking["user_collaborator"]):

                    if theUserBelongsToTheProject(
                        dataworking["user_collaborator"], activeProjectId, self.request,
                    ):
                        if (
                            dataworking["user_owner"]
                            != dataworking["user_collaborator"]
                        ):

                            remove, message = remove_collaborator(
                                self.request,
                                activeProjectId,
                                dataworking["user_collaborator"],
                                self,
                            )

                            if remove:
                                response = Response(
                                    status=200,
                                    body=self._(
                                        "The collaborator has been successfully removed."
                                    ),
                                )
                                return response

                            else:
                                response = Response(status=401, body=message)
                                return response
                        else:
                            response = Response(
                                status=401,
                                body=self._(
                                    "The user who owns the project cannot be deleted."
                                ),
                            )
                            return response
                    else:
                        response = Response(
                            status=401,
                            body=self._(
                                "You are trying to delete a collaborator that does not belong to this project."
                            ),
                        )
                        return response
                else:
                    response = Response(
                        status=401,
                        body=self._(
                            "The user you want to delete as a collaborator does not exist."
                        ),
                    )
                    return response
            else:
                response = Response(status=401, body=self._("Error in the JSON."))
                return response
        else:
            response = Response(status=401, body=self._("Only accepts POST method."))
            return response
