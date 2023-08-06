"""
create_time: 2023/2/4 15:04
author: TsangHans
"""
from unittest import TestCase
from ddtcv import Wind
import cv2 as cv


class Test(TestCase):
    def test_wind(self):
        x = cv.imread("image/img2.png")
        res = Wind(x)
        assert res == 0.4