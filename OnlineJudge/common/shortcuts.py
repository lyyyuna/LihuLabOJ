from rest_framework.response import Response


def successResponse(result,*args, **kwargs):
    return Response(data={"code": 0, "data": result},*args, **kwargs)


def errorResponse(reason,*args, **kwargs):
    return Response(data={'code': 1, 'data': reason},*args, **kwargs)