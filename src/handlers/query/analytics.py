from sqlalchemy.exc import SQLAlchemyError

from src.api.analitics.response import GetAnalyticsDetailsResponse
from src.api.analitics.response import AnalyticsCardResponse
from src.api.error_handlers import DomainError
from src.handlers.interface import QueryHandlerInterface
from src.query.analytics import GetAnalyticsQuery
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
