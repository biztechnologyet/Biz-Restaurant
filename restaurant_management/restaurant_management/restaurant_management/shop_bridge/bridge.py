# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import cint, cstr

FOODS_AND_DRINKS_ITEM_GROUP = "Foods & Drinks"
DEFAULT_PRICE_LIST = "Standard Selling"


def sync_menu_to_shop(doc, method=None):
	"""Hook: Restaurant Menu.after_save"""
	try:
		removed_items = _removed_menu_items(doc)
		for row in doc.get("menu_items") or []:
			if cint(row.get("publish_on_shop")):
				_publish_item(row.get("item"))
			else:
				_unpublish_item(row.get("item"))
		for item in removed_items:
			_unpublish_item(item)
	except Exception:
		frappe.log_error(
			title="Restaurant Shop Bridge Error",
			message=frappe.get_traceback(),
		)
		frappe.msgprint(
			_("Menu saved, but the shop listing could not be updated. See Error Log for details."),
			alert=True,
		)


def unpublish_menu(doc, method=None):
	"""Hook: Restaurant Menu.on_trash"""
	for row in doc.get("menu_items") or []:
		_unpublish_item(row.get("item"))


def _removed_menu_items(doc):
	before = doc.get_doc_before_save()
	if not before:
		return []
	before_map = {
		row.get("item"): cint(row.get("publish_on_shop"))
		for row in (before.get("menu_items") or [])
	}
	after_items = {row.get("item") for row in (doc.get("menu_items") or [])}
	return [item for item, publish in before_map.items() if publish and item not in after_items]


def _publish_item(item_code):
	if not (item_code and _webshop_installed()):
		return
	_ensure_item_group(FOODS_AND_DRINKS_ITEM_GROUP)
	item = frappe.get_doc("Item", item_code)
	_publish_on_website(item)


def _unpublish_item(item_code):
	if not (item_code and _webshop_installed()):
		return
	web_item = frappe.db.exists("Website Item", {"item_code": item_code})
	if web_item:
		frappe.db.set_value("Website Item", web_item, "published", 0)


def _webshop_installed():
	return bool(
		frappe.db.exists("DocType", "Website Item")
		and frappe.db.exists("DocType", "Webshop Settings")
	)


def _ensure_item_group(item_group):
	if frappe.db.exists("Item Group", item_group):
		return
	try:
		from frappe.utils.nestedset import get_root_of

		parent = get_root_of("Item Group")
	except Exception:
		parent = "All Item Groups"
	doc = frappe.new_doc("Item Group")
	doc.item_group_name = item_group
	doc.parent_item_group = parent or "All Item Groups"
	doc.is_group = 0
	doc.flags.ignore_permissions = True
	doc.insert()


def _publish_on_website(item):
	existing = frappe.db.exists("Website Item", {"item_code": item.name})
	if existing:
		web_item = frappe.get_doc("Website Item", existing)
	else:
		from webshop.webshop.doctype.website_item.website_item import make_website_item

		web_item = make_website_item(item, save=False)
	web_item.web_item_name = cstr(item.item_name)
	web_item.published = 1
	if item.image:
		web_item.website_image = cstr(item.image)
	_ensure_website_item_group_row(web_item, FOODS_AND_DRINKS_ITEM_GROUP)
	web_item.flags.ignore_permissions = True
	web_item.save()


def _ensure_website_item_group_row(web_item, item_group):
	existing = [
		row for row in (web_item.get("website_item_groups") or [])
		if row.item_group == item_group
	]
	if existing:
		return
	web_item.append("website_item_groups", {"item_group": item_group})
