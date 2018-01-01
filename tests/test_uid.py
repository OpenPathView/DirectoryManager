# coding: utf-8

# Copyright (C) 2017 Open Path View
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.


from zake import fake_client
from opv_directorymanager import UIDGenerator, BasicIDGenerator, ZkIDGenerator
import pytest
import uuid
import os


def test_uid_generator():
    uid = UIDGenerator()
    with pytest.raises(NotImplementedError):
        uid.getUID()


def test_basic_generator():
    uid = BasicIDGenerator("ID")

    assert(uid.prefix == "ID")

    def uid_test(count):
        muid = uid.getUID()
        assert(muid.count("ID-%s" % count) > 0)
        return muid

    temp = []
    for i in range(1,10):
        toto = uid_test(i)
        assert(toto not in temp)
        temp.append(toto)


def test_zookeeper():
    """Test zookeeper backend for generate id"""
    zk = fake_client.FakeClient()
    zk.start()
    test_zk = ZkIDGenerator(None, path="toto")

    assert(test_zk.zk is None)
    assert(test_zk.path == "toto")

    test_zk.zk = zk
    test_zk.path = "/DirectoryManager/increment"
    assert (test_zk.zk == zk)
    assert(test_zk.path == "/DirectoryManager/increment")

    assert(test_zk.increment() == 1)
    assert (test_zk.increment() == 2)
    assert (test_zk.increment() == 3)
    assert (test_zk.increment() == 4)

    zk.stop()
