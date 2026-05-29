from app.plugins.base import DataSourcePlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, DataSourcePlugin] = {}

    def register(self, plugin: DataSourcePlugin) -> None:
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> DataSourcePlugin | None:
        return self._plugins.get(name)

    def list_names(self) -> list[str]:
        return sorted(self._plugins.keys())
