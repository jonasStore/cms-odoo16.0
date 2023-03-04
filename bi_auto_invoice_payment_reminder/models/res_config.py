from odoo import api, fields, models, _



class ResConfigSettings(models.TransientModel):
	_inherit = "res.config.settings"



	payment_reminder=fields.Boolean(string="Enable payment Reminder", default=False)



	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		payment_reminder = self.env["ir.config_parameter"].sudo().get_param("bi_auto_invoice_payment_reminder.payment_reminder")
		
		res.update(
			payment_reminder=payment_reminder,	
		)
		return res



	def set_values(self):
	  res = super(ResConfigSettings, self).set_values()
	  config_env=self.env['ir.config_parameter'].sudo()
	  config_env.set_param("bi_auto_invoice_payment_reminder.payment_reminder", self.payment_reminder)