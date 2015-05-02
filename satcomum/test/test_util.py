# -*- coding: utf-8 -*-
#
# satcomum/test/test_util.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest

from satcomum.util import forcar_unicode


def test_forcar_unicode():
    texto_unicode = u'Praça de Operações'
    assert forcar_unicode(texto_unicode) == texto_unicode
    assert forcar_unicode('Simples ASCII') == u'Simples ASCII'
    pytest.raises(TypeError, forcar_unicode, 123)
