import os
import importlib.util
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Any] = {}
        self.plugin_status: Dict[str, bool] = {}

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                self._load_plugin(plugin_name)

    def _load_plugin(self, plugin_name: str):
        try:
            file_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")
            spec = importlib.util.spec_from_file_location(plugin_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Instantiate if it has a 'Plugin' class
            if hasattr(module, "Plugin"):
                plugin_instance = module.Plugin()
                self.plugins[plugin_name] = plugin_instance
                self.plugin_status[plugin_name] = True
                logger.info(f"Loaded plugin: {plugin_name}")

                # Auto-start if it has a start method
                if hasattr(plugin_instance, "on_load"):
                     plugin_instance.on_load()
            else:
                logger.warning(f"File {plugin_name}.py does not contain a 'Plugin' class.")

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            self.plugin_status[plugin_name] = False

    def get_plugins(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": name,
                "enabled": self.plugin_status.get(name, False),
                "description": getattr(self.plugins.get(name), "description", "No description")
            }
            for name in self.plugins.keys()
        ]

    def toggle_plugin(self, name: str, enabled: bool):
        if name in self.plugins:
            self.plugin_status[name] = enabled
            plugin = self.plugins[name]
            if enabled:
                if hasattr(plugin, "on_enable"): plugin.on_enable()
            else:
                if hasattr(plugin, "on_disable"): plugin.on_disable()
            return True
        return False

# Global instance
plugin_manager = PluginManager()
