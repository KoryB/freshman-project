class SimpleTimer(object):
    """
    Just a simple Timer class to help keep track of different timers I use.
    Good for reload timers, animation timers, anything really. Really basic.
    """

    def __init__(self, length, stopOnReach=False):
        """
        Assuming timer counts up until length is reached, then mReached is set to True.
        :param length: amount of time (in seconds) the Timer will count to
        :return: N/A
        """

        self.mLength = length
        self.mCurTime = 0

        self.mReached = False
        self.mRunning = False

        self.mStopOnReach = stopOnReach

    def update(self, dtime):
        """
        ticks up mAnimationLength by dtime. Triggers mReached to True
        :param dtime: amount of time (in seconds) timer will count up
        """

        if self.mRunning:
            self.mCurTime += dtime


            if self.mCurTime >= self.mLength:
                if self.mStopOnReach:
                    self.mCurTime = 0
                    self.mRunning = False

                self.mReached = True

    def reset(self):
        """
        Resets mCurTime to 0, resets mReached to False
        """

        self.mCurTime = 0
        self.mReached = False
        self.mRunning = False

    def start(self):
        """
        starts the timer. sets self.mRunning to True
        :return:
        """
        self.mRunning = True