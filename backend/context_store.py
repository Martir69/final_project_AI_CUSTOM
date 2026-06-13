"""Almacenamiento persistente de contexto por usuario en JSON."""

import json
import os


class ContextStore:
    """Guarda y recupera entradas de contexto por usuario en un archivo JSON."""

    def __init__(self, path="data/context_store.json"):
        """Inicializa el store apuntando al archivo en *path*."""
        self.path = path
        self._data = self._load()

    def _load(self):
        """Lee el archivo JSON y retorna el dict; retorna {} si no existe o está vacío."""
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def _persist(self):
        """Escribe el estado actual en el archivo JSON."""
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def save(self, user_id, key, value):
        """Agrega un ítem {key, value} al usuario y persiste en disco. Retorna el ítem."""
        item = {"key": key, "value": value}
        self._data.setdefault(user_id, []).append(item)
        self._persist()
        return item

    def list_for_user(self, user_id):
        """Retorna la lista de entradas del usuario o [] si no existe."""
        return self._data.get(user_id, [])
