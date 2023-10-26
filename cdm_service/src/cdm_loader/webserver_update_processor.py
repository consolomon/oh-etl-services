import requests
from requests import HTTPError
from datetime import datetime
from logging import Logger

from app_config import AppConfig


class WebserverUpdateProcessor:
    def __init__(
        self,
        logger: Logger,
        config: AppConfig
    ) -> None:
        self.logger = logger
        self.config = config

    def run(self) -> None:

        self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: START")

        response = requests.get(
            url=self.config.UPDATE_URL,
            headers={
                "x-api-key": self.config.API_ADMIN_KEY
            },
            timeout=600
        )

        try:
            response.raise_for_status()
            stats = response.json()

            self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: SUCCESS, UPLOAD STATS:")
            self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: new_positions_count: {stats['new_positions_count']}")
            self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: new_vacancy_count: {stats['new_vacancy_count']}")
            self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: new_tech_count: {stats['new_tech_count']}")
            self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: position_match_count: {stats['position_match_count']}")
            self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: tech_match_count: {stats['tech_match_count']}")

        except HTTPError as e:
            self.logger.error(f"WebserverUpdateProcessor: {datetime.utcnow()}: {e}")

        self.logger.info(f"WebserverUpdateProcessor: {datetime.utcnow()}: FINISH")
