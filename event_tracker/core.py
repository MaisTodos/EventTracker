import logging
from typing import List, Optional, Set

from .messages import Contexts, EventTrackerMessage, Tags
from .provider_strategy import IProviderStrategy

logger = logging.getLogger(__name__)


class EventTracker:
    def __init__(
        self,
        providers: List[IProviderStrategy],
        message_provider_map: Optional[List[tuple[str, List[str]]]] = None,
    ):
        message_provider_map = message_provider_map or []

        self.__all_providers = []
        self.__providers_by_name = {}

        for provider in providers:
            self.__all_providers.append(provider)
            self.__providers_by_name[provider.name] = provider

        self.__providers_by_message_name = {}
        for message_name, providers_names in message_provider_map:

            providers = [
                self.__providers_by_name[name]
                for name in providers_names
                if name in self.__providers_by_name
            ]

            if not providers:
                logger.warning(f"No valid providers found for message '{message_name}'")
                continue

            self.__providers_by_message_name[message_name] = providers

    def set_tags(self, tags: Tags, providers_names: Optional[List[str]] = None):
        providers: Set[IProviderStrategy] = set()

        if providers_names:
            providers.update(self.__get_providers_by_names(providers_names))

        if not providers:
            providers = set(self.__all_providers)

        for provider in providers:
            try:
                provider.set_tags(tags)
            except Exception as e:
                logger.error(f"Error setting tags for provider {provider}: {e}")

    def set_contexts(
        self, contexts: Contexts, providers_names: Optional[List[str]] = None
    ):
        providers: Set[IProviderStrategy] = set()

        if providers_names:
            providers.update(self.__get_providers_by_names(providers_names))

        if not providers:
            providers = set(self.__all_providers)

        for provider in providers:
            try:
                provider.set_contexts(contexts)
            except Exception as e:
                logger.error(f"Error setting contexts for provider {provider}: {e}")

    def emit(
        self,
        event_message: EventTrackerMessage,
        providers_names: Optional[List[str]] = None,
    ):
        providers: Set[IProviderStrategy] = set()

        providers.update(self.__get_providers_by_message_name(event_message.name))

        if providers_names:
            providers.update(self.__get_providers_by_names(providers_names))

        if not providers:
            providers = set(self.__all_providers)

        for provider in providers:
            try:
                provider.track(
                    event=event_message.message,
                    tags=event_message.tags,
                    contexts=event_message.contexts,
                )
            except Exception as e:
                logger.error(f"Error tracking event for provider {provider}: {e}")

    def __get_providers_by_message_name(
        self, message_name: str
    ) -> List[IProviderStrategy]:
        return self.__providers_by_message_name.get(message_name, [])

    def __get_providers_by_names(self, names: List[str]) -> List[IProviderStrategy]:
        providers = []
        for name in names:
            provider = self.__providers_by_name.get(name)
            if not provider:
                logger.warning(f"Provider with name '{name}' not found")
                continue

            providers.append(provider)
        return providers
