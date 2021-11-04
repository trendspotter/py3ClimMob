from climmob.models.climmobv4 import Technology, Techalia, Prjtech, I18nTechnology
from ...models.schema import mapToSchema, mapFromSchema
from sqlalchemy import func, and_
from .techaliases import getTechsAlias

__all__ = [
    "getUserTechs",
    "findTechInLibrary",
    "addTechnology",
    "getTechnology",
    "updateTechnology",
    "deleteTechnology",
    "getTechnologyByUser",
    "getTechnologyAssigned",
    "technologyExist",
    "isTechnologyAssigned",
    "getTechnologyByName",
    "getUserTechById",
]


def getUserTechs(user, request):

    res = []
    result = (
        request.dbsession.query(
            Technology,
            request.dbsession.query(func.count(Techalia.tech_id))
            .filter(Technology.tech_id == Techalia.tech_id)
            .label("quantity"),
            func.coalesce(I18nTechnology.tech_name, Technology.tech_name).label(
                "tech_name"
            ),
        )
        .join(
            I18nTechnology,
            and_(
                Technology.tech_id == I18nTechnology.tech_id,
                I18nTechnology.lang_code == request.locale_name,
            ),
            isouter=True,
        )
        .filter(Technology.user_name == user)
        .order_by(Technology.tech_name)
        .all()
    )

    for technology in result:

        res3 = (
            request.dbsession.query(func.count(Prjtech.tech_id).label("found")).filter(
                Prjtech.tech_id == technology[0].tech_id
            )
            # .filter(Prjtech.user_name == user)
            .one()
        )

        res.append(
            {
                "tech_id": technology[0].tech_id,
                # "tech_name": technology[0].tech_name,
                "tech_crop": technology[0].tech_crop,
                "tech_name": technology[2],
                "user_name": technology[0].user_name,
                "quantity": technology.quantity,
                "tech_alias": getTechsAlias(technology[0].tech_id, request),
                "found": res3.found,
            }
        )

    return res


def getUserTechById(tech_id, request):

    res = []
    result = mapFromSchema(
        request.dbsession.query(
            Technology,
            request.dbsession.query(func.count(Techalia.tech_id))
            .filter(Technology.tech_id == Techalia.tech_id)
            .label("quantity"),
        )
        .filter(Technology.tech_id == tech_id)
        .one()
    )

    res3 = (
        request.dbsession.query(func.count(Prjtech.tech_id).label("found"))
        .filter(Prjtech.tech_id == tech_id)
        .one()
    )

    result["tech_alias"] = getTechsAlias(tech_id, request)
    result["found"] = res3.found

    return result


def findTechInLibrary(data, request, adding=True):
    if adding:
        result = (
            request.dbsession.query(Technology)
            .filter(
                Technology.user_name == data["user_name"],
                Technology.tech_name == data["tech_name"],
            )
            .all()
        )
    else:
        result = (
            request.dbsession.query(Technology)
            .filter(
                Technology.user_name == data["user_name"],
                Technology.tech_name == data["tech_name"],
                Technology.tech_id != data["tech_id"],
            )
            .all()
        )

    if not result:
        return False
    else:
        return True


def addTechnology(data, request):
    mappeData = mapToSchema(Technology, data)
    newTech = Technology(**mappeData)
    try:
        request.dbsession.add(newTech)
        return True, ""

    except Exception as e:
        return False, e


def getTechnology(data, request):
    return mapFromSchema(
        request.dbsession.query(Technology)
        .filter(Technology.tech_id == data["tech_id"])
        .one()
    )


def technologyExist(data, request):
    result = (
        request.dbsession.query(Technology)
        .filter(Technology.tech_id == data["tech_id"])
        .filter(Technology.user_name == data["user_name"])
        .first()
    )
    if result:
        return True
    else:
        result = (
            request.dbsession.query(Technology)
            .filter(Technology.tech_id == data["tech_id"])
            .filter(Technology.user_name == "bioversity")
            .first()
        )
        if result:
            return True
        else:
            return False


def getTechnologyByName(data, request):
    return mapFromSchema(
        request.dbsession.query(Technology)
        .filter(
            Technology.user_name == data["user_name"],
            Technology.tech_name == data["tech_name"],
        )
        .one()
    )


def getTechnologyByUser(data, request):
    result = (
        request.dbsession.query(Technology)
        .filter(Technology.user_name == data["user_name"])
        .filter(Technology.tech_id == data["tech_id"])
        .all()
    )

    if not result:
        return False
    else:
        return True


def getTechnologyAssigned(data, request):
    result = (
        request.dbsession.query(func.count(Prjtech.tech_id).label("found"))
        .filter(Prjtech.tech_id == data["tech_id"])
        .filter(Prjtech.user_name == data["user_name"])
        .one()
    )

    if result.found == 0:
        return False
    else:
        return True


def isTechnologyAssigned(data, request):
    result = (
        request.dbsession.query(func.count(Prjtech.tech_id).label("found"))
        .filter(Prjtech.tech_id == data["tech_id"])
        .filter(Prjtech.user_name == data["user_name"])
        .filter(Prjtech.project_cod == data["project_cod"])
        .one()
    )

    if result.found == 0:
        return False
    else:
        return True


def updateTechnology(data, request):
    try:
        mappeData = mapToSchema(Technology, data)
        request.dbsession.query(Technology).filter(
            Technology.user_name == data["user_name"]
        ).filter(Technology.tech_id == data["tech_id"]).update(mappeData)
        return True, ""
    except Exception as e:
        return False, e


def deleteTechnology(data, request):
    try:
        request.dbsession.query(Technology).filter(
            Technology.user_name == data["user_name"]
        ).filter(Technology.tech_id == data["tech_id"]).delete()
        return True, ""

    except Exception as e:
        return False, e
