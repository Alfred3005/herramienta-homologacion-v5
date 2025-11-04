"""
Filtro por nivel salarial.
Permite filtrar puestos por grado (G, H, I, J, K, L, M, etc.)
"""

from typing import List, Dict, Any, Set
import math


class NivelSalarialFilter:
    """
    Filtra puestos por nivel salarial (GRADO).

    Ejemplos de uso:
        - Niveles individuales: ["G", "H", "I"]
        - Rangos: ["M1", "M2", "M3", "M4", "M5"]
        - Mixto: ["K", "L", "M1", "M2"]
    """

    def __init__(self, niveles: List[str]):
        """
        Inicializa filtro de nivel salarial.

        Args:
            niveles: Lista de códigos de nivel (ej: ["G", "H", "I", "J", "K"])
        """
        self.niveles: Set[str] = set(niveles)

    def match(self, puesto_data: Dict[str, Any]) -> bool:
        """
        Verifica si el puesto tiene uno de los niveles especificados.

        Args:
            puesto_data: Datos del puesto

        Returns:
            True si el nivel del puesto está en la lista de niveles
        """
        nivel = puesto_data.get('GRADO', '')

        # Manejar None y NaN
        if nivel is None or (isinstance(nivel, float) and math.isnan(nivel)):
            return False

        # Convertir a string y limpiar
        nivel_str = str(nivel).strip().upper()

        # Remover ".0" si es un float convertido a string (ej: "1.0" -> "1")
        if nivel_str.endswith('.0'):
            nivel_str = nivel_str[:-2]

        return nivel_str in self.niveles

    def get_description(self) -> str:
        """Descripción del filtro"""
        niveles_ordenados = sorted(list(self.niveles))
        return f"Nivel salarial: {', '.join(niveles_ordenados)}"
