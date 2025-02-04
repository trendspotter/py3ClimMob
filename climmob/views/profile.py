from climmob.views.classes import privateView
from climmob.processes import (
    getUserLog,
    getUserStats,
    getCountryList,
    getSectorList,
    otherUserHasEmail,
    updateProfile,
    addToLog,
    getActiveProject,
    changeUserPassword,
)
import datetime
from climmob.config.auth import getUserData


class profile_view(privateView):
    def processView(self):
        limit = True
        if "all" in self.request.params:
            if self.request.params["all"] == "True":
                limit = False
        activities = getUserLog(self.user.login, self.request, limit)
        userstats = getUserStats(self.user.login, self.request)
        return {
            "activeProject": getActiveProject(self.user.login, self.request),
            "activities": activities,
            "userstats": userstats,
        }


class editProfile_view(privateView):
    def processView(self):
        userstats = getUserStats(self.user.login, self.request)
        error_summary = {}
        passChanged = False
        profileUpdated = False

        if self.request.method == "POST":
            if "saveprofile" in self.request.POST:
                data = self.getPostDict()
                # print ("*****************77")
                # print (data)
                # print ("*****************77")
                if data["user_fullname"] != "":
                    if data["user_email"] != "":
                        if data["user_organization"] != "":
                            if not otherUserHasEmail(
                                self.user.login, data["user_email"], self.request
                            ):
                                updated, uerror = updateProfile(
                                    self.user.login, data, self.request
                                )
                                if updated:
                                    self.user.userData = data.copy()
                                    self.user.email = data["user_email"]
                                    self.user.organization = data["user_organization"]
                                    self.user.fullName = data["user_fullname"]
                                    self.user.country = data["user_cnty"]
                                    self.user.sector = data["user_sector"]
                                    self.user.about = data["user_about"]
                                    self.user.updateGravatarURL()
                                    addToLog(
                                        self.user.login,
                                        "PRF",
                                        "Updated profile",
                                        datetime.datetime.now(),
                                        self.request,
                                    )
                                    profileUpdated = True
                                else:
                                    error_summary["ChangeProfile"] = uerror
                            else:
                                error_summary["ChangeProfile"] = self._(
                                    "User with the same email address has already been registered."
                                )
                        else:
                            error_summary["ChangeProfile"] = self._(
                                "Organization cannot be empty"
                            )
                    else:
                        error_summary["ChangeProfile"] = self._("Email cannot be empty")
                else:
                    error_summary["ChangeProfile"] = self._("Full name cannot be empty")

            if "changepass" in self.request.POST:
                user = getUserData(self.user.login, self.request)
                # if self.request.POST.get('user_password1', '') == getUserPassword(self.user.login,self.request):
                if user.check_password(
                    self.request.POST.get("user_password1", ""), self.request
                ):
                    if self.request.POST.get("user_password2", "") != "":
                        if self.request.POST.get(
                            "user_password2", ""
                        ) == self.request.POST.get("user_password3", ""):
                            if changeUserPassword(
                                self.user.login,
                                self.request.POST.get("user_password2", ""),
                                self.request,
                            ):
                                addToLog(
                                    self.user.login,
                                    "PRF",
                                    "Changed password",
                                    datetime.datetime.now(),
                                    self.request,
                                )
                                passChanged = True
                            else:
                                error_summary["ChangePass"] = self._(
                                    "Cannot change password"
                                )
                        else:
                            error_summary["ChangePass"] = self._(
                                "New password and re-type are not equal"
                            )
                    else:
                        error_summary["ChangePass"] = self._(
                            "New password cannot be empty"
                        )
                else:
                    error_summary["ChangePass"] = self._(
                        "The current password is not valid"
                    )

        # self.needJS('editprofile')
        # self.needCSS('select2')
        return {
            "activeProject": getActiveProject(self.user.login, self.request),
            "userstats": userstats,
            "data": self.decodeDict(self.user.userData),
            "error_summary": error_summary,
            "passChanged": passChanged,
            "profileUpdated": profileUpdated,
            "countries": getCountryList(self.request),
            "sectors": getSectorList(self.request),
        }
