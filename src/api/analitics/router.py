from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from starlette import status

from src.api.analitics.request import GetAnalyticsRequest
from src.api.analitics.response import GetAnalyticsDetailsResponse, GetActivityDetailsResponse
from src.container import AppContainer
from src.handlers.interface import QueryHandlerInterface
from src.query.analytics import GetAnalyticsQuery, GetActivityQuery
from src.repositories.errors import PersistenceError

router = APIRouter()


@router.post('/analytics', response_model=GetAnalyticsDetailsResponse)
@inject
def get_analytics(
        request: GetAnalyticsRequest,
        handler: QueryHandlerInterface[GetAnalyticsQuery, GetAnalyticsDetailsResponse] =
        Depends(Provide[AppContainer.handlers.get_analytics])
) -> GetAnalyticsDetailsResponse:
    try:
        post_data = handler.handle(GetAnalyticsQuery(date_from=request.date_from, date_to=request.date_to))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_data


@router.get('/analytics/activity/{user_id}', response_model=GetActivityDetailsResponse)
@inject
def get_user_activity(
        user_id: str,
        handler: QueryHandlerInterface[GetActivityQuery, GetActivityDetailsResponse] =
        Depends(Provide[AppContainer.handlers.get_user_activity])
) -> GetActivityDetailsResponse:
    try:
        post_data = handler.handle(GetActivityQuery(user_id=user_id))
    except PersistenceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return post_data
