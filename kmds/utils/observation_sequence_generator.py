
class ObservationSequence:

    def __init__(self,) -> None:
        """ In a notebook, or real world setting, we don't know apriori how many observations we are going to make. When a sequence generator is used, we can simply keep calling next observation to get the next sequence number instead of coding the counting logic in the notebooks while tagging the observations
        """
        self._observationNumber = 1
        return
    
    def next_obs_number(self) -> int:
        """ This provides the next observation number (see above docstring)

        Returns:
            int: next observation number

        Yields:
            Iterator[int]: the observation iterator
        """
        yield self._observationNumber


    
    