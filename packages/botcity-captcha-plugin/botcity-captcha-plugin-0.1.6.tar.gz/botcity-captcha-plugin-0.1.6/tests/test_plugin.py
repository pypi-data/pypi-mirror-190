import os

import deathbycaptcha.deathbycaptcha
import pytest

from botcity.plugins.captcha import BotAntiCaptchaPlugin, BotDeathByCaptchaPlugin
from PIL import Image

cur_dir = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.xfail(reason="Because it is a captcha, it may give an error")
def test_anticaptcha_text(captcha: BotAntiCaptchaPlugin) -> None:
    # AntiCaptcha - Text
    assert captcha.solve_text(os.path.join(cur_dir, "captcha_ms.jpeg"), timeout=30) == '56nn2'
    assert isinstance(captcha.report(), BotAntiCaptchaPlugin)


@pytest.mark.xfail(reason="Because it is a captcha, it may give an error")
def test_anticaptcha_to_image(captcha: BotAntiCaptchaPlugin) -> None:
    image = Image.open(os.path.join(cur_dir, "captcha_ms.jpeg"))
    assert captcha.solve_text(img_or_path=image, timeout=30) == '56nn2'
    assert isinstance(captcha.report(), BotAntiCaptchaPlugin)


@pytest.mark.xfail(reason="Because it is a captcha, it may give an error")
def test_anticaptcha_re(captcha: BotAntiCaptchaPlugin) -> None:
    # AntiCaptcha - Re
    url = 'https://www.google.com/recaptcha/api2/demo'
    site_key = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
    assert captcha.solve_re(url, site_key, timeout=30)
    assert isinstance(captcha.report(), BotAntiCaptchaPlugin)


@pytest.mark.xfail(reason="Because it is a captcha, it may give an error")
def test_anticaptcha_fun(captcha: BotAntiCaptchaPlugin) -> None:
    # AntiCaptcha - Fun
    url = 'https://api.funcaptcha.com/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC'
    site_key = '69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC'
    assert captcha.solve_fun(url, site_key, timeout=30)
    with pytest.raises(NotImplementedError):
        captcha.report()


@pytest.mark.xfail(reason="Because it is a captcha, it may give an error")
def test_deathbycaptcha(death_by_captcha: BotDeathByCaptchaPlugin) -> None:
    # Death By Captcha
    response = death_by_captcha.solve(os.path.join(cur_dir, "captcha_ms.jpeg"), timeout=30)
    assert isinstance(response, str)
    assert response == '56nn2'
    death_by_captcha.report()


@pytest.mark.xfail(reason="Because it is a captcha, it may give an error")
def test_deathbycaptcha_to_image(death_by_captcha: BotDeathByCaptchaPlugin) -> None:
    # Death By Captcha
    image = Image.open(os.path.join(cur_dir, "captcha_ms.jpeg"))
    response = death_by_captcha.solve(image, timeout=30)
    assert isinstance(response, str)
    assert response == '56nn2'
    death_by_captcha.report()


def test_auth_anticaptcha() -> None:
    captcha = BotAntiCaptchaPlugin(api_key="test")
    response = captcha.auth(api_key="test_two")
    assert response.api_key == "test_two"


def test_auth_deathbycaptcha() -> None:

    captcha = BotDeathByCaptchaPlugin(
        username='test',
        password='test'
    )
    response = captcha.auth(username='test', password='test')
    assert isinstance(response._client, deathbycaptcha.deathbycaptcha.SocketClient)
