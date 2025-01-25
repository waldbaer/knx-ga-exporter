"""Representation of a KNX group address (GA)."""

# ---- Imports ---------------------------------------------------------------------------------------------------------
from dataclasses import dataclass

# ---- Class / Functions -----------------------------------------------------------------------------------------------


@dataclass
class GroupAddress:
    """Representation of a KNX group address."""

    def __init__(
        self,
        main: str,
        middle: str,
        sub: str,
        main_name: str,
        middle_name: str,
        sub_name: str,
        target_id: str,
        dpt: str,
        comment: str,
    ) -> None:
        """Constructor.

        Args:
            main (str): Main group ID
            middle (str): Middle group ID
            sub (str): Sub group ID
            main_name (str): Main group name
            middle_name (str): Middle group name
            sub_name (str): Sub group name
            target_id (str): Target ID
            dpt (str): DPT datatype
            comment (str): comment
        """
        self.main = main
        self.middle = middle
        self.sub = sub
        self.main_name = main_name
        self.middle_name = middle_name
        self.sub_name = sub_name
        self.target_id = target_id
        self.dpt = dpt
        self.comment = comment
        self._validate()

    def _validate(self) -> None:
        # check mandatory attributes
        if (
            self.main is None
            or self.middle is None
            or self.sub is None
            or self.main_name is None
            or self.middle_name is None
            or self.sub_name is None
            or self.dpt is None
        ):
            raise ValueError(f"Incomplete KNX group address detected: {str(self)}")

    def __str__(self) -> str:
        """Build string representation.

        Returns:
            Formatted string.
        """
        addr_formatted = f"{self.main}/{self.middle}/{self.sub}"
        return (
            f"{addr_formatted:8s} | {self.main_name} | {self.middle_name} | "
            + f"{self.dpt} | {self.target_id} - {self.sub_name}"
        )
