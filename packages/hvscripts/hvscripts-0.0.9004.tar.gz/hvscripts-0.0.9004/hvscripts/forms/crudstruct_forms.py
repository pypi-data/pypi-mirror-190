import datetime
import pytz
from ..string import RandomIdentifier
from ..config import pagesPossibles
from .. import JON
from ..config import pagesPossibles, responsesPossibles


def structEditResult(lang: str):
    return JON.Object(lang).struct({
        'data': JON.Object(lang).min(1).required(),
        'notif': JON.Object(lang).struct({
            'type': JON.Enum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JON.Enum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JON.Enum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JON.Enum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    })
def structEditMultipleResult(lang: str):
    return JON.Object(lang).struct({
        'data': JON.Array(lang).types(
            JON.Object(lang).min(1).required(),
        ).min(1).required(),
        'notif': JON.Object(lang).struct({
            'type': JON.Enum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JON.Enum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JON.Enum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JON.Enum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    })


def structFindOneResult(lang: str):
    return JON.Object(lang).struct({
        'data': JON.Object(lang).min(1).required(),
        'exists': JON.Enum(lang).choices(True).required(),
        'notif': JON.Object(lang).struct({
            'type': JON.Enum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JON.Enum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JON.Enum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JON.Enum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()
def structExistsResult(lang: str):
    return JON.Object(lang).struct({
        'exists': JON.Enum(lang).choices(True).required(),
        'notif': JON.Object(lang).struct({
            'type': JON.Enum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JON.Enum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JON.Enum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JON.Enum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()
def structFindAllResult(lang: str):
    return JON.Object(lang).struct({
        'datas': JON.Array(lang).types(
            JON.Object(lang).required()
        ).required(),
        'meta': JON.Object(lang).struct({
            'pagination': JON.Object(lang).struct({
                'page': JON.Number(lang).min(1).required(),
                'pageSize': JON.Enum(lang).choices(*pagesPossibles).required(),
                'pageLength': JON.Number(lang).min(1).required(),
                'pageCount': JON.Number(lang).min(1).required(),
                'total': JON.Number(lang).min(0).required(),
            }).required(),
        }).required(),
        'notif': JON.Object(lang).struct({
            'type': JON.Enum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JON.Enum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JON.Enum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JON.Enum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()
    
def structExtractResult(lang: str):
    return JON.Object(lang).struct({
        'datas': JON.Array(lang).types(
            JON.Object(lang).required()
        ).required(),
        'meta': JON.Object(lang).struct({
            'invalid-datas': JON.Array(lang).types(
                JON.Object(lang).struct({
                    'key': JON.Number(lang).min(1).required(),
                    'schemas': JON.Array(lang).types(
                        JON.String(lang).min(1).required()
                    ).required(),
                }).required(),
            ).length(0),
        }),
        'notif': JON.Object(lang).struct({
            'type': JON.Enum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JON.Enum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JON.Enum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JON.Enum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()