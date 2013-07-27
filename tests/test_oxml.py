# -*- coding: utf-8 -*-
#
# test_oxml.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.oxml module."""

from opc.constants import RELATIONSHIP_TARGET_MODE as RTM
from opc.oxml import CT_Default, CT_Override, CT_Relationship, CT_Types

from .unitdata import a_Default, an_Override, a_Relationship, a_Types


class DescribeCT_Default(object):

    def it_provides_read_access_to_xml_values(self):
        default = a_Default().element
        assert default.extension == 'xml'
        assert default.content_type == 'application/xml'

    def it_can_construct_a_new_default_element(self):
        default = CT_Default.new('.xml', 'application/xml')
        expected_xml = a_Default().xml
        assert default.xml == expected_xml


class DescribeCT_Override(object):

    def it_provides_read_access_to_xml_values(self):
        override = an_Override().element
        assert override.partname == '/part/name.xml'
        assert override.content_type == 'app/vnd.type'

    def it_can_construct_a_new_override_element(self):
        override = CT_Override.new('/part/name.xml', 'app/vnd.type')
        expected_xml = an_Override().xml
        assert override.xml == expected_xml


class DescribeCT_Relationship(object):

    def it_provides_read_access_to_xml_values(self):
        rel = a_Relationship().element
        assert rel.rId == 'rId9'
        assert rel.reltype == 'ReLtYpE'
        assert rel.target_ref == 'docProps/core.xml'
        assert rel.target_mode == RTM.INTERNAL

    def it_can_construct_from_attribute_values(self):
        cases = (
            ('rId9', 'ReLtYpE', 'foo/bar.xml',      None),
            ('rId9', 'ReLtYpE', 'bar/foo.xml',      RTM.INTERNAL),
            ('rId9', 'ReLtYpE', 'http://some/link', RTM.EXTERNAL),
        )
        for rId, reltype, target, target_mode in cases:
            if target_mode is None:
                rel = CT_Relationship.new(rId, reltype, target)
            else:
                rel = CT_Relationship.new(rId, reltype, target, target_mode)
            builder = a_Relationship().with_target(target)
            if target_mode == RTM.EXTERNAL:
                builder = builder.with_target_mode(RTM.EXTERNAL)
            expected_rel_xml = builder.xml
            assert rel.xml == expected_rel_xml


class DescribeCT_Types(object):

    def it_provides_access_to_default_child_elements(self):
        types = a_Types().element
        assert len(types.defaults) == 2
        for default in types.defaults:
            assert isinstance(default, CT_Default)

    def it_provides_access_to_override_child_elements(self):
        types = a_Types().element
        assert len(types.overrides) == 3
        for override in types.overrides:
            assert isinstance(override, CT_Override)

    def it_should_have_empty_list_on_no_matching_elements(self):
        types = a_Types().empty().element
        assert types.defaults == []
        assert types.overrides == []

    def it_can_construct_a_new_types_element(self):
        types = CT_Types.new()
        expected_xml = a_Types().empty().xml
        assert types.xml == expected_xml

    def it_can_build_types_element_incrementally(self):
        types = CT_Types.new()
        types.add_default('.xml', 'application/xml')
        types.add_default('.jpeg', 'image/jpeg')
        types.add_override('/docProps/core.xml', 'app/vnd.type1')
        types.add_override('/ppt/presentation.xml', 'app/vnd.type2')
        types.add_override('/docProps/thumbnail.jpeg', 'image/jpeg')
        expected_types_xml = a_Types().xml
        assert types.xml == expected_types_xml
