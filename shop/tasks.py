import time
from django.core.mail import send_mail
from celery import shared_task
from .models import Product
from django.db import connection
# from celery.decorators import periodic_task

EMAIL_HOST_USER = 'vdovin_site_mdm@mail.ru'

@shared_task
def increase_product_quantity_task(product_id):
    '''запускается из views MakeOrder'''
    time.sleep(20)
    try:
        product = Product.objects.get(id=product_id)
        product.amount += 10
        product.save()
    except Product.DoesNotExist:
        pass

# @shared_task
# def update_order_status():
#     orders = Order.objects.filter(status='active')
#     for order in orders:
#         order.status = 'updated'
#         order.save()

@shared_task
def test_task():
    print("Test task executed!")


def get_orders_status(id_status):
    '''Вспомогательня функция для получения списка заказов с соответственным
    id_status. Вызывается функцией check_orders (она уже периодически
    вызывается из celery'''
    try:
        with connection.cursor() as cursor:
            cursor.execute("select id from shop_order where status_id = %s and "
                           "flag_finish = false", [id_status])
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except:
        print('Error query in the function "get_orders_status"')
        return []

@shared_task
def process_order(end_status_id, order_id, start_status_id):
    '''вспомогательная ф-ия для изменения статусов заказов'''
    try:
        with connection.cursor() as cursor:
            cursor.execute("update shop_orderstatus set flag_finish = true, "
                           "date_finish = NOW() where order_id_id = %s and "
                           "status_id_id = %s", [order_id, start_status_id])
            cursor.execute("insert into shop_orderstatus(flag_finish, status_id_id, order_id_id, date_finish, date_strat)"
                           " values(false,  %s, %s, NOW(), NOW())", [end_status_id, order_id])
            return True
    except:
        print('Error query in the function "process_order"')
        return False


# @periodic_task(run_every=timedelta(minutes=10))
@shared_task
def check_orders():
    '''Вызывается из Celery каждые 10 минут. Если есть заказы меняет статус'''

    id_delivering = 2
    id_delivered = 4
    order_ids_three = get_orders_status(3)
    for order_id in order_ids_three:
        process_order.delay(id_delivering, order_id, 3)
    order_ids_two = get_orders_status(2)
    for order_id in order_ids_two:
        process_order.delay(id_delivered, order_id, 2)



def check_delivered_orders():
    '''Вспомогательная функция, для определения Заказов, которые доставлены.
    Нужна для формирования списка кортожей кому необходимо отрпавить email'''
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT email, name, shop_order.id AS order_id FROM shop_customuser \
                INNER JOIN shop_order ON shop_customuser.id = shop_order.user_id \
                INNER JOIN shop_orderstatus so ON shop_order.id = so.order_id_id \
                WHERE so.flag_finish = false AND so.status_id_id = 4;")
            rows = cursor.fetchall()
    except:
        print('Error query in the function "check_delivered_orders"')
        rows = []
    return rows


def send_delivery_email(email, name, order_id):
    '''Вспомогательная функция для отправки почты'''

    subject = "Ваш заказ доставлен"
    message = f"[{name}] ваш заказ [{order_id}] доставлен. \n"\
              f"Поздравляю Вы сделали виртуальную покупку в моем портфолио. " \
              f"Спасибо за уделенное время. Если у вас есть предложения по " \
              f"работе сайта или предложения участвовать в ваших проектах " \
              f"пишите и звоните мне, контактные данные есть в 'подвале' сайта"
    from_email = EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def update_order_status():
    '''Вспомогательная функция для обновления информации о доставленных
    заказах. Ставится True в колонке flag_Finish'''

    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE shop_orderstatus SET flag_finish = true, date_finish = NOW() \
                WHERE flag_finish = false AND status_id_id = 4;")
            cursor.execute("SELECT ROW_COUNT();")
            row_count = cursor.fetchone()[0]
    except:
        row_count = []
        print('Error query in the function "update_order_status"')
    return row_count

@shared_task
def process_delivered_orders():
    '''Функция, которая вызывается через Celery каждые 10 минут'''

    orders = check_delivered_orders()
    for order in orders:
        send_delivery_email.delay(order[0], order[1], order[2])
    updated_orders_count = update_order_status()
    return f"{len(orders)} delivered orders processed, {updated_orders_count} order statuses updated."