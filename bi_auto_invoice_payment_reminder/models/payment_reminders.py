from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo.http import request



class PaymentReminder(models.Model):
	_name = "payment.reminder"
	_description = "Payment Reminder"
	_rec_name = "name_seq"


	name_seq = fields.Char(string="Name" , index=True , copy=False , default=lambda self:_('New'))
	reminder = fields.Selection([
        ('before', 'Before Due Date'), 
        ('after', 'After Due date')],
        string='Reminder Selection', required=True)

	
	reminder_day = fields.Integer(string="Days")
	company_id = fields.Many2one('res.company', string='Company' , required=True)
	mail_template= fields.Many2one('mail.template' , string="Mail Template" )
	
	@api.model
	def create(self , vals):
		if vals.get('name_seq',_('New')) == ('New'):
			vals['name_seq'] = self.env['ir.sequence'].next_by_code('payment.reminder.sequence')
		
		result = super(PaymentReminder , self).create(vals)
		return result


	@api.model
	def _run_before_payment_due_date(self):

		su_id = self.env['res.partner'].browse(SUPERUSER_ID)
		for invoice_id in self.env['account.move'].search([('invoice_date' , '!=' , None),('state','in', ['posted']),('move_type', '=', 'out_invoice')]):
			for pay_id in self.env['res.config.settings'].sudo().search([],order="id desc", limit=1):
				for rem_days in self.env['payment.reminder'].search([('reminder_day' , '!=' , None),('reminder' , '=' , 'before')]):
					count_day = rem_days.reminder_day
					reminder_date = invoice_id.invoice_date - relativedelta(days=count_day)
					today = datetime.now().date()
					if reminder_date < today and pay_id.payment_reminder == True:
						if invoice_id:
								template_id = self.env['ir.model.data']._xmlid_lookup('bi_auto_invoice_payment_reminder.email_template_reminder_before_payment_notification')[2]
								email_template_obj = self.env['mail.template'].browse(template_id)
								values = email_template_obj.generate_email(invoice_id.id, fields=['subject' , 'body_html' , 'email_from' , 'email_to' , 'partner_to' , 'email_cc' , 'reply_to'])
								values['email_from'] = su_id.email
								values['email_to'] = invoice_id.partner_id.email
								values['res_id'] = False
								values['author_id'] = self.env['res.users'].browse(request.env.uid).partner_id.id
								mail_mail_obj = self.env['mail.mail']
								msg_id = mail_mail_obj.sudo().create(values)
								invoice_id.partner_id.update({'payment_reminder_ids' :

								[(0,0, {
                                                'partner_id':invoice_id.partner_id.id,
                                                'invoice_ref':invoice_id.name,
                                                'mail_date': datetime.today(),
                                                'mail_template' : email_template_obj.id,
                                                'due_date' : invoice_id.invoice_date,
                                        })]})

								if msg_id:
									msg_id.sudo().send()

		return True


	@api.model
	def _run_after_payment_due_date(self):
		
		su_id = self.env['res.partner'].browse(SUPERUSER_ID)
		for invoice in self.env['account.move'].search([('invoice_date' , '!=' , None),('state','in', ['posted']),('move_type', '=', 'out_invoice')]):
			for payment_id in self.env['res.config.settings'].sudo().search([],order="id desc", limit=1):
				for re_days in self.env['payment.reminder'].search([('reminder_day' , '!=' , None),('reminder' , '=' , 'after')]):
					count_day = re_days.reminder_day
					reminder_date = invoice.invoice_date + relativedelta(days=count_day)
					today = datetime.now().date()
					if reminder_date > today and payment_id.payment_reminder == True :
						
						if invoice:
								template_id = self.env['ir.model.data']._xmlid_lookup('bi_auto_invoice_payment_reminder.email_template_reminder_after_payment_notification')[2]
								email_template_obj = self.env['mail.template'].browse(template_id)
								values = email_template_obj.generate_email(invoice.id, fields=['subject' , 'body_html' , 'email_from' , 'email_to' , 'partner_to' , 'email_cc' , 'reply_to'])
								values['email_from'] = su_id.email
								values['email_to'] = invoice.partner_id.email
								values['res_id'] = False
								values['author_id'] = self.env['res.users'].browse(request.env.uid).partner_id.id
								mail_mail_obj = self.env['mail.mail']
								msg_id = mail_mail_obj.sudo().create(values)
								invoice.partner_id.update({'payment_reminder_ids' :

								[(0,0, {
                                                'partner_id':invoice.partner_id.id,
                                                'invoice_ref':invoice.name,
                                                'mail_date': datetime.today(),
                                                'mail_template' : email_template_obj.id,
                                                'due_date' : invoice.invoice_date,
                                        })]})
								if msg_id:
									msg_id.sudo().send()

		return True	