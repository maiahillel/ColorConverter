class CalibratedPair(webcams.StereoPair):
    """
    A stereo pair of calibrated cameras.
 
    Should be initialized with a context manager to ensure that the camera
    connections are closed properly.
    """
    def __init__(self, devices,
                 calibration,
                 stereo_bm_preset=cv2.STEREO_BM_BASIC_PRESET,
                 search_range=0,
                 window_size=5):
        """
        Initialize cameras.
 
        ``devices`` is an iterable of the device numbers. If you want to use the
        ``CalibratedPair`` in offline mode, pass None.
        ``calibration`` is a StereoCalibration object. ``stereo_bm_preset``,
        ``search_range`` and ``window_size`` are parameters for the
        ``block_matcher``.
        """
        if devices:
            super(CalibratedPair, self).__init__(devices)
        #: ``StereoCalibration`` object holding the camera pair's calibration.
        self.calibration = calibration
        self._bm_preset = cv2.STEREO_BM_BASIC_PRESET
        self._search_range = 0
        self._window_size = 5
        #: OpenCV camera type for ``block_matcher``
        self.stereo_bm_preset = stereo_bm_preset
        #: Number of disparities for ``block_matcher``
        self.search_range = search_range
        #: Search window size for ``block_matcher``
        self.window_size = window_size
        #: ``cv2.StereoBM`` object for block matching.
        self.block_matcher = cv2.StereoBM(self.stereo_bm_preset,
                                          self.search_range,
                                          self.window_size)
    def get_frames(self):
        """Rectify and return current frames from cameras."""
        frames = super(CalibratedPair, self).get_frames()
        return self.calibration.rectify(frames)
    def compute_disparity(self, pair):
        """
        Compute disparity from image pair (left, right).
 
        First, convert images to grayscale if needed. Then pass to the
        ``CalibratedPair``'s ``block_matcher`` for stereo matching.
 
        If you wish to visualize the image, remember to normalize it to 0-255.
        """
        gray = []
        if pair[0].ndim == 3:
            for side in pair:
                gray.append(cv2.cvtColor(side, cv2.COLOR_BGR2GRAY))
        else:
            gray = pair
        return self.block_matcher.compute(gray[0], gray[1])
    @property
    def search_range(self):
        """Number of disparities for ``block_matcher``."""
        return self._search_range
    @search_range.setter
    def search_range(self, value):
        """Set ``search_range`` to multiple of 16, replace ``block_matcher``."""
        if value == 0 or not value % 16:
            self._search_range = value
            self.replace_block_matcher()
        else:
            raise InvalidSearchRange("Search range must be a multiple of 16.")
    @property
    def window_size(self):
        """Search window size."""
        return self._window_size
    @window_size.setter
    def window_size(self, value):
        """Set search window size and update ``block_matcher``."""
        if value > 4 and value < 22 and value % 2:
            self._window_size = value
            self.replace_block_matcher()
        else:
            raise InvalidWindowSize("Window size must be an odd number between "
                                    "5 and 21 (inclusive).")
    @property
    def stereo_bm_preset(self):
        """Stereo BM preset used by ``block_matcher``."""
        return self._bm_preset
    @stereo_bm_preset.setter
    def stereo_bm_preset(self, value):
        """Set stereo BM preset and update ``block_matcher``."""
        if value in (cv2.STEREO_BM_BASIC_PRESET,
                     cv2.STEREO_BM_FISH_EYE_PRESET,
                     cv2.STEREO_BM_NARROW_PRESET):
            self._bm_preset = value
            self.replace_block_matcher()
        else:
            raise InvalidBMPreset("Stereo BM preset must be defined as "
                                  "cv2.STEREO_BM_*_PRESET.")
    def replace_block_matcher(self):
        """Replace ``block_matcher`` with current values."""
        self.block_matcher = cv2.StereoBM(preset=self._bm_preset,
                                          ndisparities=self._search_range,
                                          SADWindowSize=self._window_size)
