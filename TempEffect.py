class TempEffect(object):

    def __init__(self, owner, attr, mod, timerLength):
        """
        This class defines a temporary effect and handles the timing of it as well
        :param owner: an Entity object
        :param attr: the ATTRibute to be modified, a string
        :param mod: the amount to MODify
        :param timerLength: the amount of time the effect should last
        :return: N/A
        """

        self.mOwner = owner
        self.mModAttr = attr
        self.mModAmount = mod

        self.mTimerLength = timerLength
        self.mCurTime = 0

        self.mIsReached = False


    def onEnter(self):
        """
        This function is to be called whenever the effect is first applied
        :return: None
        """

        setattr(self.mOwner, self.mModAttr, getattr(self.mOwner, self.mModAttr)+self.mModAmount)


    def update(self, dtime):
        """
        This simply updates the timer dtime amount of time
        :param dtime: amount of time passed since last call
        :return: None
        """

        if not self.mIsReached:
            self.mCurTime += dtime
            self.mIsReached = self.mCurTime >= self.mTimerLength


    def onExit(self):
        """
        This function should be called whenever the timer is reached and the effect should be removed
        :return: None
        """

        setattr(self.mOwner, self.mModAttr, getattr(self.mOwner, self.mModAttr)-self.mModAmount)
