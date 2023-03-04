def post_install_set_require_zip_for_belgium(cr, registry):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    env["res.country"].search([("code", "=", "BE")]).write({"zip_required": True, "enforce_cities": True})
