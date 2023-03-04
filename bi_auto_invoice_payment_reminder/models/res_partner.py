from odoo import api, fields, models, _


class Paymenthistoryline(models.Model):
	_name = "payment.history.line"
	_description = "Payment History Line"

	partner_id = fields.Many2one('res.partner',
		string='Customer')
	invoice_ref = fields.Char(string='Invoice')
	mail_date =fields.Date(string="Mail Date")
	mail_template= fields.Many2one('mail.template' , string="Email Template" )
	due_date = fields.Date(string="Due Date")

	


class ResPartner(models.Model):
	_inherit = "res.partner"


	payment_reminder_ids = fields.One2many('payment.history.line', 'partner_id' , string='Payment History Lines')



	


	