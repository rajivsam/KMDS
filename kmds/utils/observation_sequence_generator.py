
class SequenceGenerator:

    def __init__(self, desc:str = "sequence generator") -> None:
        self._desc = desc
        self._observationNumber = 0
        return
    
    def next_obs_number(self) -> int:
        self._observationNumber += 1
        return self._observationNumber
    
    