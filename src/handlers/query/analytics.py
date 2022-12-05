from sqlalchemy.exc import SQLAlchemyError

from src.api.analitics.response import GetAnalyticsDetailsResponse, GetActivityDetailsResponse
from src.api.analitics.response import AnalyticsCardResponse
from src.api.error_handlers import DomainError
from src.handlers.interface import QueryHandlerInterface
from src.query.analytics import GetAnalyticsQuery
from src.query.analytics import GetActivityQuery
from src.repositories.errors import UserNotExistsError
from src.repositories.interface import AnalyticsRepositoryInterface


class GetAnalyticsQueryHandler(QueryHandlerInterface):
    def __init__(self, analytic_repository: AnalyticsRepositoryInterface) -> None:
        self.analytic_repository = analytic_repository

    def handle(self, query: GetAnalyticsQuery) -> GetAnalyticsDetailsResponse:
        with self.analytic_repository.autocommit():
            try:
                likes = self.analytic_repository.get_analytics_by_filter(query)
                loaded_data = GetAnalyticsDetailsResponse(
                    likes=[
                        AnalyticsCardResponse(date=k, qty=v) for k, v in likes.items()
                    ])
            except SQLAlchemyError:
                raise DomainError('Failed to get analytics information')
        return loaded_data


class GetActivityQueryHandler(QueryHandlerInterface):
    def __init__(self, analytic_repository: AnalyticsRepositoryInterface) -> None:
        self.analytic_repository = analytic_repository

    def handle(self, query: GetActivityQuery) -> GetActivityDetailsResponse:
        with self.analytic_repository.autocommit():
            try:
                user = self.analytic_repository.get_user_by_id(query.user_id)
                loaded_data = GetActivityDetailsResponse(
                    last_login=user.date_logged.date(),
                    last_request=user.date_updated.date() if user.date_updated is not None else None,
                )
            except SQLAlchemyError:
                raise DomainError('Failed to get activity information')
            except UserNotExistsError as e:
                raise DomainError(str(e))
        return loaded_data
