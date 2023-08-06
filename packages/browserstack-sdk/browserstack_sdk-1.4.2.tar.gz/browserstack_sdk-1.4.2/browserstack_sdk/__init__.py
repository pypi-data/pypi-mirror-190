# coding: UTF-8
import sys
bstack1l1_opy_ = sys.version_info [0] == 2
bstackl_opy_ = 2048
bstack11_opy_ = 7
def bstack1l1l_opy_ (bstack1_opy_):
    global bstack1ll1_opy_
    stringNr = ord (bstack1_opy_ [-1])
    bstack1l_opy_ = bstack1_opy_ [:-1]
    bstack111_opy_ = stringNr % len (bstack1l_opy_)
    bstack11l_opy_ = bstack1l_opy_ [:bstack111_opy_] + bstack1l_opy_ [bstack111_opy_:]
    if bstack1l1_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstackl_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack11l_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstackl_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack11l_opy_)])
    return eval (bstack1lll_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack11ll_opy_ = {
	bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ্ࠬ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࠨৎ"),
  bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ৏"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡱࡥࡺࠩ৐"),
  bstack1l1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ৑"): bstack1l1l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৒"),
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ৓"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪ৔"),
  bstack1l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ৕"): bstack1l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹ࠭৖"),
  bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩৗ"): bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭৘"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭৙"): bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ৚"),
  bstack1l1l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩ৛"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨࠩড়"),
  bstack1l1l_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪঢ়"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡵࡲࡰࡪ࠭৞"),
  bstack1l1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬয়"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬৠ"),
  bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ৡ"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭ৢ"),
  bstack1l1l_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪৣ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡻ࡯ࡤࡦࡱࠪ৤"),
  bstack1l1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ৥"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡍࡱࡪࡷࠬ০"),
  bstack1l1l_opy_ (u"ࠨࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨ১"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡰࡪࡳࡥࡵࡴࡼࡐࡴ࡭ࡳࠨ২"),
  bstack1l1l_opy_ (u"ࠪ࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨ৩"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡵࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨ৪"),
  bstack1l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ৫"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡩ࡮ࡧࡽࡳࡳ࡫ࠧ৬"),
  bstack1l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ৭"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ৮"),
  bstack1l1l_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ৯"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨৰ"),
  bstack1l1l_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩৱ"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩ৲"),
  bstack1l1l_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭৳"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭৴"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪ৵"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡲࡩࡑࡥࡺࡵࠪ৶"),
  bstack1l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬ৷"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯ࡘࡣ࡬ࡸࠬ৸"),
  bstack1l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫ৹"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡶࠫ৺"),
  bstack1l1l_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨ৻"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡨࡦࡥࡨ࡮ࡥࠨৼ"),
  bstack1l1l_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪ৽"): bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪ৾"),
  bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ৿"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ਀"),
  bstack1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪਁ"): bstack1l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧਂ"),
  bstack1l1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬਃ"): bstack1l1l_opy_ (u"ࠩࡵࡩࡦࡲ࡟࡮ࡱࡥ࡭ࡱ࡫ࠧ਄"),
  bstack1l1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪਅ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫਆ"),
  bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬਇ"): bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬਈ"),
  bstack1l1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨਉ"): bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨਊ"),
  bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨ਋"): bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫ਌"),
  bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਍"): bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਎"),
  bstack1l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ਏ"): bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡰࡷࡵࡧࡪ࠭ਐ"),
  bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਑"): bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਒"),
  bstack1l1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬਓ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡏࡣࡰࡩࠬਔ"),
}
bstack11l11_opy_ = [
  bstack1l1l_opy_ (u"ࠬࡵࡳࠨਕ"),
  bstack1l1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩਖ"),
  bstack1l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩਗ"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਘ"),
  bstack1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ਙ"),
  bstack1l1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧਚ"),
  bstack1l1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫਛ"),
]
bstack1ll1ll_opy_ = {
  bstack1l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨਜ"): bstack1l1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪਝ"),
  bstack1l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩਞ"): [bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪਟ"), bstack1l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬਠ")],
  bstack1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਡ"): bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩਢ"),
  bstack1l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩਣ"): bstack1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ਤ"),
  bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬਥ"): [bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩਦ"), bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨਧ")],
  bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਨ"): bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭਩"),
  bstack1l1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩਪ"): bstack1l1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫਫ"),
  bstack1l1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧਬ"): [bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਭ"), bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪਮ")],
  bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩਯ"): [bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬਰ"), bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬ਱")]
}
bstack1l111_opy_ = [
  bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬਲ"),
  bstack1l1l_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪਲ਼"),
  bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ਴"),
  bstack1l1l_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩਵ"),
  bstack1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬਸ਼"),
  bstack1l1l_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩ਷"),
  bstack1l1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨਸ"),
  bstack1l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫਹ"),
  bstack1l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ਺"),
  bstack1l1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ਻"),
  bstack1l1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ਼"),
  bstack1l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ਽"),
]
bstack1llll1_opy_ = [
  bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨਾ"),
  bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩਿ"),
  bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬੀ"),
  bstack1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧੁ"),
  bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫੂ"),
  bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ੃"),
  bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭੄"),
  bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ੅"),
  bstack1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ੆"),
]
bstack11111_opy_ = [
  bstack1l1l_opy_ (u"࠭ࡵࡱ࡮ࡲࡥࡩࡓࡥࡥ࡫ࡤࠫੇ"),
  bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩੈ"),
  bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ੉"),
  bstack1l1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ੊"),
  bstack1l1l_opy_ (u"ࠪࡸࡪࡹࡴࡑࡴ࡬ࡳࡷ࡯ࡴࡺࠩੋ"),
  bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧੌ"),
  bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡦ࡭੍ࠧ"),
  bstack1l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ੎"),
  bstack1l1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ੏"),
  bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭੐"),
  bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪੑ"),
  bstack1l1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩ੒"),
  bstack1l1l_opy_ (u"ࠫࡴࡹࠧ੓"),
  bstack1l1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ੔"),
  bstack1l1l_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬ੕"),
  bstack1l1l_opy_ (u"ࠧࡢࡷࡷࡳ࡜ࡧࡩࡵࠩ੖"),
  bstack1l1l_opy_ (u"ࠨࡴࡨ࡫࡮ࡵ࡮ࠨ੗"),
  bstack1l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡺࡰࡰࡨࠫ੘"),
  bstack1l1l_opy_ (u"ࠪࡱࡦࡩࡨࡪࡰࡨࠫਖ਼"),
  bstack1l1l_opy_ (u"ࠫࡷ࡫ࡳࡰ࡮ࡸࡸ࡮ࡵ࡮ࠨਗ਼"),
  bstack1l1l_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪਜ਼"),
  bstack1l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡕࡲࡪࡧࡱࡸࡦࡺࡩࡰࡰࠪੜ"),
  bstack1l1l_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࠭੝"),
  bstack1l1l_opy_ (u"ࠨࡰࡲࡔࡦ࡭ࡥࡍࡱࡤࡨ࡙࡯࡭ࡦࡱࡸࡸࠬਫ਼"),
  bstack1l1l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ੟"),
  bstack1l1l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩ੠"),
  bstack1l1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ੡"),
  bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭੢"),
  bstack1l1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪ੣"),
  bstack1l1l_opy_ (u"ࠧ࡯ࡱࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠫ੤"),
  bstack1l1l_opy_ (u"ࠨࡥ࡫ࡩࡨࡱࡕࡓࡎࠪ੥"),
  bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੦"),
  bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡆࡳࡴࡱࡩࡦࡵࠪ੧"),
  bstack1l1l_opy_ (u"ࠫࡨࡧࡰࡵࡷࡵࡩࡈࡸࡡࡴࡪࠪ੨"),
  bstack1l1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ੩"),
  bstack1l1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭੪"),
  bstack1l1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࡚ࡪࡸࡳࡪࡱࡱࠫ੫"),
  bstack1l1l_opy_ (u"ࠨࡰࡲࡆࡱࡧ࡮࡬ࡒࡲࡰࡱ࡯࡮ࡨࠩ੬"),
  bstack1l1l_opy_ (u"ࠩࡰࡥࡸࡱࡓࡦࡰࡧࡏࡪࡿࡳࠨ੭"),
  bstack1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡏࡳ࡬ࡹࠧ੮"),
  bstack1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡍࡩ࠭੯"),
  bstack1l1l_opy_ (u"ࠬࡪࡥࡥ࡫ࡦࡥࡹ࡫ࡤࡅࡧࡹ࡭ࡨ࡫ࠧੰ"),
  bstack1l1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡖࡡࡳࡣࡰࡷࠬੱ"),
  bstack1l1l_opy_ (u"ࠧࡱࡪࡲࡲࡪࡔࡵ࡮ࡤࡨࡶࠬੲ"),
  bstack1l1l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ੳ"),
  bstack1l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡏࡱࡶ࡬ࡳࡳࡹࠧੴ"),
  bstack1l1l_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨੵ"),
  bstack1l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ੶"),
  bstack1l1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱࡑࡵࡧࡴࠩ੷"),
  bstack1l1l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡈࡩࡰ࡯ࡨࡸࡷ࡯ࡣࠨ੸"),
  bstack1l1l_opy_ (u"ࠧࡷ࡫ࡧࡩࡴ࡜࠲ࠨ੹"),
  bstack1l1l_opy_ (u"ࠨ࡯࡬ࡨࡘ࡫ࡳࡴ࡫ࡲࡲࡎࡴࡳࡵࡣ࡯ࡰࡆࡶࡰࡴࠩ੺"),
  bstack1l1l_opy_ (u"ࠩࡨࡷࡵࡸࡥࡴࡵࡲࡗࡪࡸࡶࡦࡴࠪ੻"),
  bstack1l1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡑࡵࡧࡴࠩ੼"),
  bstack1l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡉࡤࡱࠩ੽"),
  bstack1l1l_opy_ (u"ࠬࡺࡥ࡭ࡧࡰࡩࡹࡸࡹࡍࡱࡪࡷࠬ੾"),
  bstack1l1l_opy_ (u"࠭ࡳࡺࡰࡦࡘ࡮ࡳࡥࡘ࡫ࡷ࡬ࡓ࡚ࡐࠨ੿"),
  bstack1l1l_opy_ (u"ࠧࡨࡧࡲࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ઀"),
  bstack1l1l_opy_ (u"ࠨࡩࡳࡷࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ઁ"),
  bstack1l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪં"),
  bstack1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪઃ"),
  bstack1l1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࡆ࡬ࡦࡴࡧࡦࡌࡤࡶࠬ઄"),
  bstack1l1l_opy_ (u"ࠬࡾ࡭ࡴࡌࡤࡶࠬઅ"),
  bstack1l1l_opy_ (u"࠭ࡸ࡮ࡺࡍࡥࡷ࠭આ"),
  bstack1l1l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭ઇ"),
  bstack1l1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨઈ"),
  bstack1l1l_opy_ (u"ࠩࡺࡷࡑࡵࡣࡢ࡮ࡖࡹࡵࡶ࡯ࡳࡶࠪઉ"),
  bstack1l1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ઊ"),
  bstack1l1l_opy_ (u"ࠫࡦࡶࡰࡗࡧࡵࡷ࡮ࡵ࡮ࠨઋ"),
  bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫઌ"),
  bstack1l1l_opy_ (u"࠭ࡲࡦࡵ࡬࡫ࡳࡇࡰࡱࠩઍ"),
  bstack1l1l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡰ࡬ࡱࡦࡺࡩࡰࡰࡶࠫ઎"),
  bstack1l1l_opy_ (u"ࠨࡥࡤࡲࡦࡸࡹࠨએ"),
  bstack1l1l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪઐ"),
  bstack1l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪઑ"),
  bstack1l1l_opy_ (u"ࠫ࡮࡫ࠧ઒"),
  bstack1l1l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪઓ"),
  bstack1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ઔ"),
  bstack1l1l_opy_ (u"ࠧࡲࡷࡨࡹࡪ࠭ક"),
  bstack1l1l_opy_ (u"ࠨ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪખ"),
  bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࡙ࡴࡰࡴࡨࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠪગ"),
  bstack1l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡆࡥࡲ࡫ࡲࡢࡋࡰࡥ࡬࡫ࡉ࡯࡬ࡨࡧࡹ࡯࡯࡯ࠩઘ"),
  bstack1l1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡇࡻࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧઙ"),
  bstack1l1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡌࡲࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨચ"),
  bstack1l1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࠪછ"),
  bstack1l1l_opy_ (u"ࠧࡳࡧࡶࡩࡷࡼࡥࡅࡧࡹ࡭ࡨ࡫ࠧજ"),
  bstack1l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨઝ"),
  bstack1l1l_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫઞ"),
  bstack1l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡥࡸࡹࡣࡰࡦࡨࠫટ"),
  bstack1l1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫઠ"),
  bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ડ"),
  bstack1l1l_opy_ (u"࠭ࡷࡥ࡫ࡲࡗࡪࡸࡶࡪࡥࡨࠫઢ"),
  bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩણ"),
  bstack1l1l_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵࡅࡵࡳࡸࡹࡓࡪࡶࡨࡘࡷࡧࡣ࡬࡫ࡱ࡫ࠬત"),
  bstack1l1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡒࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࡸ࠭થ"),
  bstack1l1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭દ"),
  bstack1l1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡸࡨࡍࡔ࡙ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࡐࡴࡩࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩધ"),
  bstack1l1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧન"),
  bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ઩")
]
bstack1llll_opy_ = {
  bstack1l1l_opy_ (u"ࠧࡷࠩપ"): bstack1l1l_opy_ (u"ࠨࡸࠪફ"),
  bstack1l1l_opy_ (u"ࠩࡩࠫબ"): bstack1l1l_opy_ (u"ࠪࡪࠬભ"),
  bstack1l1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪમ"): bstack1l1l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫય"),
  bstack1l1l_opy_ (u"࠭࡯࡯࡮ࡼࡥࡺࡺ࡯࡮ࡣࡷࡩࠬર"): bstack1l1l_opy_ (u"ࠧࡰࡰ࡯ࡽࡆࡻࡴࡰ࡯ࡤࡸࡪ࠭઱"),
  bstack1l1l_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬલ"): bstack1l1l_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭ળ"),
  bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭઴"): bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧવ"),
  bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨશ"): bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩષ"),
  bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪસ"): bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫહ"),
  bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬ઺"): bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭઻"),
  bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡩࡱࡶࡸ઼ࠬ"): bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡊࡲࡷࡹ࠭ઽ"),
  bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧા"): bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨિ"),
  bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩી"): bstack1l1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫુ"),
  bstack1l1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬૂ"): bstack1l1l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ૃ"),
  bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ૄ"): bstack1l1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨૅ"),
  bstack1l1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩ૆"): bstack1l1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪે"),
  bstack1l1l_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ૈ"): bstack1l1l_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧૉ"),
  bstack1l1l_opy_ (u"ࠫࡵࡧࡣࡧ࡫࡯ࡩࠬ૊"): bstack1l1l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨો"),
  bstack1l1l_opy_ (u"࠭ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨૌ"): bstack1l1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧ્ࠪ"),
  bstack1l1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ૎"): bstack1l1l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ૏"),
  bstack1l1l_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫૐ"): bstack1l1l_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬ૑"),
  bstack1l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૒"): bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૓"),
}
bstack1lll11_opy_ = bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡹࡧ࠳࡭ࡻࡢࠨ૔")
bstack111l_opy_ = bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠫ૕")
bstack1l1l1_opy_ = {
  bstack1l1l_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫ૖"): 50,
  bstack1l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ૗"): 40,
  bstack1l1l_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬ૘"): 30,
  bstack1l1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ૙"): 20,
  bstack1l1l_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ૚"): 10
}
DEFAULT_LOG_LEVEL = bstack1l1l1_opy_[bstack1l1l_opy_ (u"ࠧࡪࡰࡩࡳࠬ૛")]
bstack1111l_opy_ = bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧ૜")
bstack11l1_opy_ = bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧ૝")
bstack11l1l_opy_ = bstack1l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩ૞")
bstack1ll11_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪ૟")
bstack1lll1l_opy_ = [bstack1l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ૠ"), bstack1l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ૡ")]
bstack1ll1l_opy_ = [bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪૢ"), bstack1l1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪૣ")]
bstack1111_opy_ = [
  bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪ૤"),
  bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૥"),
  bstack1l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ૦"),
  bstack1l1l_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩ૧"),
  bstack1l1l_opy_ (u"࠭ࡡࡱࡲࠪ૨"),
  bstack1l1l_opy_ (u"ࠧࡶࡦ࡬ࡨࠬ૩"),
  bstack1l1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ૪"),
  bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩ૫"),
  bstack1l1l_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨ૬"),
  bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩ૭"),
  bstack1l1l_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭૮"), bstack1l1l_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩ૯"),
  bstack1l1l_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪ૰"),
  bstack1l1l_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧ૱"),
  bstack1l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭૲"),
  bstack1l1l_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭૳"),
  bstack1l1l_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ૴"),
  bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ૵"), bstack1l1l_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ૶"), bstack1l1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ૷"), bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ૸"), bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫૹ"),
  bstack1l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨૺ"),
  bstack1l1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨૻ"),
  bstack1l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧૼ"), bstack1l1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ૽"),
  bstack1l1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ૾"),
  bstack1l1l_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ૿"),
  bstack1l1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨ଀"),
  bstack1l1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫଁ"),
  bstack1l1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩଂ"),
  bstack1l1l_opy_ (u"ࠬࡧࡶࡥࠩଃ"), bstack1l1l_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩ଄"), bstack1l1l_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩଅ"), bstack1l1l_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩଆ"),
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧଇ"), bstack1l1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩଈ"), bstack1l1l_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧଉ"),
  bstack1l1l_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧଊ"), bstack1l1l_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫଋ"),
  bstack1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩଌ"), bstack1l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫ଍"), bstack1l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧ଎"), bstack1l1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬଏ"), bstack1l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨଐ"),
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨ଑"), bstack1l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪ଒"),
  bstack1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩଓ"),
  bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ଔ"),
  bstack1l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨକ"), bstack1l1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫଖ"), bstack1l1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩଗ"), bstack1l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨଘ"),
  bstack1l1l_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫଙ"),
  bstack1l1l_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩଚ"), bstack1l1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨଛ"),
  bstack1l1l_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩଜ"),
  bstack1l1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬଝ"),
  bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭ଞ"),
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬଟ"),
  bstack1l1l_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧଠ"),
  bstack1l1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ଡ"),
  bstack1l1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩଢ"),
  bstack1l1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨଣ"),
  bstack1l1l_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧତ"),
  bstack1l1l_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨଥ"),
  bstack1l1l_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ଦ"),
  bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬଧ"),
  bstack1l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫନ"),
  bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨ଩"),
  bstack1l1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧପ"),
  bstack1l1l_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧଫ"),
  bstack1l1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫବ"),
  bstack1l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩଭ"), bstack1l1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪମ"), bstack1l1l_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪଯ"),
  bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬର"),
  bstack1l1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭଱"),
  bstack1l1l_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬଲ"),
  bstack1l1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ଳ"),
  bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ଴"),
  bstack1l1l_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪଵ"),
  bstack1l1l_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪଶ"), bstack1l1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧଷ"), bstack1l1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬସ"),
  bstack1l1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪହ"),
  bstack1l1l_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬ଺"),
  bstack1l1l_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧ଻"),
  bstack1l1l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ଼࠭"),
  bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪଽ"), bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧା"),
  bstack1l1l_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬି"), bstack1l1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧୀ"),
  bstack1l1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫୁ"),
  bstack1l1l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫୂ"),
  bstack1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩୃ"), bstack1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫୄ"), bstack1l1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬ୅"), bstack1l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩ୆"),
  bstack1l1l_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪେ"),
  bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬୈ"),
  bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ୉"),
  bstack1l1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭୊"),
  bstack1l1l_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪࠫୋ"),
  bstack1l1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪୌ"),
  bstack1l1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶ୍ࠪ"), bstack1l1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫ୎"),
  bstack1l1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧ୏"),
  bstack1l1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬ୐"),
  bstack1l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧ୑"),
  bstack1l1l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ୒"),
  bstack1l1l_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪ୓"),
  bstack1l1l_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ୔"),
  bstack1l1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ୕"),
  bstack1l1l_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬୖ"),
  bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬୗ"),
  bstack1l1l_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ୘"),
  bstack1l1l_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ୙"),
  bstack1l1l_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧ୚"),
  bstack1l1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨ୛"),
  bstack1l1l_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩࠬଡ଼"),
  bstack1l1l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ଢ଼"),
  bstack1l1l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ୞"),
  bstack1l1l_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧୟ"),
  bstack1l1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨୠ"),
  bstack1l1l_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬୡ"),
  bstack1l1l_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨୢ"),
  bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭ୣ"),
  bstack1l1l_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ୤"), bstack1l1l_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ୥"),
  bstack1l1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪ୦"), bstack1l1l_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ୧"),
  bstack1l1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭୨"),
  bstack1l1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ୩"),
  bstack1l1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ୪"),
  bstack1l1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨ୫"), bstack1l1l_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨ୬"),
  bstack1l1l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ୭"),
  bstack1l1l_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬ୮"),
  bstack1l1l_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨ୯"),
  bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪ୰"),
  bstack1l1l_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬୱ"),
  bstack1l1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧ୲"),
  bstack1l1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ୳"),
  bstack1l1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ୴"),
  bstack1l1l_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ୵"),
  bstack1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ୶"), bstack1l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭୷"),
  bstack1l1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ୸")
]
bstack11lll_opy_ = bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ୹")
bstack11ll1_opy_ = [bstack1l1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ୺"), bstack1l1l_opy_ (u"࠭࠮ࡢࡣࡥࠫ୻"), bstack1l1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ୼")]
bstack111l1_opy_ = [bstack1l1l_opy_ (u"ࠨ࡫ࡧࠫ୽"), bstack1l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ୾"), bstack1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭୿"), bstack1l1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪ஀")]
bstack1lll1_opy_ = {
  bstack1l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ஁"): bstack1l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫஂ"),
  bstack1l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨஃ"): bstack1l1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭஄"),
  bstack1l1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧஅ"): bstack1l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫஆ"),
  bstack1l1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧஇ"): bstack1l1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫஈ"),
  bstack1l1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭உ"): bstack1l1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨஊ")
}
bstack1l11_opy_ = [
  bstack1l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭஋"),
  bstack1l1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ஌"),
  bstack1l1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ஍"),
  bstack1l1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪஎ"),
  bstack1l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ஏ"),
]
bstack1lllll_opy_ = bstack1llll1_opy_ + bstack11111_opy_ + bstack1111_opy_
bstack111ll_opy_ = [
  bstack1l1l_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫஐ"),
  bstack1l1l_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨ஑"),
  bstack1l1l_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧஒ"),
  bstack1l1l_opy_ (u"ࠩࡡ࠵࠵࠴ࠧஓ"),
  bstack1l1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩஔ"),
  bstack1l1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪக"),
  bstack1l1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫ஖"),
  bstack1l1l_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩ஗")
]
bstack1l11l_opy_ = bstack1l1l_opy_ (u"ࠧ࠵࠰࠳࠲࠵࠭஘")
bstack11l1111l_opy_ = bstack1l1l_opy_ (u"ࠨࡕࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠭ࠢࡸࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠾ࠥࢁࡽࠨங")
bstack1l1111ll_opy_ = bstack1l1l_opy_ (u"ࠩࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡹࡥࡵࡷࡳࠥࠬச")
bstack1lll1l1ll_opy_ = bstack1l1l_opy_ (u"ࠪࡔࡦࡸࡳࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬ஛")
bstack1ll11ll1_opy_ = bstack1l1l_opy_ (u"ࠫࡘࡧ࡮ࡪࡶ࡬ࡾࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩஜ")
bstack1lll1lll_opy_ = bstack1l1l_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤ࡭ࡻࡢࠡࡷࡵࡰ࠿ࠦࡻࡾࠩ஝")
bstack1llll111l_opy_ = bstack1l1l_opy_ (u"࠭ࡓࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࡿࢂ࠭ஞ")
bstack111111_opy_ = bstack1l1l_opy_ (u"ࠧࡓࡧࡦࡩ࡮ࡼࡥࡥࠢ࡬ࡲࡹ࡫ࡲࡳࡷࡳࡸ࠱ࠦࡥࡹ࡫ࡷ࡭ࡳ࡭ࠧட")
bstack11l11l_opy_ = bstack1l1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭஠")
bstack11l1l1_opy_ = bstack1l1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧ஡")
bstack1l11lll_opy_ = bstack1l1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶ࠯ࠤࡵࡧࡢࡰࡶࠣࡥࡳࡪࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧࡶࠤࡹࡵࠠࡳࡷࡱࠤࡷࡵࡢࡰࡶࠣࡸࡪࡹࡴࡴࠢ࡬ࡲࠥࡶࡡࡳࡣ࡯ࡰࡪࡲ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡳࡥࡧࡵࡴࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬ஢")
bstack1l1l11ll_opy_ = bstack1l1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡨࡥࡩࡣࡹࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࡤࠬண")
bstack1ll11lll1_opy_ = bstack1l1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡡࡱࡲ࡬ࡹࡲ࠳ࡣ࡭࡫ࡨࡲࡹࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡇࡰࡱ࡫ࡸࡱ࠲ࡖࡹࡵࡪࡲࡲ࠲ࡉ࡬ࡪࡧࡱࡸࡥ࠭த")
bstack1lll1l1l1_opy_ = bstack1l1l_opy_ (u"࠭ࡈࡢࡰࡧࡰ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡰࡴࡹࡥࠨ஥")
bstack11l1lll_opy_ = bstack1l1l_opy_ (u"ࠧࡂ࡮࡯ࠤࡩࡵ࡮ࡦࠣࠪ஦")
bstack1lll11111_opy_ = bstack1l1l_opy_ (u"ࠨࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࠠࡢࡶࠣࠦࢀࢃࠢ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡨࡲࡵࡥࡧࠣࡥࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡨ࡬ࡰࡪࠦࡣࡰࡰࡷࡥ࡮ࡴࡩࡨࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡴࡦࡵࡷࡷ࠳࠭஧")
bstack1l1lll1l_opy_ = bstack1l1l_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦ࡮ࡰࡶࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡸ࡭࡫࡭ࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡧࡳࠡࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦࠥࡧ࡮ࡥࠢࠥࡥࡨࡩࡥࡴࡵࡎࡩࡾࠨࠠࡰࡴࠣࡷࡪࡺࠠࡵࡪࡨࡱࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠼ࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧࠦࡡ࡯ࡦࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠢࠨந")
bstack1lllll1l_opy_ = bstack1l1l_opy_ (u"ࠪࡑࡦࡲࡦࡰࡴࡰࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠧࢁࡽࠣࠩன")
bstack1llll11ll_opy_ = bstack1l1l_opy_ (u"ࠫࡊࡴࡣࡰࡷࡱࡸࡪࡸࡥࡥࠢࡨࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࠲ࠦࡻࡾࠩப")
bstack1l11l11l_opy_ = bstack1l1l_opy_ (u"࡙ࠬࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠬ஫")
bstack1lllllll_opy_ = bstack1l1l_opy_ (u"࠭ࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭஬")
bstack11ll111l_opy_ = bstack1l1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠥ࡯ࡳࠡࡰࡲࡻࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠧࠧ஭")
bstack1l111l1l_opy_ = bstack1l1l_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬࠻ࠢࡾࢁࠬம")
bstack111l111l_opy_ = bstack1l1l_opy_ (u"ࠩࡖࡸࡦࡸࡴࡪࡰࡪࠤࡱࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡻ࡮ࡺࡨࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࡿࢂ࠭ய")
bstack1l11l11_opy_ = bstack1l1l_opy_ (u"࡙ࠪࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫர")
bstack1ll1ll1l_opy_ = bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠪற")
bstack1l1lll11_opy_ = bstack1l1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࠦࡡ࡯ࠢࡤࡴࡵࡸ࡯ࡱࡴ࡬ࡥࡹ࡫ࠠࡇ࡙ࠣࠬࡷࡵࡢࡰࡶ࠲ࡴࡦࡨ࡯ࡵࠫࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠰ࠥࡹ࡫ࡪࡲࠣࡸ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡯ࡪࡿࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩࠣ࡭࡫ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡴ࡫ࡰࡴࡱ࡫ࠠࡱࡻࡷ࡬ࡴࡴࠠࡴࡥࡵ࡭ࡵࡺࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡣࡱࡽࠥࡌࡗ࠯ࠩல")
bstack11lll1ll_opy_ = bstack1l1l_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡩࡶࡷࡴࡕࡸ࡯ࡹࡻ࠲࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠠࡪࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡣࡶࡴࡵࡩࡳࡺ࡬ࡺࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࠭ࢁࡽࠪ࠮ࠣࡴࡱ࡫ࡡࡴࡧࠣࡹࡵ࡭ࡲࡢࡦࡨࠤࡹࡵࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡀࡀ࠸࠳࠶࠮࠱ࠢࡲࡶࠥࡸࡥࡧࡧࡵࠤࡹࡵࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡰࡪࡴࡩࡶ࡯࠲ࡶࡺࡴ࠭ࡵࡧࡶࡸࡸ࠳ࡢࡦࡪ࡬ࡲࡩ࠳ࡰࡳࡱࡻࡽࠨࡶࡹࡵࡪࡲࡲࠥ࡬࡯ࡳࠢࡤࠤࡼࡵࡲ࡬ࡣࡵࡳࡺࡴࡤ࠯ࠩள")
bstack11ll1l_opy_ = bstack1l1l_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡽࡲࡲࠠࡧ࡫࡯ࡩ࠳࠴ࠧழ")
bstack1l11ll1l_opy_ = bstack1l1l_opy_ (u"ࠨࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡨࡧࡱࡩࡷࡧࡴࡦࡦࠣࡸ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠦ࠭வ")
bstack11l111_opy_ = bstack1l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥ࠯ࠢࡾࢁࠬஶ")
bstack111l11_opy_ = bstack1l1l_opy_ (u"ࠪࡉࡽࡶࡥࡤࡶࡨࡨࠥࡧࡴࠡ࡮ࡨࡥࡸࡺࠠ࠲ࠢ࡬ࡲࡵࡻࡴ࠭ࠢࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࠵࠭ஷ")
bstack1l1l1ll1_opy_ = bstack1l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡺࡸࡩ࡯ࡩࠣࡅࡵࡶࠠࡶࡲ࡯ࡳࡦࡪ࠮ࠡࡽࢀࠫஸ")
bstack1lll1111_opy_ = bstack1l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡃࡳࡴ࠳ࠦࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࢁࡽ࠯ࠩஹ")
bstack1llll111_opy_ = bstack1l1l_opy_ (u"࠭ࡋࡦࡻࡶࠤࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࠭ࡦࡺ࡬ࡷࡹࠦࡡࡴࠢࡤࡴࡵࠦࡶࡢ࡮ࡸࡩࡸ࠲ࠠࡶࡵࡨࠤࡦࡴࡹࠡࡱࡱࡩࠥࡶࡲࡰࡲࡨࡶࡹࡿࠠࡧࡴࡲࡱࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠯ࠤࡴࡴ࡬ࡺࠢࠥࡴࡦࡺࡨࠣࠢࡤࡲࡩࠦࠢࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠥࠤࡨࡧ࡮ࠡࡥࡲ࠱ࡪࡾࡩࡴࡶࠣࡸࡴ࡭ࡥࡵࡪࡨࡶ࠳࠭஺")
bstack11llll11_opy_ = bstack1l1l_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠢࡤࡶࡪࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩ஻")
bstack111l11ll_opy_ = bstack1l1l_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡗࡺࡶࡰࡰࡴࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࡸࠦ࡯ࡧࠢࡤࡴࡵࠦࡡࡳࡧࠣࡳ࡫ࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩ஼")
bstack11l11l11_opy_ = bstack1l1l_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡵࡶࠠࡪࡦࠣࡿࢂࠦࡦࡰࡴࠣ࡬ࡦࡹࡨࠡ࠼ࠣࡿࢂ࠴ࠧ஽")
bstack11ll1ll1_opy_ = bstack1l1l_opy_ (u"ࠪࡅࡵࡶࠠࡖࡲ࡯ࡳࡦࡪࡥࡥࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠢࡌࡈࠥࡀࠠࡼࡿࠪா")
bstack11ll11l1_opy_ = bstack1l1l_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣࡅࡵࡶࠠ࠻ࠢࡾࢁ࠳࠭ி")
bstack1lll1l1l_opy_ = bstack1l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡲࡶࠥࡼࡡ࡯࡫࡯ࡰࡦࠦࡰࡺࡶ࡫ࡳࡳࠦࡴࡦࡵࡷࡷ࠱ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶࡡࡳࡣ࡯ࡰࡪࡲࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤࡂࠦ࠱ࠨீ")
bstack11lllll_opy_ = bstack1l1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࠿ࠦࡻࡾࠩு")
bstack1l1ll1l1_opy_ = bstack1l1l_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴ࠽ࠤࢀࢃࠧூ")
bstack1llllll_opy_ = bstack1l1l_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤ࡬࡫ࡴࠡࡴࡨࡥࡸࡵ࡮ࠡࡨࡲࡶࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫࠮ࠡࡽࢀࠫ௃")
bstack1lllllll1_opy_ = bstack1l1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡣࡳ࡭ࠥࡩࡡ࡭࡮࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ௄")
bstack1l1lll_opy_ = bstack1l1l_opy_ (u"࡙ࠪࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡩࡱࡺࠤࡧࡻࡩ࡭ࡦ࡙ࠣࡗࡒࠬࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠࡪࡵࠣࡲࡴࡺࠠࡶࡵࡨࡨ࠳࠭௅")
bstack1ll11lll_opy_ = bstack1l1l_opy_ (u"ࠫࡘ࡫ࡲࡷࡧࡵࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡥࡲ࡫ࠠࡢࡵࠣࡧࡱ࡯ࡥ࡯ࡶࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠨெ")
bstack111l1l_opy_ = bstack1l1l_opy_ (u"ࠬ࡜ࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡲࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠺ࠡࡽࢀࠫே")
bstack111llll_opy_ = bstack1l1l_opy_ (u"࠭ࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡤࡧࡨ࡫ࡳࡴࠢࡤࠤࡵࡸࡩࡷࡣࡷࡩࠥࡪ࡯࡮ࡣ࡬ࡲ࠿ࠦࡻࡾࠢ࠱ࠤࡘ࡫ࡴࠡࡶ࡫ࡩࠥ࡬࡯࡭࡮ࡲࡻ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠤࡡࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯࠾ࠥࡺࡲࡶࡧࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠪை")
bstack1ll111_opy_ = bstack1l1l_opy_ (u"ࠧࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡪࡩࡹࡥ࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࡣࡪࡸࡲࡰࡴࠣ࠾ࠥࢁࡽࠨ௉")
bstack1l1llll1_opy_ = bstack1l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠࡱࡴࡲࡼࡾࠦࡳࡦࡶࡷ࡭ࡳ࡭ࡳ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬொ")
from ._version import __version__
bstack1lll1ll1l_opy_ = None
CONFIG = {}
bstack11ll1l11_opy_ = None
bstack1llll1l11_opy_ = None
bstack1lllll1_opy_ = None
bstack1l1lll1_opy_ = -1
bstack11l11lll_opy_ = DEFAULT_LOG_LEVEL
bstack1l1l1l_opy_ = 1
bstack11lll11_opy_ = False
bstack111l1ll_opy_ = bstack1l1l_opy_ (u"ࠩࠪோ")
bstack1l1111_opy_ = bstack1l1l_opy_ (u"ࠪࠫௌ")
bstack11llll_opy_ = False
bstack1ll11l_opy_ = None
bstack11l111ll_opy_ = None
bstack1lll11ll1_opy_ = None
bstack1ll1l1l1l_opy_ = None
bstack1111l11_opy_ = None
bstack1111ll1_opy_ = None
bstack111111ll_opy_ = None
bstack1lll1lll1_opy_ = None
bstack111lllll_opy_ = None
bstack1lll111l_opy_ = None
bstack1ll1l1l1_opy_ = None
bstack1l11ll11_opy_ = bstack1l1l_opy_ (u"்ࠦࠧ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l11lll_opy_,
                    format=bstack1l1l_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪ௎"),
                    datefmt=bstack1l1l_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ௏"))
def bstack1ll1lll11_opy_():
  global CONFIG
  global bstack11l11lll_opy_
  if bstack1l1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩௐ") in CONFIG:
    bstack11l11lll_opy_ = bstack1l1l1_opy_[CONFIG[bstack1l1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ௑")]]
    logging.getLogger().setLevel(bstack11l11lll_opy_)
def bstack1llll1ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11111ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1lll1l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡤࡱࡱࡪ࡮࡭ࡦࡪ࡮ࡨࠦ௒") in args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll11l_opy_
      bstack1ll11l_opy_ = path
      return path
  return None
def bstack11l1lll1_opy_():
  bstack1ll1ll1_opy_ = bstack1ll1lll1l_opy_()
  if bstack1ll1ll1_opy_ and os.path.exists(os.path.abspath(bstack1ll1ll1_opy_)):
    fileName = bstack1ll1ll1_opy_
  if bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧ௓") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ௔")])) and not bstack1l1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧ௕") in locals():
    fileName = os.environ[bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ௖")]
  if not bstack1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩௗ") in locals():
    fileName = bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ௘")
  bstack1111l1l_opy_ = os.path.abspath(fileName)
  if not os.path.exists(bstack1111l1l_opy_):
    fileName = bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭௙")
    bstack1111l1l_opy_ = os.path.abspath(fileName)
    if not os.path.exists(bstack1111l1l_opy_):
      bstack1llllll1_opy_(
        bstack1lll11111_opy_.format(os.getcwd()))
  with open(bstack1111l1l_opy_, bstack1l1l_opy_ (u"ࠪࡶࠬ௚")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1llllll1_opy_(bstack1lllll1l_opy_.format(str(exc)))
def bstack1l1ll11l_opy_(config):
  bstack1lll11l1l_opy_ = bstack1l1ll1l_opy_(config)
  for option in list(bstack1lll11l1l_opy_):
    if option.lower() in bstack1llll_opy_ and option != bstack1llll_opy_[option.lower()]:
      bstack1lll11l1l_opy_[bstack1llll_opy_[option.lower()]] = bstack1lll11l1l_opy_[option]
      del bstack1lll11l1l_opy_[option]
  return config
def bstack11111lll_opy_(config):
  bstack1l11l1_opy_ = config.keys()
  for bstack11l1l11l_opy_, bstack1l1l1ll_opy_ in bstack11ll_opy_.items():
    if bstack1l1l1ll_opy_ in bstack1l11l1_opy_:
      config[bstack11l1l11l_opy_] = config[bstack1l1l1ll_opy_]
      del config[bstack1l1l1ll_opy_]
  for bstack11l1l11l_opy_, bstack1l1l1ll_opy_ in bstack1ll1ll_opy_.items():
    if isinstance(bstack1l1l1ll_opy_, list):
      for bstack1lllll11l_opy_ in bstack1l1l1ll_opy_:
        if bstack1lllll11l_opy_ in bstack1l11l1_opy_:
          config[bstack11l1l11l_opy_] = config[bstack1lllll11l_opy_]
          del config[bstack1lllll11l_opy_]
          break
    elif bstack1l1l1ll_opy_ in bstack1l11l1_opy_:
        config[bstack11l1l11l_opy_] = config[bstack1l1l1ll_opy_]
        del config[bstack1l1l1ll_opy_]
  for bstack1lllll11l_opy_ in list(config):
    for bstack1l11l1ll_opy_ in bstack1lllll_opy_:
      if bstack1lllll11l_opy_.lower() == bstack1l11l1ll_opy_.lower() and bstack1lllll11l_opy_ != bstack1l11l1ll_opy_:
        config[bstack1l11l1ll_opy_] = config[bstack1lllll11l_opy_]
        del config[bstack1lllll11l_opy_]
  bstack1llll1l1l_opy_ = []
  if bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௛") in config:
    bstack1llll1l1l_opy_ = config[bstack1l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௜")]
  for platform in bstack1llll1l1l_opy_:
    for bstack1lllll11l_opy_ in list(platform):
      for bstack1l11l1ll_opy_ in bstack1lllll_opy_:
        if bstack1lllll11l_opy_.lower() == bstack1l11l1ll_opy_.lower() and bstack1lllll11l_opy_ != bstack1l11l1ll_opy_:
          platform[bstack1l11l1ll_opy_] = platform[bstack1lllll11l_opy_]
          del platform[bstack1lllll11l_opy_]
  for bstack11l1l11l_opy_, bstack1l1l1ll_opy_ in bstack1ll1ll_opy_.items():
    for platform in bstack1llll1l1l_opy_:
      if isinstance(bstack1l1l1ll_opy_, list):
        for bstack1lllll11l_opy_ in bstack1l1l1ll_opy_:
          if bstack1lllll11l_opy_ in platform:
            platform[bstack11l1l11l_opy_] = platform[bstack1lllll11l_opy_]
            del platform[bstack1lllll11l_opy_]
            break
      elif bstack1l1l1ll_opy_ in platform:
        platform[bstack11l1l11l_opy_] = platform[bstack1l1l1ll_opy_]
        del platform[bstack1l1l1ll_opy_]
  for bstack1l1ll1_opy_ in bstack1lll1_opy_:
    if bstack1l1ll1_opy_ in config:
      if not bstack1lll1_opy_[bstack1l1ll1_opy_] in config:
        config[bstack1lll1_opy_[bstack1l1ll1_opy_]] = {}
      config[bstack1lll1_opy_[bstack1l1ll1_opy_]].update(config[bstack1l1ll1_opy_])
      del config[bstack1l1ll1_opy_]
  for platform in bstack1llll1l1l_opy_:
    for bstack1l1ll1_opy_ in bstack1lll1_opy_:
      if bstack1l1ll1_opy_ in list(platform):
        if not bstack1lll1_opy_[bstack1l1ll1_opy_] in platform:
          platform[bstack1lll1_opy_[bstack1l1ll1_opy_]] = {}
        platform[bstack1lll1_opy_[bstack1l1ll1_opy_]].update(platform[bstack1l1ll1_opy_])
        del platform[bstack1l1ll1_opy_]
  config = bstack1l1ll11l_opy_(config)
  return config
def bstack1l111ll_opy_(config):
  global bstack1l1111_opy_
  if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௝") in config and str(config[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ௞")]).lower() != bstack1l1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௟"):
    if not bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭௠") in config:
      config[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ௡")] = {}
    if not bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௢") in config[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ௣")]:
      if bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ௤") in os.environ:
        config[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ௥")][bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௦")] = os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ௧")]
      else:
        current_time = datetime.datetime.now()
        bstack11l1ll11_opy_ = current_time.strftime(bstack1l1l_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧ௨"))
        hostname = socket.gethostname()
        bstack1ll1lll1_opy_ = bstack1l1l_opy_ (u"ࠫࠬ௩").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack1l1l_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧ௪").format(bstack11l1ll11_opy_, hostname, bstack1ll1lll1_opy_)
        config[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௫")][bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬")] = identifier
    bstack1l1111_opy_ = config[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ௭")][bstack1l1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௮")]
  return config
def bstack1ll11llll_opy_(config):
  if bstack1l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭௯") in config and config[bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ௰")] not in bstack1ll1l_opy_:
    return config[bstack1l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ௱")]
  elif bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ௲") in os.environ:
    return os.environ[bstack1l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ௳")]
  else:
    return None
def bstack1lll1l111_opy_(config):
  if bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫ௴") in os.environ:
    return os.environ[bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬ௵")]
  elif bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௶") in config:
    return config[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௷")]
  else:
    return None
def bstack1ll11ll1l_opy_():
  if (
    isinstance(os.getenv(bstack1l1l_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪ௸")), str) and len(os.getenv(bstack1l1l_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫ௹"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l1l_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭௺")), str) and len(os.getenv(bstack1l1l_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧ௻"))) > 0
  ):
    return os.getenv(bstack1l1l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨ௼"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠪࡇࡎ࠭௽"))).lower() == bstack1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ௾") and str(os.getenv(bstack1l1l_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡈࡏࠧ௿"))).lower() == bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫఀ"):
    return os.getenv(bstack1l1l_opy_ (u"ࠧࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠪఁ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠨࡅࡌࠫం"))).lower() == bstack1l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧః") and str(os.getenv(bstack1l1l_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࠪఄ"))).lower() == bstack1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩఅ"):
    return os.getenv(bstack1l1l_opy_ (u"࡚ࠬࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫఆ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"࠭ࡃࡊࠩఇ"))).lower() == bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬఈ") and str(os.getenv(bstack1l1l_opy_ (u"ࠨࡅࡌࡣࡓࡇࡍࡆࠩఉ"))).lower() == bstack1l1l_opy_ (u"ࠩࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠫఊ"):
    return 0 # bstack1lll11ll_opy_ bstack11l111l1_opy_ not set build number env
  if os.getenv(bstack1l1l_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍ࠭ఋ")) and os.getenv(bstack1l1l_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠧఌ")):
    return os.getenv(bstack1l1l_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧ఍"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"࠭ࡃࡊࠩఎ"))).lower() == bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬఏ") and str(os.getenv(bstack1l1l_opy_ (u"ࠨࡆࡕࡓࡓࡋࠧఐ"))).lower() == bstack1l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ఑"):
    return os.getenv(bstack1l1l_opy_ (u"ࠪࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨఒ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠫࡈࡏࠧఓ"))).lower() == bstack1l1l_opy_ (u"ࠬࡺࡲࡶࡧࠪఔ") and str(os.getenv(bstack1l1l_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࠩక"))).lower() == bstack1l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬఖ"):
    return os.getenv(bstack1l1l_opy_ (u"ࠨࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠫగ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠩࡆࡍࠬఘ"))).lower() == bstack1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨఙ") and str(os.getenv(bstack1l1l_opy_ (u"ࠫࡌࡏࡔࡍࡃࡅࡣࡈࡏࠧచ"))).lower() == bstack1l1l_opy_ (u"ࠬࡺࡲࡶࡧࠪఛ"):
    return os.getenv(bstack1l1l_opy_ (u"࠭ࡃࡊࡡࡍࡓࡇࡥࡉࡅࠩజ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"ࠧࡄࡋࠪఝ"))).lower() == bstack1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ఞ") and str(os.getenv(bstack1l1l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠬట"))).lower() == bstack1l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨఠ"):
    return os.getenv(bstack1l1l_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭డ"), 0)
  if str(os.getenv(bstack1l1l_opy_ (u"࡚ࠬࡆࡠࡄࡘࡍࡑࡊࠧఢ"))).lower() == bstack1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫణ"):
    return os.getenv(bstack1l1l_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧత"), 0)
  return -1
def bstack1111l1l1_opy_(bstack11lllll1_opy_):
  global CONFIG
  if not bstack1l1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪథ") in CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫద")]:
    return
  CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬధ")] = CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭న")].replace(
    bstack1l1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ఩"),
    str(bstack11lllll1_opy_)
  )
def bstack1l1l111l_opy_():
  global CONFIG
  if not bstack1l1l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬప") in CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఫ")]:
    return
  current_time = datetime.datetime.now()
  bstack11l1ll11_opy_ = current_time.strftime(bstack1l1l_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭బ"))
  CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫభ")] = CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬమ")].replace(
    bstack1l1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪయ"),
    bstack11l1ll11_opy_
  )
def bstack11l1111_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧర") in CONFIG and not bool(CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఱ")]):
    del CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩల")]
    return
  if not bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪళ") in CONFIG:
    CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫఴ")] = bstack1l1l_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭వ")
  if bstack1l1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪశ") in CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧష")]:
    bstack1l1l111l_opy_()
    os.environ[bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪస")] = CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩహ")]
  if not bstack1l1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ఺") in CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ఻")]:
    return
  bstack11lllll1_opy_ = bstack1l1l_opy_ (u"఼ࠪࠫ")
  bstack1llll1lll_opy_ = bstack1ll11ll1l_opy_()
  if bstack1llll1lll_opy_ != -1:
    bstack11lllll1_opy_ = bstack1l1l_opy_ (u"ࠫࡈࡏࠠࠨఽ") + str(bstack1llll1lll_opy_)
  if bstack11lllll1_opy_ == bstack1l1l_opy_ (u"ࠬ࠭ా"):
    bstack1111lll1_opy_ = bstack1ll1l11ll_opy_(CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩి")])
    if bstack1111lll1_opy_ != -1:
      bstack11lllll1_opy_ = str(bstack1111lll1_opy_)
  if bstack11lllll1_opy_:
    bstack1111l1l1_opy_(bstack11lllll1_opy_)
    os.environ[bstack1l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫీ")] = CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪు")]
def bstack11lll1_opy_(bstack11lll11l_opy_, bstack1lll1ll_opy_, path):
  bstack1ll111l_opy_ = {
    bstack1l1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ూ"): bstack1lll1ll_opy_
  }
  if os.path.exists(path):
    bstack1ll11l11_opy_ = json.load(open(path, bstack1l1l_opy_ (u"ࠪࡶࡧ࠭ృ")))
  else:
    bstack1ll11l11_opy_ = {}
  bstack1ll11l11_opy_[bstack11lll11l_opy_] = bstack1ll111l_opy_
  with open(path, bstack1l1l_opy_ (u"ࠦࡼ࠱ࠢౄ")) as outfile:
    json.dump(bstack1ll11l11_opy_, outfile)
def bstack1ll1l11ll_opy_(bstack11lll11l_opy_):
  bstack11lll11l_opy_ = str(bstack11lll11l_opy_)
  bstack111lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠬࢄࠧ౅")), bstack1l1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ె"))
  try:
    if not os.path.exists(bstack111lll11_opy_):
      os.makedirs(bstack111lll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠧࡿࠩే")), bstack1l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨై"), bstack1l1l_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ౉"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1l_opy_ (u"ࠪࡻࠬొ")):
        pass
      with open(file_path, bstack1l1l_opy_ (u"ࠦࡼ࠱ࠢో")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1l_opy_ (u"ࠬࡸࠧౌ")) as bstack11111l1l_opy_:
      bstack111ll1ll_opy_ = json.load(bstack11111l1l_opy_)
    if bstack11lll11l_opy_ in bstack111ll1ll_opy_:
      bstack111ll1l_opy_ = bstack111ll1ll_opy_[bstack11lll11l_opy_][bstack1l1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ్ࠪ")]
      bstack111l1lll_opy_ = int(bstack111ll1l_opy_) + 1
      bstack11lll1_opy_(bstack11lll11l_opy_, bstack111l1lll_opy_, file_path)
      return bstack111l1lll_opy_
    else:
      bstack11lll1_opy_(bstack11lll11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11lllll_opy_.format(str(e)))
    return -1
def bstack11lll111_opy_(config):
  if bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౎") in config and config[bstack1l1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ౏")] not in bstack1lll1l_opy_:
    return config[bstack1l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ౐")]
  elif bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ౑") in os.environ:
    return os.environ[bstack1l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ౒")]
  else:
    return None
def bstack1llllll1l_opy_(config):
  if not bstack11lll111_opy_(config) or not bstack1ll11llll_opy_(config):
    return True
  else:
    return False
def bstack111111l1_opy_(config):
  if bstack11111ll_opy_() < version.parse(bstack1l1l_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫ౓")):
    return False
  if bstack11111ll_opy_() >= version.parse(bstack1l1l_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬ౔")):
    return True
  if bstack1l1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉౕࠧ") in config and config[bstack1l1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨౖ")] == False:
    return False
  else:
    return True
def bstack1l11l1l_opy_(config, index = 0):
  global bstack11llll_opy_
  bstack1l1l1l1l_opy_ = {}
  caps = bstack1llll1_opy_ + bstack1l111_opy_
  if bstack11llll_opy_:
    caps += bstack1111_opy_
  for key in config:
    if key in caps + [bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗")]:
      continue
    bstack1l1l1l1l_opy_[key] = config[key]
  if bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ౘ") in config:
    for bstack11llll1_opy_ in config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౙ")][index]:
      if bstack11llll1_opy_ in caps + [bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪౚ"), bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౛")]:
        continue
      bstack1l1l1l1l_opy_[bstack11llll1_opy_] = config[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౜")][index][bstack11llll1_opy_]
  bstack1l1l1l1l_opy_[bstack1l1l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪౝ")] = socket.gethostname()
  return bstack1l1l1l1l_opy_
def bstack1l111l1_opy_(config):
  global bstack11llll_opy_
  bstack1lll1l1_opy_ = {}
  caps = bstack1l111_opy_
  if bstack11llll_opy_:
    caps+= bstack1111_opy_
  for key in caps:
    if key in config:
      bstack1lll1l1_opy_[key] = config[key]
  return bstack1lll1l1_opy_
def bstack1ll1111l_opy_(bstack1l1l1l1l_opy_, bstack1lll1l1_opy_):
  bstack1llll11l1_opy_ = {}
  for key in bstack1l1l1l1l_opy_.keys():
    if key in bstack11ll_opy_:
      bstack1llll11l1_opy_[bstack11ll_opy_[key]] = bstack1l1l1l1l_opy_[key]
    else:
      bstack1llll11l1_opy_[key] = bstack1l1l1l1l_opy_[key]
  for key in bstack1lll1l1_opy_:
    if key in bstack11ll_opy_:
      bstack1llll11l1_opy_[bstack11ll_opy_[key]] = bstack1lll1l1_opy_[key]
    else:
      bstack1llll11l1_opy_[key] = bstack1lll1l1_opy_[key]
  return bstack1llll11l1_opy_
def bstack11lll1l_opy_(config, index = 0):
  global bstack11llll_opy_
  caps = {}
  bstack1lll1l1_opy_ = bstack1l111l1_opy_(config)
  bstack11111ll1_opy_ = bstack1l111_opy_
  bstack11111ll1_opy_ += bstack1l11_opy_
  if bstack11llll_opy_:
    bstack11111ll1_opy_ += bstack1111_opy_
  if bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౞") in config:
    if bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ౟") in config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౠ")][index]:
      caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪౡ")] = config[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ")][index][bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬౣ")]
    if bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ౤") in config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౥")][index]:
      caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ౦")] = str(config[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ౧")][index][bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౨")])
    bstack1ll1l1l_opy_ = {}
    for bstack1ll11l1l_opy_ in bstack11111ll1_opy_:
      if bstack1ll11l1l_opy_ in config[bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౩")][index]:
        if bstack1ll11l1l_opy_ == bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ౪"):
          bstack1ll1l1l_opy_[bstack1ll11l1l_opy_] = str(config[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౫")][index][bstack1ll11l1l_opy_] * 1.0)
        else:
          bstack1ll1l1l_opy_[bstack1ll11l1l_opy_] = config[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౬")][index][bstack1ll11l1l_opy_]
        del(config[bstack1l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౭")][index][bstack1ll11l1l_opy_])
    bstack1lll1l1_opy_ = update(bstack1lll1l1_opy_, bstack1ll1l1l_opy_)
  bstack1l1l1l1l_opy_ = bstack1l11l1l_opy_(config, index)
  for bstack1lllll11l_opy_ in bstack1l111_opy_ + [bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ౮"), bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౯")]:
    if bstack1lllll11l_opy_ in bstack1l1l1l1l_opy_:
      bstack1lll1l1_opy_[bstack1lllll11l_opy_] = bstack1l1l1l1l_opy_[bstack1lllll11l_opy_]
      del(bstack1l1l1l1l_opy_[bstack1lllll11l_opy_])
  if bstack111111l1_opy_(config):
    bstack1l1l1l1l_opy_[bstack1l1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭౰")] = True
    caps.update(bstack1lll1l1_opy_)
    caps[bstack1l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ౱")] = bstack1l1l1l1l_opy_
  else:
    bstack1l1l1l1l_opy_[bstack1l1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ౲")] = False
    caps.update(bstack1ll1111l_opy_(bstack1l1l1l1l_opy_, bstack1lll1l1_opy_))
    if bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ౳") in caps:
      caps[bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ౴")] = caps[bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ౵")]
      del(caps[bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ౶")])
    if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౷") in caps:
      caps[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ౸")] = caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ౹")]
      del(caps[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ౺")])
  return caps
def bstack111l11l_opy_():
  if bstack11111ll_opy_() <= version.parse(bstack1l1l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ౻")):
    return bstack111l_opy_
  return bstack1lll11_opy_
def bstack1ll1ll11l_opy_(options):
  return hasattr(options, bstack1l1l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ౼"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l111l_opy_(options, bstack11ll1l1_opy_):
  for bstack1lll1ll11_opy_ in bstack11ll1l1_opy_:
    if bstack1lll1ll11_opy_ in [bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ౽"), bstack1l1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ౾")]:
      next
    if bstack1lll1ll11_opy_ in options._experimental_options:
      options._experimental_options[bstack1lll1ll11_opy_]= update(options._experimental_options[bstack1lll1ll11_opy_], bstack11ll1l1_opy_[bstack1lll1ll11_opy_])
    else:
      options.add_experimental_option(bstack1lll1ll11_opy_, bstack11ll1l1_opy_[bstack1lll1ll11_opy_])
  if bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ౿") in bstack11ll1l1_opy_:
    for arg in bstack11ll1l1_opy_[bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ಀ")]:
      options.add_argument(arg)
    del(bstack11ll1l1_opy_[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧಁ")])
  if bstack1l1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧಂ") in bstack11ll1l1_opy_:
    for ext in bstack11ll1l1_opy_[bstack1l1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨಃ")]:
      options.add_extension(ext)
    del(bstack11ll1l1_opy_[bstack1l1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ಄")])
def bstack11111l11_opy_(options, bstack1ll1llll_opy_):
  if bstack1l1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬಅ") in bstack1ll1llll_opy_:
    for bstack1ll1ll1ll_opy_ in bstack1ll1llll_opy_[bstack1l1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ಆ")]:
      if bstack1ll1ll1ll_opy_ in options._preferences:
        options._preferences[bstack1ll1ll1ll_opy_] = update(options._preferences[bstack1ll1ll1ll_opy_], bstack1ll1llll_opy_[bstack1l1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧಇ")][bstack1ll1ll1ll_opy_])
      else:
        options.set_preference(bstack1ll1ll1ll_opy_, bstack1ll1llll_opy_[bstack1l1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨಈ")][bstack1ll1ll1ll_opy_])
  if bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨಉ") in bstack1ll1llll_opy_:
    for arg in bstack1ll1llll_opy_[bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩಊ")]:
      options.add_argument(arg)
def bstack1l1111l_opy_(options, bstack1lllll111_opy_):
  if bstack1l1l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ಋ") in bstack1lllll111_opy_:
    options.use_webview(bool(bstack1lllll111_opy_[bstack1l1l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧಌ")]))
  bstack1l111l_opy_(options, bstack1lllll111_opy_)
def bstack11llllll_opy_(options, bstack111l1l11_opy_):
  for bstack1ll1l111l_opy_ in bstack111l1l11_opy_:
    if bstack1ll1l111l_opy_ in [bstack1l1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ಍"), bstack1l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ಎ")]:
      next
    options.set_capability(bstack1ll1l111l_opy_, bstack111l1l11_opy_[bstack1ll1l111l_opy_])
  if bstack1l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧಏ") in bstack111l1l11_opy_:
    for arg in bstack111l1l11_opy_[bstack1l1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨಐ")]:
      options.add_argument(arg)
  if bstack1l1l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨ಑") in bstack111l1l11_opy_:
    options.use_technology_preview(bool(bstack111l1l11_opy_[bstack1l1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩಒ")]))
def bstack1l11ll_opy_(options, bstack1l1l1l1_opy_):
  for bstack11l11l1l_opy_ in bstack1l1l1l1_opy_:
    if bstack11l11l1l_opy_ in [bstack1l1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪಓ"), bstack1l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬಔ")]:
      next
    options._options[bstack11l11l1l_opy_] = bstack1l1l1l1_opy_[bstack11l11l1l_opy_]
  if bstack1l1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬಕ") in bstack1l1l1l1_opy_:
    for bstack111l1l1l_opy_ in bstack1l1l1l1_opy_[bstack1l1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಖ")]:
      options.add_additional_option(
          bstack111l1l1l_opy_, bstack1l1l1l1_opy_[bstack1l1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧಗ")][bstack111l1l1l_opy_])
  if bstack1l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩಘ") in bstack1l1l1l1_opy_:
    for arg in bstack1l1l1l1_opy_[bstack1l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪಙ")]:
      options.add_argument(arg)
def bstack1lll11lll_opy_(options, caps):
  if not hasattr(options, bstack1l1l_opy_ (u"࠭ࡋࡆ࡛ࠪಚ")):
    return
  if options.KEY == bstack1l1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬಛ") and options.KEY in caps:
    bstack1l111l_opy_(options, caps[bstack1l1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ಜ")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧಝ") and options.KEY in caps:
    bstack11111l11_opy_(options, caps[bstack1l1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨಞ")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬಟ") and options.KEY in caps:
    bstack11llllll_opy_(options, caps[bstack1l1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ಠ")])
  elif options.KEY == bstack1l1l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧಡ") and options.KEY in caps:
    bstack1l1111l_opy_(options, caps[bstack1l1l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨಢ")])
  elif options.KEY == bstack1l1l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧಣ") and options.KEY in caps:
    bstack1l11ll_opy_(options, caps[bstack1l1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨತ")])
def bstack1ll1lllll_opy_(caps):
  global bstack11llll_opy_
  if bstack11llll_opy_:
    if bstack1llll1ll1_opy_() < version.parse(bstack1l1l_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩಥ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫದ")
    if bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪಧ") in caps:
      browser = caps[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫನ")]
    elif bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ಩") in caps:
      browser = caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩಪ")]
    browser = str(browser).lower()
    if browser == bstack1l1l_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩಫ") or browser == bstack1l1l_opy_ (u"ࠪ࡭ࡵࡧࡤࠨಬ"):
      browser = bstack1l1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫಭ")
    if browser == bstack1l1l_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭ಮ"):
      browser = bstack1l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ಯ")
    if browser not in [bstack1l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧರ"), bstack1l1l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ಱ"), bstack1l1l_opy_ (u"ࠩ࡬ࡩࠬಲ"), bstack1l1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪಳ"), bstack1l1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ಴")]:
      return None
    try:
      package = bstack1l1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧವ").format(browser)
      name = bstack1l1l_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧಶ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1ll11l_opy_(options):
        return None
      for bstack1lllll11l_opy_ in caps.keys():
        options.set_capability(bstack1lllll11l_opy_, caps[bstack1lllll11l_opy_])
      bstack1lll11lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1111llll_opy_(options, bstack111ll11l_opy_):
  if not bstack1ll1ll11l_opy_(options):
    return
  for bstack1lllll11l_opy_ in bstack111ll11l_opy_.keys():
    if bstack1lllll11l_opy_ in bstack1l11_opy_:
      next
    if bstack1lllll11l_opy_ in options._caps and type(options._caps[bstack1lllll11l_opy_]) in [dict, list]:
      options._caps[bstack1lllll11l_opy_] = update(options._caps[bstack1lllll11l_opy_], bstack111ll11l_opy_[bstack1lllll11l_opy_])
    else:
      options.set_capability(bstack1lllll11l_opy_, bstack111ll11l_opy_[bstack1lllll11l_opy_])
  bstack1lll11lll_opy_(options, bstack111ll11l_opy_)
  if bstack1l1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ಷ") in options._caps:
    if options._caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ಸ")] and options._caps[bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧಹ")].lower() != bstack1l1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ಺"):
      del options._caps[bstack1l1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ಻")]
def bstack1l1l11l_opy_(proxy_config):
  if bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺ಼ࠩ") in proxy_config:
    proxy_config[bstack1l1l_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨಽ")] = proxy_config[bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫಾ")]
    del(proxy_config[bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬಿ")])
  if bstack1l1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬೀ") in proxy_config and proxy_config[bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ು")].lower() != bstack1l1l_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫೂ"):
    proxy_config[bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨೃ")] = bstack1l1l_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭ೄ")
  if bstack1l1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ೅") in proxy_config:
    proxy_config[bstack1l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫೆ")] = bstack1l1l_opy_ (u"ࠩࡳࡥࡨ࠭ೇ")
  return proxy_config
def bstack1ll1111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩೈ") in config:
    return proxy
  config[bstack1l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ೉")] = bstack1l1l11l_opy_(config[bstack1l1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫೊ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬೋ")])
  return proxy
def bstack111ll1_opy_(self):
  global CONFIG
  global bstack111lllll_opy_
  if bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪೌ") in CONFIG:
    return CONFIG[bstack1l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼ್ࠫ")]
  elif bstack1l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭೎") in CONFIG:
    return CONFIG[bstack1l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ೏")]
  else:
    return bstack111lllll_opy_(self)
def bstack1lllll11_opy_():
  global CONFIG
  return bstack1l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ೐") in CONFIG or bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ೑") in CONFIG
def bstack1l111111_opy_():
  return bstack1lllll11_opy_() and bstack11111ll_opy_() >= version.parse(bstack1l11l_opy_)
def bstack1l1llll_opy_(config):
  if bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ೒") in config:
    if str(config[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ೓")]).lower() == bstack1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭೔"):
      return True
    else:
      return False
  elif bstack1l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧೕ") in os.environ:
    if str(os.environ[bstack1l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨೖ")]).lower() == bstack1l1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ೗"):
      return True
    else:
      return False
  else:
    return False
def bstack1l1ll1l_opy_(config):
  if bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ೘") in config:
    return config[bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ೙")]
  if bstack1l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭೚") in config:
    return config[bstack1l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ೛")]
  return {}
def bstack1ll1llll1_opy_(caps):
  global bstack1l1111_opy_
  if bstack1l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ೜") in caps:
    caps[bstack1l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫೝ")][bstack1l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪೞ")] = True
    if bstack1l1111_opy_:
      caps[bstack1l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭೟")][bstack1l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨೠ")] = bstack1l1111_opy_
  else:
    caps[bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬೡ")] = True
    if bstack1l1111_opy_:
      caps[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩೢ")] = bstack1l1111_opy_
def bstack1llll11l_opy_():
  global CONFIG
  if bstack1l1llll_opy_(CONFIG):
    bstack1lll11l1l_opy_ = bstack1l1ll1l_opy_(CONFIG)
    bstack11l111l_opy_(bstack1ll11llll_opy_(CONFIG), bstack1lll11l1l_opy_)
def bstack11l111l_opy_(key, bstack1lll11l1l_opy_):
  global bstack1lll1ll1l_opy_
  logger.info(bstack1l11l11l_opy_)
  try:
    bstack1lll1ll1l_opy_ = Local()
    bstack11ll111_opy_ = {bstack1l1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ೣ"): key}
    bstack11ll111_opy_.update(bstack1lll11l1l_opy_)
    logger.debug(bstack111l111l_opy_.format(str(bstack11ll111_opy_)))
    bstack1lll1ll1l_opy_.start(**bstack11ll111_opy_)
    if bstack1lll1ll1l_opy_.isRunning():
      logger.info(bstack11ll111l_opy_)
  except Exception as e:
    bstack1llllll1_opy_(bstack1l111l1l_opy_.format(str(e)))
def bstack11ll1111_opy_():
  global bstack1lll1ll1l_opy_
  if bstack1lll1ll1l_opy_.isRunning():
    logger.info(bstack1lllllll_opy_)
    bstack1lll1ll1l_opy_.stop()
  bstack1lll1ll1l_opy_ = None
def bstack1l111lll_opy_():
  global bstack1l11ll11_opy_
  if bstack1l11ll11_opy_:
    logger.warning(bstack111llll_opy_.format(str(bstack1l11ll11_opy_)))
  logger.info(bstack1lll1l1l1_opy_)
  global bstack1lll1ll1l_opy_
  if bstack1lll1ll1l_opy_:
    bstack11ll1111_opy_()
  logger.info(bstack11l1lll_opy_)
def bstack11l1l1ll_opy_(self, *args):
  logger.error(bstack111111_opy_)
  bstack1l111lll_opy_()
  sys.exit(1)
def bstack1llllll1_opy_(err):
  logger.critical(bstack1llll11ll_opy_.format(str(err)))
  atexit.unregister(bstack1l111lll_opy_)
  sys.exit(1)
def bstack1ll1l1lll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack1l111lll_opy_)
  sys.exit(1)
def bstack11llll1l_opy_():
  global CONFIG
  CONFIG = bstack11l1lll1_opy_()
  CONFIG = bstack11111lll_opy_(CONFIG)
  CONFIG = bstack1l111ll_opy_(CONFIG)
  if bstack1llllll1l_opy_(CONFIG):
    bstack1llllll1_opy_(bstack1l1lll1l_opy_)
  CONFIG[bstack1l1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ೤")] = bstack11lll111_opy_(CONFIG)
  CONFIG[bstack1l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ೥")] = bstack1ll11llll_opy_(CONFIG)
  if bstack1lll1l111_opy_(CONFIG):
    CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೦")] = bstack1lll1l111_opy_(CONFIG)
    if not os.getenv(bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩ೧")):
      if os.getenv(bstack1l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ೨")):
        CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೩")] = os.getenv(bstack1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭೪"))
      else:
        bstack11l1111_opy_()
    else:
      if bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ೫") in CONFIG:
        del(CONFIG[bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೬")])
  bstack1ll1l1l11_opy_()
  bstack111l1ll1_opy_()
  if bstack11llll_opy_:
    CONFIG[bstack1l1l_opy_ (u"ࠬࡧࡰࡱࠩ೭")] = bstack111lll1_opy_(CONFIG)
    logger.info(bstack11ll11l1_opy_.format(CONFIG[bstack1l1l_opy_ (u"࠭ࡡࡱࡲࠪ೮")]))
def bstack111l1ll1_opy_():
  global CONFIG
  global bstack11llll_opy_
  if bstack1l1l_opy_ (u"ࠧࡢࡲࡳࠫ೯") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1ll11lll1_opy_)
    bstack11llll_opy_ = True
def bstack111lll1_opy_(config):
  bstack1111111l_opy_ = bstack1l1l_opy_ (u"ࠨࠩ೰")
  app = config[bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࠭ೱ")]
  if isinstance(config[bstack1l1l_opy_ (u"ࠪࡥࡵࡶࠧೲ")], str):
    if os.path.splitext(app)[1] in bstack11ll1_opy_:
      if os.path.exists(app):
        bstack1111111l_opy_ = bstack11lll1l1_opy_(config, app)
      elif bstack1ll1l1_opy_(app):
        bstack1111111l_opy_ = app
      else:
        bstack1llllll1_opy_(bstack1lll1111_opy_.format(app))
    else:
      if bstack1ll1l1_opy_(app):
        bstack1111111l_opy_ = app
      elif os.path.exists(app):
        bstack1111111l_opy_ = bstack11lll1l1_opy_(app)
      else:
        bstack1llllll1_opy_(bstack111l11ll_opy_)
  else:
    if len(app) > 2:
      bstack1llllll1_opy_(bstack1llll111_opy_)
    elif len(app) == 2:
      if bstack1l1l_opy_ (u"ࠫࡵࡧࡴࡩࠩೳ") in app and bstack1l1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ೴") in app:
        if os.path.exists(app[bstack1l1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ೵")]):
          bstack1111111l_opy_ = bstack11lll1l1_opy_(config, app[bstack1l1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ೶")], app[bstack1l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ೷")])
        else:
          bstack1llllll1_opy_(bstack1lll1111_opy_.format(app))
      else:
        bstack1llllll1_opy_(bstack1llll111_opy_)
    else:
      for key in app:
        if key in bstack111l1_opy_:
          if key == bstack1l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ೸"):
            if os.path.exists(app[key]):
              bstack1111111l_opy_ = bstack11lll1l1_opy_(config, app[key])
            else:
              bstack1llllll1_opy_(bstack1lll1111_opy_.format(app))
          else:
            bstack1111111l_opy_ = app[key]
        else:
          bstack1llllll1_opy_(bstack11llll11_opy_)
  return bstack1111111l_opy_
def bstack1ll1l1_opy_(bstack1111111l_opy_):
  import re
  bstack1lll11l11_opy_ = re.compile(bstack1l1l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ೹"))
  bstack1l1lllll_opy_ = re.compile(bstack1l1l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ೺"))
  if bstack1l1l_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ೻") in bstack1111111l_opy_ or re.fullmatch(bstack1lll11l11_opy_, bstack1111111l_opy_) or re.fullmatch(bstack1l1lllll_opy_, bstack1111111l_opy_):
    return True
  else:
    return False
def bstack11lll1l1_opy_(config, path, bstack1ll1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1l_opy_ (u"࠭ࡲࡣࠩ೼")).read()).hexdigest()
  bstack1111ll_opy_ = bstack1ll1l1ll1_opy_(md5_hash)
  bstack1111111l_opy_ = None
  if bstack1111ll_opy_:
    logger.info(bstack11l11l11_opy_.format(bstack1111ll_opy_, md5_hash))
    return bstack1111ll_opy_
  bstack111lll_opy_ = MultipartEncoder(
    fields={
        bstack1l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ೽"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1l_opy_ (u"ࠨࡴࡥࠫ೾")), bstack1l1l_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭೿")),
        bstack1l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ഀ"): bstack1ll1l11_opy_
    }
  )
  response = requests.post(bstack11lll_opy_, data=bstack111lll_opy_,
                         headers={bstack1l1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪഁ"): bstack111lll_opy_.content_type}, auth=(bstack11lll111_opy_(config), bstack1ll11llll_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack1111111l_opy_ = res[bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡡࡸࡶࡱ࠭ം")]
    logger.info(bstack11ll1ll1_opy_.format(bstack1111111l_opy_))
    bstack1l11llll_opy_(md5_hash, bstack1111111l_opy_)
  except ValueError as err:
    bstack1llllll1_opy_(bstack1l1l1ll1_opy_.format(str(err)))
  return bstack1111111l_opy_
def bstack1ll1l1l11_opy_():
  global CONFIG
  global bstack1l1l1l_opy_
  bstack1ll1l111_opy_ = 1
  if bstack1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ഃ") in CONFIG:
    bstack1ll1l111_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧഄ")]
  bstack1lll1llll_opy_ = 0
  if bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഅ") in CONFIG:
    bstack1lll1llll_opy_ = len(CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬആ")])
  bstack1l1l1l_opy_ = int(bstack1ll1l111_opy_) * int(bstack1lll1llll_opy_)
def bstack1ll1l1ll1_opy_(md5_hash):
  bstack1l1l111_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠪࢂࠬഇ")), bstack1l1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫഈ"), bstack1l1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ഉ"))
  if os.path.exists(bstack1l1l111_opy_):
    bstack11l11ll1_opy_ = json.load(open(bstack1l1l111_opy_,bstack1l1l_opy_ (u"࠭ࡲࡣࠩഊ")))
    if md5_hash in bstack11l11ll1_opy_:
      bstack1111111_opy_ = bstack11l11ll1_opy_[md5_hash]
      bstack1l1111l1_opy_ = datetime.datetime.now()
      bstack1llll11_opy_ = datetime.datetime.strptime(bstack1111111_opy_[bstack1l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪഋ")], bstack1l1l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬഌ"))
      if (bstack1l1111l1_opy_ - bstack1llll11_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1111111_opy_[bstack1l1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ഍")]):
        return None
      return bstack1111111_opy_[bstack1l1l_opy_ (u"ࠪ࡭ࡩ࠭എ")]
  else:
    return None
def bstack1l11llll_opy_(md5_hash, bstack1111111l_opy_):
  bstack111lll11_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"ࠫࢃ࠭ഏ")), bstack1l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬഐ"))
  if not os.path.exists(bstack111lll11_opy_):
    os.makedirs(bstack111lll11_opy_)
  bstack1l1l111_opy_ = os.path.join(os.path.expanduser(bstack1l1l_opy_ (u"࠭ࡾࠨ഑")), bstack1l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧഒ"), bstack1l1l_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩഓ"))
  bstack11l1ll_opy_ = {
    bstack1l1l_opy_ (u"ࠩ࡬ࡨࠬഔ"): bstack1111111l_opy_,
    bstack1l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ക"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨഖ")),
    bstack1l1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪഗ"): str(__version__)
  }
  if os.path.exists(bstack1l1l111_opy_):
    bstack11l11ll1_opy_ = json.load(open(bstack1l1l111_opy_,bstack1l1l_opy_ (u"࠭ࡲࡣࠩഘ")))
  else:
    bstack11l11ll1_opy_ = {}
  bstack11l11ll1_opy_[md5_hash] = bstack11l1ll_opy_
  with open(bstack1l1l111_opy_, bstack1l1l_opy_ (u"ࠢࡸ࠭ࠥങ")) as outfile:
    json.dump(bstack11l11ll1_opy_, outfile)
def bstack11ll1ll_opy_(self):
  return
def bstack111ll11_opy_(self):
  return
def bstack11ll11l_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1llll1l1_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11ll1l11_opy_
  global bstack1l1lll1_opy_
  global bstack1lllll1_opy_
  global bstack11lll11_opy_
  global bstack111l1ll_opy_
  global bstack11l111ll_opy_
  CONFIG[bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪച")] = str(bstack111l1ll_opy_) + str(__version__)
  command_executor = bstack111l11l_opy_()
  logger.debug(bstack1lll1lll_opy_.format(command_executor))
  proxy = bstack1ll1111_opy_(CONFIG, proxy)
  bstack1l11111l_opy_ = 0 if bstack1l1lll1_opy_ < 0 else bstack1l1lll1_opy_
  if bstack11lll11_opy_ is True:
    bstack1l11111l_opy_ = int(threading.current_thread().getName())
  bstack111ll11l_opy_ = bstack11lll1l_opy_(CONFIG, bstack1l11111l_opy_)
  logger.debug(bstack1lll1l1ll_opy_.format(str(bstack111ll11l_opy_)))
  if bstack1l1llll_opy_(CONFIG):
    bstack1ll1llll1_opy_(bstack111ll11l_opy_)
  if desired_capabilities:
    bstack111l11l1_opy_ = bstack11lll1l_opy_(bstack11111lll_opy_(desired_capabilities))
    if bstack111l11l1_opy_:
      bstack111ll11l_opy_ = update(bstack111l11l1_opy_, bstack111ll11l_opy_)
    desired_capabilities = None
  if options:
    bstack1111llll_opy_(options, bstack111ll11l_opy_)
  if not options:
    options = bstack1ll1lllll_opy_(bstack111ll11l_opy_)
  if options and bstack11111ll_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨഛ")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack11111ll_opy_() < version.parse(bstack1l1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩജ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack111ll11l_opy_)
  logger.info(bstack1l1111ll_opy_)
  if bstack11111ll_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪഝ")):
    bstack11l111ll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11111ll_opy_() >= version.parse(bstack1l1l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬഞ")):
    bstack11l111ll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l111ll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack11ll1l11_opy_ = self.session_id
  if bstack1l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩട") in CONFIG and bstack1l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬഠ") in CONFIG[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഡ")][bstack1l11111l_opy_]:
    bstack1lllll1_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬഢ")][bstack1l11111l_opy_][bstack1l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨണ")]
  logger.debug(bstack1llll111l_opy_.format(bstack11ll1l11_opy_))
def bstack111111l_opy_(self, url):
  global bstack1ll1l1l1_opy_
  try:
    bstack1lll11l_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll111_opy_.format(str(err)))
  bstack1ll1l1l1_opy_(self, url)
def bstack11111l_opy_(self, test):
  global CONFIG
  global bstack11ll1l11_opy_
  global bstack1llll1l11_opy_
  global bstack1lllll1_opy_
  global bstack1lll11ll1_opy_
  if bstack11ll1l11_opy_:
    try:
      data = {}
      bstack11ll1lll_opy_ = None
      if test:
        bstack11ll1lll_opy_ = str(test.data)
      if bstack11ll1lll_opy_ and not bstack1lllll1_opy_:
        data[bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩത")] = bstack11ll1lll_opy_
      if bstack1llll1l11_opy_:
        if bstack1llll1l11_opy_.status == bstack1l1l_opy_ (u"ࠬࡖࡁࡔࡕࠪഥ"):
          data[bstack1l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ദ")] = bstack1l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧധ")
        elif bstack1llll1l11_opy_.status == bstack1l1l_opy_ (u"ࠨࡈࡄࡍࡑ࠭ന"):
          data[bstack1l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩഩ")] = bstack1l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪപ")
          if bstack1llll1l11_opy_.message:
            data[bstack1l1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫഫ")] = str(bstack1llll1l11_opy_.message)
      user = CONFIG[bstack1l1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧബ")]
      key = CONFIG[bstack1l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഭ")]
      url = bstack1l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬമ").format(user, key, bstack11ll1l11_opy_)
      headers = {
        bstack1l1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧയ"): bstack1l1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬര"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1ll1l_opy_.format(str(e)))
  bstack1lll11ll1_opy_(self, test)
def bstack1l11ll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1l1l1l_opy_
  bstack1ll1l1l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llll1l11_opy_
  bstack1llll1l11_opy_ = self._test
def bstack1l111ll1_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l1l_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࠥറ"), bstack1l1l_opy_ (u"ࠦࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠣല"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l1l_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࡩ࡯ࡲࠣള"), bstack1l1l_opy_ (u"ࠨ࠮ࠣഴ")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l1l_opy_ (u"ࠢࠫ࠰ࡻࡱࡱࠨവ"))))
  if not files:
    pabot._write(bstack1l1l_opy_ (u"ࠨ࡙ࡄࡖࡓࡀࠠࡏࡱࠣࡳࡺࡺࡰࡶࡶࠣࡪ࡮ࡲࡥࡴࠢ࡬ࡲࠥࠨࠥࡴࠤࠪശ") % outs_dir, pabot.Color.YELLOW)
    return bstack1l1l_opy_ (u"ࠤࠥഷ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1111ll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢസ") in options:
    del options[bstack1l1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣഹ")]
  if ROBOT_VERSION < bstack1l1l_opy_ (u"ࠧ࠺࠮࠱ࠤഺ"):
    stats = {
      bstack1l1l_opy_ (u"ࠨࡣࡳ࡫ࡷ࡭ࡨࡧ࡬഻ࠣ"): {bstack1l1l_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨ഼"): 0, bstack1l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣഽ"): 0, bstack1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤാ"): 0},
      bstack1l1l_opy_ (u"ࠥࡥࡱࡲࠢി"): {bstack1l1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥീ"): 0, bstack1l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧു"): 0, bstack1l1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨൂ"): 0},
    }
  else:
    stats = {
      bstack1l1l_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨൃ"): 0,
      bstack1l1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣൄ"): 0,
      bstack1l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ൅"): 0,
      bstack1l1l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦെ"): 0,
    }
  if pabot_args[bstack1l1l_opy_ (u"ࠦࡇ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑࡥࡒࡖࡐࠥേ")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l1l_opy_ (u"ࠧࡈࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒ࡟ࡓࡗࡑࠦൈ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l1l_opy_ (u"ࠨࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠤ൉")], pabot_args[bstack1l1l_opy_ (u"ࠢࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࡬ࡲࡸࡻࡢࡧࡱ࡯ࡨࡪࡸࡳࠣൊ")]
      )
      outputs += [
        bstack1l111ll1_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l1l_opy_ (u"ࠣ࠱ࠥോ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l1l_opy_ (u"ࠤࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠤൌ"), bstack1l1l_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࠨࡷ࠳ࡾ࡭࡭ࠤ്") % index),
        )
      ]
    if bstack1l1l_opy_ (u"ࠦࡴࡻࡴࡱࡷࡷࠦൎ") not in options:
      options[bstack1l1l_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠧ൏")] = bstack1l1l_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠥ൐")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lllll1ll_opy_(self, ff_profile_dir):
  global bstack1111l11_opy_
  if not ff_profile_dir:
    return None
  return bstack1111l11_opy_(self, ff_profile_dir)
def bstack111ll1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1111_opy_
  bstack11l11l1_opy_ = []
  if bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ൑") in CONFIG:
    bstack11l11l1_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ൒")]
  bstack111l1l1_opy_ = len(suite_group) * len(pabot_args[bstack1l1l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤ൓")] or [(bstack1l1l_opy_ (u"ࠥࠦൔ"), None)]) * len(bstack11l11l1_opy_)
  pabot_args[bstack1l1l_opy_ (u"ࠦࡇ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑࡥࡒࡖࡐࠥൕ")] = []
  for q in range(bstack111l1l1_opy_):
    pabot_args[bstack1l1l_opy_ (u"ࠧࡈࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒ࡟ࡓࡗࡑࠦൖ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢൗ")],
      pabot_args[bstack1l1l_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣ൘")],
      argfile,
      pabot_args.get(bstack1l1l_opy_ (u"ࠣࡪ࡬ࡺࡪࠨ൙")),
      pabot_args[bstack1l1l_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧ൚")],
      platform[0],
      bstack1l1111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥ൛")] or [(bstack1l1l_opy_ (u"ࠦࠧ൜"), None)]
    for platform in enumerate(bstack11l11l1_opy_)
  ]
def bstack1lll111ll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11l1llll_opy_=bstack1l1l_opy_ (u"ࠬ࠭൝")):
  global bstack111111ll_opy_
  self.platform_index = platform_index
  self.bstack1l1ll1ll_opy_ = bstack11l1llll_opy_
  bstack111111ll_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1lll1ll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll1lll1_opy_
  global bstack1ll11l_opy_
  if not bstack1l1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ൞") in item.options:
    item.options[bstack1l1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩൟ")] = []
  for v in item.options[bstack1l1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪൠ")]:
    if bstack1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨൡ") in v:
      item.options[bstack1l1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬൢ")].remove(v)
  item.options[bstack1l1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ൣ")].insert(0, bstack1l1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧ൤").format(item.platform_index))
  item.options[bstack1l1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ൥")].insert(0, bstack1l1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧ൦").format(item.bstack1l1ll1ll_opy_))
  if bstack1ll11l_opy_:
    item.options[bstack1l1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ൧")].insert(0, bstack1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡒࡒࡋࡏࡇࡇࡋࡏࡉ࠿ࢁࡽࠨ൨").format(bstack1ll11l_opy_))
  return bstack1lll1lll1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1lll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1111ll1_opy_
  global bstack1ll11l_opy_
  if bstack1ll11l_opy_:
    command[0] = command[0].replace(bstack1l1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൩"), bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠥ࠭൪") + bstack1ll11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ൫"), bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൬"), 1)
  return bstack1111ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1111l111_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111l11_opy_
  bstack111l111_opy_ = bstack1l111l11_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l1l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ൭")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ൮")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l111_opy_
def bstack111lll1l_opy_(self, name, context, *args):
  global bstack1lll1l11_opy_
  if name in [bstack1l1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ൯"), bstack1l1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൰")]:
    bstack1lll1l11_opy_(self, name, context, *args)
  if name == bstack1l1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ൱"):
    try:
      bstack11l1l111_opy_ = str(self.feature.name)
      context.browser.execute_script(bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ൲") + json.dumps(bstack11l1l111_opy_) + bstack1l1l_opy_ (u"࠭ࡽࡾࠩ൳"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ൴").format(str(e)))
  if name == bstack1l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ൵"):
    try:
      if not hasattr(self, bstack1l1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൶")):
        self.driver_before_scenario = True
      bstack1111l1ll_opy_ = args[0].name
      bstack11111111_opy_ = bstack11l1l111_opy_ = str(self.feature.name)
      bstack11l1l111_opy_ = bstack11111111_opy_ + bstack1l1l_opy_ (u"ࠪࠤ࠲ࠦࠧ൷") + bstack1111l1ll_opy_
      if self.driver_before_scenario:
        context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ൸") + json.dumps(bstack11l1l111_opy_) + bstack1l1l_opy_ (u"ࠬࢃࡽࠨ൹"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧൺ").format(str(e)))
  if name == bstack1l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨൻ"):
    try:
      bstack1llll1ll_opy_ = args[0].status.name
      if str(bstack1llll1ll_opy_).lower() == bstack1l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨർ"):
        bstack11l1l11_opy_ = bstack1l1l_opy_ (u"ࠩࠪൽ")
        bstack11l1l1l1_opy_ = bstack1l1l_opy_ (u"ࠪࠫൾ")
        bstack1l1l1l11_opy_ = bstack1l1l_opy_ (u"ࠫࠬൿ")
        try:
          import traceback
          bstack11l1l11_opy_ = self.exception.__class__.__name__
          bstack1ll1ll111_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11l1l1l1_opy_ = bstack1l1l_opy_ (u"ࠬࠦࠧ඀").join(bstack1ll1ll111_opy_)
          bstack1l1l1l11_opy_ = bstack1ll1ll111_opy_[-1]
        except Exception as e:
          logger.debug(bstack1llllll_opy_.format(str(e)))
        bstack11l1l11_opy_ += bstack1l1l1l11_opy_
        context.browser.execute_script(bstack1l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫඁ") + json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨං") + str(bstack11l1l1l1_opy_)) + bstack1l1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨඃ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ඄") + json.dumps(bstack1l1l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢඅ") + str(bstack11l1l11_opy_)) + bstack1l1l_opy_ (u"ࠫࢂࢃࠧආ"))
      else:
        context.browser.execute_script(bstack1l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪඇ") + json.dumps(str(args[0].name) + bstack1l1l_opy_ (u"ࠨࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠥඈ")) + bstack1l1l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ඉ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬඊ"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫඋ").format(str(e)))
  if name == bstack1l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪඌ"):
    try:
      if context.failed is True:
        bstack111l1111_opy_ = []
        bstack1lll1l11l_opy_ = []
        bstack1ll11l1_opy_ = []
        bstack1lll11l1_opy_ = bstack1l1l_opy_ (u"ࠫࠬඍ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack111l1111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll1ll111_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11ll_opy_ = bstack1l1l_opy_ (u"ࠬࠦࠧඎ").join(bstack1ll1ll111_opy_)
            bstack1lll1l11l_opy_.append(bstack1ll11ll_opy_)
            bstack1ll11l1_opy_.append(bstack1ll1ll111_opy_[-1])
        except Exception as e:
          logger.debug(bstack1llllll_opy_.format(str(e)))
        bstack11l1l11_opy_ = bstack1l1l_opy_ (u"࠭ࠧඏ")
        for i in range(len(bstack111l1111_opy_)):
          bstack11l1l11_opy_ += bstack111l1111_opy_[i] + bstack1ll11l1_opy_[i] + bstack1l1l_opy_ (u"ࠧ࡝ࡰࠪඐ")
        bstack1lll11l1_opy_ = bstack1l1l_opy_ (u"ࠨࠢࠪඑ").join(bstack1lll1l11l_opy_)
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧඒ") + json.dumps(bstack1lll11l1_opy_) + bstack1l1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪඓ"))
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫඔ") + json.dumps(bstack1l1l_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥඕ") + str(bstack11l1l11_opy_)) + bstack1l1l_opy_ (u"࠭ࡽࡾࠩඖ"))
      else:
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ඗") + json.dumps(bstack1l1l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦ඘") + str(self.feature.name) + bstack1l1l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦ඙")) + bstack1l1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩක"))
          context.browser.execute_script(bstack1l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨඛ"))
    except Exception as e:
      logger.debug(bstack1l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧග").format(str(e)))
  if name in [bstack1l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ඝ"), bstack1l1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨඞ")]:
    bstack1lll1l11_opy_(self, name, context, *args)
def bstack1l11lll1_opy_(bstack1lll111l1_opy_):
  global bstack111l1ll_opy_
  bstack111l1ll_opy_ = bstack1lll111l1_opy_
  logger.info(bstack11l1111l_opy_.format(bstack111l1ll_opy_.split(bstack1l1l_opy_ (u"ࠨ࠯ࠪඟ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1ll1l1lll_opy_(e, bstack11l11l_opy_)
  Service.start = bstack11ll1ll_opy_
  Service.stop = bstack111ll11_opy_
  webdriver.Remote.__init__ = bstack1llll1l1_opy_
  webdriver.Remote.get = bstack111111l_opy_
  WebDriver.close = bstack11ll11l_opy_
  if bstack1l111111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111ll1_opy_
    except Exception as e:
      logger.error(bstack1l1llll1_opy_.format(str(e)))
  if (bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨච") in str(bstack1lll111l1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l11lll_opy_)
    Output.end_test = bstack11111l_opy_
    TestStatus.__init__ = bstack1l11ll1_opy_
    WebDriverCreator._get_ff_profile = bstack1lllll1ll_opy_
    QueueItem.__init__ = bstack1lll111ll_opy_
    pabot._create_items = bstack111ll1l1_opy_
    pabot._run = bstack1lll111_opy_
    pabot._create_command_for_execution = bstack1lll1ll1_opy_
    pabot._report_results = bstack1111ll11_opy_
  if bstack1l1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪඡ") in str(bstack1lll111l1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l1l11ll_opy_)
    Runner.run_hook = bstack111lll1l_opy_
    Step.run = bstack1111l111_opy_
def bstack1ll11111_opy_():
  global CONFIG
  if bstack1l1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫජ") in CONFIG and int(CONFIG[bstack1l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬඣ")]) > 1:
    logger.warn(bstack1lll1l1l_opy_)
def bstack1l1ll111_opy_(bstack1111l11l_opy_, index):
  bstack1l11lll1_opy_(bstack1111l_opy_)
  exec(open(bstack1111l11l_opy_).read())
def bstack1111lll_opy_(arg):
  global CONFIG
  bstack1l11lll1_opy_(bstack1ll11_opy_)
  os.environ[bstack1l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧඤ")] = CONFIG[bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩඥ")]
  os.environ[bstack1l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫඦ")] = CONFIG[bstack1l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬට")]
  from _pytest.config import main as bstack1l11111_opy_
  bstack1l11111_opy_(arg)
def bstack1ll1ll11_opy_(arg):
  bstack1l11lll1_opy_(bstack11l1l_opy_)
  from behave.__main__ import main as bstack1lll1111l_opy_
  bstack1lll1111l_opy_(arg)
def bstack1111l1_opy_():
  logger.info(bstack11ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩඨ"), help=bstack1l1l_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬඩ"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠬ࠳ࡵࠨඪ"), bstack1l1l_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪණ"), help=bstack1l1l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ඬ"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠨ࠯࡮ࠫත"), bstack1l1l_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨථ"), help=bstack1l1l_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫද"))
  parser.add_argument(bstack1l1l_opy_ (u"ࠫ࠲࡬ࠧධ"), bstack1l1l_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪන"), help=bstack1l1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ඲"))
  bstack11l11ll_opy_ = parser.parse_args()
  try:
    bstack1l1l1111_opy_ = bstack1l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫඳ")
    if bstack11l11ll_opy_.framework and bstack11l11ll_opy_.framework not in (bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨප"), bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪඵ")):
      bstack1l1l1111_opy_ = bstack1l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩබ")
    bstack1l11l1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1111_opy_)
    bstack1lllll1l1_opy_ = open(bstack1l11l1l1_opy_, bstack1l1l_opy_ (u"ࠫࡷ࠭භ"))
    bstack111llll1_opy_ = bstack1lllll1l1_opy_.read()
    bstack1lllll1l1_opy_.close()
    if bstack11l11ll_opy_.username:
      bstack111llll1_opy_ = bstack111llll1_opy_.replace(bstack1l1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬම"), bstack11l11ll_opy_.username)
    if bstack11l11ll_opy_.key:
      bstack111llll1_opy_ = bstack111llll1_opy_.replace(bstack1l1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨඹ"), bstack11l11ll_opy_.key)
    if bstack11l11ll_opy_.framework:
      bstack111llll1_opy_ = bstack111llll1_opy_.replace(bstack1l1l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨය"), bstack11l11ll_opy_.framework)
    file_name = bstack1l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫර")
    file_path = os.path.abspath(file_name)
    bstack1llllll11_opy_ = open(file_path, bstack1l1l_opy_ (u"ࠩࡺࠫ඼"))
    bstack1llllll11_opy_.write(bstack111llll1_opy_)
    bstack1llllll11_opy_.close()
    logger.info(bstack1l11ll1l_opy_)
  except Exception as e:
    logger.error(bstack11l111_opy_.format(str(e)))
def bstack11ll1l1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack11llll1l_opy_()
  logger.debug(bstack1ll11ll1_opy_.format(str(CONFIG)))
  bstack1ll1lll11_opy_()
  atexit.register(bstack1l111lll_opy_)
  signal.signal(signal.SIGINT, bstack11l1l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack11l1l1ll_opy_)
def bstack1l1ll11_opy_(bstack1111ll1l_opy_, size):
  bstack11l11111_opy_ = []
  while len(bstack1111ll1l_opy_) > size:
    bstack1llll1111_opy_ = bstack1111ll1l_opy_[:size]
    bstack11l11111_opy_.append(bstack1llll1111_opy_)
    bstack1111ll1l_opy_   = bstack1111ll1l_opy_[size:]
  bstack11l11111_opy_.append(bstack1111ll1l_opy_)
  return bstack11l11111_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack111l11_opy_)
    return
  if sys.argv[1] == bstack1l1l_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ල")  or sys.argv[1] == bstack1l1l_opy_ (u"ࠫ࠲ࡼࠧ඾"):
    logger.info(bstack1l1l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ඿").format(__version__))
    return
  if sys.argv[1] == bstack1l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬව"):
    bstack1111l1_opy_()
    return
  args = sys.argv
  bstack11ll1l1l_opy_()
  global CONFIG
  global bstack1l1l1l_opy_
  global bstack11lll11_opy_
  global bstack1l1lll1_opy_
  global bstack1l1111_opy_
  global bstack1ll11l_opy_
  bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠧࠨශ")
  if args[1] == bstack1l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨෂ") or args[1] == bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪස"):
    bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪහ")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪළ"):
    bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෆ")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෇"):
    bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭෈")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෉"):
    bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮්ࠪ")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෋"):
    bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෌")
    args = args[2:]
  elif args[1] == bstack1l1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෍"):
    bstack111ll111_opy_ = bstack1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෎")
    args = args[2:]
  else:
    if not bstack1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪා") in CONFIG or str(CONFIG[bstack1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫැ")]).lower() in [bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩෑ"), bstack1l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫි")]:
      bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫී")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨු")]).lower() == bstack1l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෕"):
      bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ූ")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෗")]).lower() == bstack1l1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨෘ"):
      bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩෙ")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧේ")]).lower() == bstack1l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬෛ"):
      bstack111ll111_opy_ = bstack1l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ො")
      args = args[1:]
    elif str(CONFIG[bstack1l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪෝ")]).lower() == bstack1l1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨෞ"):
      bstack111ll111_opy_ = bstack1l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෟ")
      args = args[1:]
    else:
      bstack1llllll1_opy_(bstack1l1lll11_opy_)
  global bstack11l111ll_opy_
  global bstack1lll11ll1_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1111l11_opy_
  global bstack1111ll1_opy_
  global bstack111111ll_opy_
  global bstack1lll1lll1_opy_
  global bstack1lll111l_opy_
  global bstack1lll1l11_opy_
  global bstack1l111l11_opy_
  global bstack1ll1l1l1_opy_
  global bstack111lllll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1ll1l1lll_opy_(e, bstack11l11l_opy_)
  bstack11l111ll_opy_ = webdriver.Remote.__init__
  bstack1lll111l_opy_ = WebDriver.close
  bstack1ll1l1l1_opy_ = WebDriver.get
  if bstack1lllll11_opy_():
    if bstack11111ll_opy_() < version.parse(bstack1l11l_opy_):
      logger.error(bstack11lll1ll_opy_.format(bstack11111ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111lllll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1llll1_opy_.format(str(e)))
  if (bstack111ll111_opy_ in [bstack1l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෠"), bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෡"), bstack1l1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෢")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l11lll_opy_)
    bstack1lll11ll1_opy_ = Output.end_test
    bstack1ll1l1l1l_opy_ = TestStatus.__init__
    bstack1111l11_opy_ = WebDriverCreator._get_ff_profile
    bstack1111ll1_opy_ = pabot._run
    bstack111111ll_opy_ = QueueItem.__init__
    bstack1lll1lll1_opy_ = pabot._create_command_for_execution
  if bstack111ll111_opy_ == bstack1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෣"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l1l11ll_opy_)
    bstack1lll1l11_opy_ = Runner.run_hook
    bstack1l111l11_opy_ = Step.run
  if bstack111ll111_opy_ == bstack1l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෤"):
    bstack1llll11l_opy_()
    bstack1ll11111_opy_()
    if bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ෥") in CONFIG:
      bstack11lll11_opy_ = True
      bstack11l1ll1_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෦")]):
        bstack11l1ll1_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1l1ll111_opy_, args=(args[0], index)))
      for t in bstack11l1ll1_opy_:
        t.start()
      for t in bstack11l1ll1_opy_:
        t.join()
    else:
      bstack1l11lll1_opy_(bstack1111l_opy_)
      exec(open(args[0]).read())
  elif bstack111ll111_opy_ == bstack1l1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෧") or bstack111ll111_opy_ == bstack1l1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෨"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l11lll_opy_)
    bstack1llll11l_opy_()
    bstack1l11lll1_opy_(bstack11l1_opy_)
    if bstack1l1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ෩") in args:
      i = args.index(bstack1l1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ෪"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1l1l_opy_))
    args.insert(0, str(bstack1l1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෫")))
    pabot.main(args)
  elif bstack111ll111_opy_ == bstack1l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ෬"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l11lll_opy_)
    for a in args:
      if bstack1l1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ෭") in a:
        bstack1l1lll1_opy_ = int(a.split(bstack1l1l_opy_ (u"ࠪ࠾ࠬ෮"))[1])
      if bstack1l1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ෯") in a:
        bstack1l1111_opy_ = str(a.split(bstack1l1l_opy_ (u"ࠬࡀࠧ෰"))[1])
      if bstack1l1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡏࡏࡈࡌࡋࡋࡏࡌࡆࠩ෱") in a:
        bstack1ll11l_opy_ = str(a.split(bstack1l1l_opy_ (u"ࠧ࠻ࠩෲ"))[1])
    bstack1l11lll1_opy_(bstack11l1_opy_)
    run_cli(args)
  elif bstack111ll111_opy_ == bstack1l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෳ"):
    try:
      from _pytest.config import _prepareconfig
      import importlib
      bstack1llll1l_opy_ = importlib.find_loader(bstack1l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ෴"))
      if bstack1llll1l_opy_ is None:
        bstack1ll1l1lll_opy_(e, bstack11l1l1_opy_)
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack11l1l1_opy_)
    bstack1llll11l_opy_()
    try:
      if bstack1l1l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ෵") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭෶"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෷") in args:
        i = args.index(bstack1l1l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ෸"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1l_opy_ (u"ࠧ࠮ࡰࠪ෹") in args:
        i = args.index(bstack1l1l_opy_ (u"ࠨ࠯ࡱࠫ෺"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1ll1l11l_opy_ = config.args
    bstack1ll1l1ll_opy_ = config.invocation_params.args
    bstack1ll1l1ll_opy_ = list(bstack1ll1l1ll_opy_)
    bstack11111l1_opy_ = []
    for arg in bstack1ll1l1ll_opy_:
      for spec in bstack1ll1l11l_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack11111l1_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l1l_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ෻"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll111l1_opy_)))
                    for bstack1ll111l1_opy_ in bstack1ll1l11l_opy_]
    bstack11111l1_opy_.append(bstack1l1l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ෼"))
    bstack11111l1_opy_.append(bstack1l1l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠪ෽"))
    bstack1llllllll_opy_ = []
    for spec in bstack1ll1l11l_opy_:
      bstack11l1l1l_opy_ = []
      bstack11l1l1l_opy_.append(spec)
      bstack11l1l1l_opy_ += bstack11111l1_opy_
      bstack1llllllll_opy_.append(bstack11l1l1l_opy_)
    bstack11lll11_opy_ = True
    bstack11ll11ll_opy_ = 1
    if bstack1l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෾") in CONFIG:
      bstack11ll11ll_opy_ = CONFIG[bstack1l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭෿")]
    bstack1ll1l11l1_opy_ = int(bstack11ll11ll_opy_)*int(len(CONFIG[bstack1l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ฀")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫก")]):
      for bstack11l1l1l_opy_ in bstack1llllllll_opy_:
        item = {}
        item[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬࠭ข")] = bstack11l1l1l_opy_
        item[bstack1l1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩฃ")] = index
        execution_items.append(item)
    bstack1l1l1lll_opy_ = bstack1l1ll11_opy_(execution_items, bstack1ll1l11l1_opy_)
    for execution_item in bstack1l1l1lll_opy_:
      bstack11l1ll1_opy_ = []
      for item in execution_item:
        bstack11l1ll1_opy_.append(threading.Thread(name=str(item[bstack1l1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪค")]),
                                            target=bstack1111lll_opy_,
                                            args=(item[bstack1l1l_opy_ (u"ࠬࡧࡲࡨࠩฅ")],)))
      for t in bstack11l1ll1_opy_:
        t.start()
      for t in bstack11l1ll1_opy_:
        t.join()
  elif bstack111ll111_opy_ == bstack1l1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ฆ"):
    try:
      from behave.__main__ import main as bstack1lll1111l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1lll_opy_(e, bstack1l1l11ll_opy_)
    bstack1llll11l_opy_()
    bstack11lll11_opy_ = True
    bstack11ll11ll_opy_ = 1
    if bstack1l1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧง") in CONFIG:
      bstack11ll11ll_opy_ = CONFIG[bstack1l1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨจ")]
    bstack1ll1l11l1_opy_ = int(bstack11ll11ll_opy_)*int(len(CONFIG[bstack1l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬฉ")]))
    config = Configuration(args)
    bstack1ll1l11l_opy_ = config.paths
    bstack11ll11_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1ll1l11l_opy_:
        bstack11ll11_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l1l_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫช"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1l11l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll111l1_opy_)))
                    for bstack1ll111l1_opy_ in bstack1ll1l11l_opy_]
    bstack1llllllll_opy_ = []
    for spec in bstack1ll1l11l_opy_:
      bstack11l1l1l_opy_ = []
      bstack11l1l1l_opy_ += bstack11ll11_opy_
      bstack11l1l1l_opy_.append(spec)
      bstack1llllllll_opy_.append(bstack11l1l1l_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧซ")]):
      for bstack11l1l1l_opy_ in bstack1llllllll_opy_:
        item = {}
        item[bstack1l1l_opy_ (u"ࠬࡧࡲࡨࠩฌ")] = bstack1l1l_opy_ (u"࠭ࠠࠨญ").join(bstack11l1l1l_opy_)
        item[bstack1l1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ฎ")] = index
        execution_items.append(item)
    bstack1l1l1lll_opy_ = bstack1l1ll11_opy_(execution_items, bstack1ll1l11l1_opy_)
    for execution_item in bstack1l1l1lll_opy_:
      bstack11l1ll1_opy_ = []
      for item in execution_item:
        bstack11l1ll1_opy_.append(threading.Thread(name=str(item[bstack1l1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧฏ")]),
                                            target=bstack1ll1ll11_opy_,
                                            args=(item[bstack1l1l_opy_ (u"ࠩࡤࡶ࡬࠭ฐ")],)))
      for t in bstack11l1ll1_opy_:
        t.start()
      for t in bstack11l1ll1_opy_:
        t.join()
  else:
    bstack1llllll1_opy_(bstack1l1lll11_opy_)
  bstack1ll1l1111_opy_()
def bstack1ll1l1111_opy_():
  global CONFIG
  try:
    if bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฑ") in CONFIG:
      host = bstack1l1l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧฒ") if bstack1l1l_opy_ (u"ࠬࡧࡰࡱࠩณ") in CONFIG else bstack1l1l_opy_ (u"࠭ࡡࡱ࡫ࠪด")
      user = CONFIG[bstack1l1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩต")]
      key = CONFIG[bstack1l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫถ")]
      bstack1ll1ll1l1_opy_ = bstack1l1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨท") if bstack1l1l_opy_ (u"ࠪࡥࡵࡶࠧธ") in CONFIG else bstack1l1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭น")
      url = bstack1l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬบ").format(user, key, host, bstack1ll1ll1l1_opy_)
      headers = {
        bstack1l1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬป"): bstack1l1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪผ"),
      }
      if bstack1l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪฝ") in CONFIG:
        params = {bstack1l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧพ"):CONFIG[bstack1l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฟ")], bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧภ"):CONFIG[bstack1l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧม")]}
      else:
        params = {bstack1l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫย"):CONFIG[bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪร")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1l1l11l1_opy_ = response.json()[0][bstack1l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫฤ")]
        if bstack1l1l11l1_opy_:
          bstack11l1ll1l_opy_ = bstack1l1l11l1_opy_[bstack1l1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ล")].split(bstack1l1l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩฦ"))[0] + bstack1l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬว") + bstack1l1l11l1_opy_[bstack1l1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨศ")]
          logger.info(bstack111l1l_opy_.format(bstack11l1ll1l_opy_))
          bstack1ll1lll_opy_ = CONFIG[bstack1l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩษ")]
          if bstack1l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩส") in CONFIG:
            bstack1ll1lll_opy_ += bstack1l1l_opy_ (u"ࠨࠢࠪห") + CONFIG[bstack1l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫฬ")]
          if bstack1ll1lll_opy_!= bstack1l1l11l1_opy_[bstack1l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨอ")]:
            logger.debug(bstack1ll11lll_opy_.format(bstack1l1l11l1_opy_[bstack1l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩฮ")], bstack1ll1lll_opy_))
    else:
      logger.warn(bstack1l1lll_opy_)
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_.format(str(e)))
def bstack1lll11l_opy_(url):
  global CONFIG
  global bstack1l11ll11_opy_
  if not bstack1l11ll11_opy_:
    hostname = bstack1l1l11_opy_(url)
    is_private = bstack1ll111ll_opy_(hostname)
    if not bstack1l1llll_opy_(CONFIG) and is_private:
      bstack1l11ll11_opy_ = hostname
def bstack1l1l11_opy_(url):
  return urlparse(url).hostname
def bstack1ll111ll_opy_(hostname):
  for bstack1l11l111_opy_ in bstack111ll_opy_:
    regex = re.compile(bstack1l11l111_opy_)
    if regex.match(hostname):
      return True
  return False