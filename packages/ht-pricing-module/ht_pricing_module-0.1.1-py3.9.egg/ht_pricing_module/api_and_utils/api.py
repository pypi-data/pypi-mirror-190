class OptionTypeEnum:
    @property
    def CALL(self) -> int: return 1

    @property
    def PUT(self) -> int: return 2


class ExerciseTypeEnum:
    @property
    def EUROPEAN(self) -> int: return 1

    @property
    def AMERICAN(self) -> int: return 2


class BarrierTypeEnum:
    @property
    def UP(self) -> int: return 1

    @property
    def DOWN(self) -> int: return 2


class KnockTypeEnum:
    @property
    def IN(self) -> int: return 1

    @property
    def OUT(self) -> int: return 2


class DirectionTypeEnum:
    @property
    def STANDARD(self) -> int: return 1

    @property
    def REVERSE(self) -> int: return 2


OptionType = OptionTypeEnum()
ExerciseType = ExerciseTypeEnum()
BarrierType = BarrierTypeEnum()
KnockType = KnockTypeEnum()
DirectionType = DirectionTypeEnum()