from website.bits import bits_category, bits_sub_category
from website.qapi.component import Component
from website.qapi.primitives import OneOf

slug = Component('slug', str)
title = Component('title', str)
description = Component('description', str)

category = Component('category', bits_category)
sub_category = Component('sub_category', bits_sub_category)

order = Component('order', int)

path = Component('path', str)
template = Component('template', str)