
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from matricula.models import Enroll, Bill
from django.utils.translation import ugettext_lazy as _
from paypal.standard.ipn.signals import valid_ipn_received

from paypal.standard.models import ST_PP_COMPLETED
from datetime import datetime

@receiver(post_save, sender=Enroll)
def create_bill(sender, **kwargs):
    instance = kwargs['instance']
    # print (instance, "   Bingo##############################################")

    if not instance.bill_created and instance.enroll_finished:
        instance.bill_created = True
        Bill.objects.create(short_description=_("Enroll in %s" % (str(instance.group))),
                             description=_("""
                             User %s 
                             Enroll in %s
                             At %s
                            """ % (instance.student.username,
                                   str(instance.group),
                                   str(instance.enroll_date)
                                  )),
                            amount=instance.group.cost,
                            student=instance.student
                            )
        instance.save()


def paypal_bill_paid(sender, **kwargs):
    ipn_obj = sender
    print (ipn_obj.payment_status)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            bill = Bill.objects.get(pk=ipn_obj.invoice)
            bill.is_paid = True
            bill.paid_date = datetime.now()
            bill.save()
        except:
            pass
        
    print(ipn_obj.invoice, ipn_obj.payment_status, ipn_obj.pending_reason) 
    
valid_ipn_received.connect(paypal_bill_paid)