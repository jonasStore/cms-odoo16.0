{
    'name': 'Auto Invoice Payment Reminders',
    'version': '16.0.0.0',
    'category': 'Accounting',
    'summary': 'Auto Invoice Payment Reminders Odoo App helps users to configure payment reminders for before due date and after due date with selection of mail template and set days. User can see the reminder mail will be send to the customers before and after due date. User can also view payment reminder history customer wise.',
    
    'depends': ['base','account'],
    
    'data': [
    
        'security/ir.model.access.csv',
        'data/payment_data_views.xml',
        'data/remider_alert_mail_data.xml',
        'data/remider_alert_cron.xml',
        'views/payment_reminder_views.xml',
        'views/res_config_views.xml',
        'views/res_partner_views.xml',
      
    ],
    'license' : 'OPL-1',
    'installable': True,
    'auto_install': False,
    
}
