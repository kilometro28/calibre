#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2014, Kovid Goyal <kovid at kovidgoyal.net>'

from lxml import etree

from calibre.ebooks.oeb.polish.container import OPF_NAMESPACES
from calibre.utils.localization import canonicalize_lang

def get_book_language(container):
    for lang in container.opf_xpath('//dc:language'):
        raw = lang.text
        if raw:
            code = canonicalize_lang(raw.split(',')[0].strip())
            if code:
                return code

def set_guide_item(container, item_type, title, name, frag=None):
    guides = container.opf_xpath('//opf:guide')
    if not guides:
        g = container.opf.makeelement('{%s}guide' % OPF_NAMESPACES['opf'], nsmap={'opf':OPF_NAMESPACES['opf']})
        container.insert_into_xml(container.opf, g)
        guides = [g]
    ref_tag = '{%s}reference' % OPF_NAMESPACES['opf']
    href = container.name_to_href(name, container.opf_name)
    if frag:
        href += '#' + frag

    for guide in guides:
        matches = []
        for child in guide.iterchildren(etree.Element):
            if child.tag == ref_tag and child.get('type', '').lower() == item_type.lower():
                matches.append(child)
        if not matches:
            r = guide.makeelement(ref_tag, type=item_type, nsmap={'opf':OPF_NAMESPACES['opf']})
            container.insert_into_xml(guide, r)
            matches.append(r)
        for m in matches:
            m.set('title', title), m.set('href', href), m.set('type', item_type)
    container.dirty(container.opf_name)

