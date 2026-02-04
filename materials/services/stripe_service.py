import stripe
import os
from django.conf import settings


def get_stripe_client():
    """Инициализация клиента Stripe"""
    # Пробуем разные варианты названий переменных
    stripe_api_key = os.getenv('STRIPE_SECRET_KEY') or os.getenv('STRIPE_API_KEY')
    
    if not stripe_api_key:
        raise ValueError("STRIPE_SECRET_KEY или STRIPE_API_KEY не установлены в переменных окружения")
    
    stripe.api_key = stripe_api_key
    return stripe


def create_stripe_product(name, description=""):
    """
    Создание продукта в Stripe
    
    Args:
        name (str): Название продукта
        description (str): Описание продукта
    Returns:
        str: ID созданного продукта или None в случае ошибки
    """
    try:
        stripe = get_stripe_client()
        product = stripe.Product.create(
            name=name,
            description=description[:500]  # Ограничиваем длину описания
        )
        return product.id
    except Exception as e:
        print(f"Ошибка при создании продукта Stripe: {e}")
        return None


def create_stripe_price(product_id, amount, currency="rub"):
    """
    Создание цены в Stripe
    
    Args:
        product_id (str): ID продукта в Stripe
        amount (float): Сумма (в рублях)
        currency (str): Валюта (по умолчанию 'rub')
    
    Returns:
        str: ID созданной цены или None в случае ошибки
    """
    try:
        stripe = get_stripe_client()
        # Конвертируем рубли в копейки/центы
        unit_amount = int(float(amount) * 100)
        
        price = stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,
            currency=currency.lower(),
        )
        return price.id
    except Exception as e:
        print(f"Ошибка при создании цены Stripe: {e}")
        return None

def create_stripe_checkout_session(price_id, success_url, cancel_url, customer_email=None):
    """
    Создание сессии оплаты в Stripe
    
    Args:
        price_id (str): ID цены в Stripe
        success_url (str): URL для перенаправления после успешной оплаты
        cancel_url (str): URL для перенаправления при отмене оплаты
        customer_email (str): Email покупателя (опционально)
    
    Returns:
        dict: Данные сессии или None в случае ошибки
    """
    try:
        stripe = get_stripe_client()
        
        session_params = {
            'payment_method_types': ['card'],
            'line_items': [{
                'price': price_id,
                'quantity': 1,
            }],
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
        }
        
        if customer_email:
            session_params['customer_email'] = customer_email
        
        session = stripe.checkout.Session.create(**session_params)
        
        return {
            'id': session.id,
            'url': session.url,
            'payment_intent': session.payment_intent,
        }
    except Exception as e:
        print(f"Ошибка при создании сессии Stripe: {e}")
        return None
def get_stripe_session_status(session_id):
    """
    Получение статуса сессии оплаты
    
    Args:
        session_id (str): ID сессии Stripe
    
    Returns:
        dict: Данные о статусе или None в случае ошибки
    """
    try:
        stripe = get_stripe_client()
        session = stripe.checkout.Session.retrieve(session_id)
        
        return {
            'id': session.id,
            'payment_status': session.payment_status,
            'status': session.status,
            'payment_intent': session.payment_intent,
            'customer_email': session.customer_details.get('email') if session.customer_details else None,
        }
    except Exception as e:
        print(f"Ошибка при получении статуса сессии Stripe: {e}")
        return None


def retrieve_stripe_payment(payment_intent_id):
    """
    Получение информации о платеже
    
    Args:
        payment_intent_id (str): ID платежа в Stripe
    
    Returns:
        dict: Данные платежа или None в случае ошибки
    """
    try:
        stripe = get_stripe_client()
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        return {
            'id': payment_intent.id,
            'amount': payment_intent.amount / 100,  # Конвертируем обратно в рубли
            'currency': payment_intent.currency,
            'status': payment_intent.status,
            'created': payment_intent.created,
        }
    except Exception as e:
        print(f"Ошибка при получении платежа Stripe: {e}")
        return None

"""
ВНИМАНИЕ: Для работы требуется реальный API ключ Stripe.
В тестовом режиме используется мок-версия.

Чтобы переключиться на реальный Stripe:
1. Получите ключи на https://dashboard.stripe.com/
2. Добавьте в .env:
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
3. Установите USE_MOCK_STRIPE=False

Тестовые карты для Stripe:
- Номер: 4242 4242 4242 4242
- Срок: любая будущая дата
- CVC: любые 3 цифры
"""
