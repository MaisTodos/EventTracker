import logging
from typing import Dict, List, Optional, Set

from .messages import Contexts, EventTrackerMessage, Tags
from .provider_strategy import IProviderStrategy

logger = logging.getLogger(__name__)


class EventTracker:
    def __init__(
        self,
        strategies: List[IProviderStrategy],
        strategies_by_message: Optional[Dict[str, List[str]]] = None,
    ):
        strategies_by_message = strategies_by_message or {}

        self.__all_strategies = []
        self.__strategy_by_name = {}

        for strategy in strategies:
            self.__all_strategies.append(strategy)
            self.__strategy_by_name[strategy.name] = strategy

        self.__strategies_by_message_name = {}
        for message_name, strategies_names in strategies_by_message.items():

            strategies = [
                self.__strategy_by_name[name]
                for name in strategies_names
                if name in self.__strategy_by_name
            ]

            if not strategies:
                logger.warning(
                    f"No valid strategies found for message '{message_name}'"
                )
                continue

            self.__strategies_by_message_name[message_name] = strategies

    def set_tags(self, tags: Tags, strategies_names: Optional[List[str]] = None):
        strategies: Set[IProviderStrategy] = set()

        if strategies_names:
            strategies.update(self.__get_strategies_by_names(strategies_names))

        if not strategies:
            strategies = set(self.__all_strategies)

        for strategy in strategies:
            try:
                strategy.set_tags(tags)
            except Exception as e:
                logger.error(f"Error setting tags for strategy {strategy}: {e}")

    def set_contexts(
        self, contexts: Contexts, strategies_names: Optional[List[str]] = None
    ):
        strategies: Set[IProviderStrategy] = set()

        if strategies_names:
            strategies.update(self.__get_strategies_by_names(strategies_names))

        if not strategies:
            strategies = set(self.__all_strategies)

        for strategy in strategies:
            try:
                strategy.set_contexts(contexts)
            except Exception as e:
                logger.error(f"Error setting contexts for strategy {strategy}: {e}")

    def emit(
        self,
        event_message: EventTrackerMessage,
        strategies_names: Optional[List[str]] = None,
    ):
        strategies: Set[IProviderStrategy] = set()

        strategies.update(self.__get_strategies_by_message_name(event_message.name))

        if strategies_names:
            strategies.update(self.__get_strategies_by_names(strategies_names))

        if not strategies:
            strategies = set(self.__all_strategies)

        for strategy in strategies:
            try:
                strategy.track(
                    event=event_message.message,
                    tags=event_message.tags,
                    contexts=event_message.contexts,
                )
            except Exception as e:
                logger.error(f"Error tracking event for strategy {strategy}: {e}")

    def __get_strategies_by_message_name(
        self, message_name: str
    ) -> List[IProviderStrategy]:
        return self.__strategies_by_message_name.get(message_name, [])

    def __get_strategies_by_names(self, names: List[str]) -> List[IProviderStrategy]:
        strategies = []
        for name in names:
            strategy = self.__strategy_by_name.get(name)
            if not strategy:
                logger.warning(f"Strategy with name '{name}' not found")
                continue

            strategies.append(strategy)
        return strategies
