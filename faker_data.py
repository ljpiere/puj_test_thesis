from faker import Faker
import random
import pandas as pd
import numpy as np
from datetime import timedelta

fake = Faker('es_ES')

def generar_clientes(n):
    clientes = []
    for i in range(n):
        clientes.append({
            'cliente_id': i + 1,
            'nombre': fake.name(),
            'direccion': fake.address(),
            'fecha_registro': fake.date_between(start_date='-5y', end_date='today')
        })
    return pd.DataFrame(clientes)

def generar_transacciones(clientes, n_transacciones, drift=False):
    transacciones = []
    for i in range(n_transacciones):
        # Selecciona un cliente aleatoriamente
        cliente = random.choice(clientes.to_dict('records'))
        fecha_transaccion = fake.date_between(start_date=cliente['fecha_registro'], end_date='today')
        
        # Configuración de parámetros base
        if not drift:
            monto = np.random.normal(loc=100, scale=20)
        else:
            monto = np.random.normal(loc=150, scale=30)
        monto = max(round(monto, 2), 0.01)
        
        # Generación de atributos adicionales
        transaccion = {
            'transaction_id': f"T{i+1:07d}",                          # ID único de transacción
            'cliente_id': cliente['cliente_id'],                        # ID del cliente
            'transaction_date': fecha_transaccion,                      # Fecha de la transacción
            'transaction_type': random.choice(['débito', 'crédito', 'transferencia', 'pago online']),
            'amount': monto,                                            # Monto de la transacción
            'currency': random.choice(['USD', 'EUR', 'GBP']),
            'merchant_id': f"M{random.randint(1000, 9999)}",             # ID del comerciante
            'merchant_name': fake.company(),                            # Nombre del comerciante
            'merchant_category': random.choice(['Alimentos', 'Tecnología', 'Ropa', 'Entretenimiento', 'Salud']),
            'terminal_id': f"TERM{random.randint(100, 999)}",            # ID de terminal
            'card_type': random.choice(['Visa', 'MasterCard', 'Amex']),
            'card_last4': str(random.randint(1000, 9999)),               # Últimos 4 dígitos de la tarjeta
            'transaction_status': random.choice(['aprobada', 'pendiente', 'fallida']),
            'device': random.choice(['móvil', 'desktop', 'tablet']),
            'ip_address': fake.ipv4(),
            'country': fake.country(),
            'city': fake.city(),
            'postal_code': fake.postcode(),
            'latitude': round(random.uniform(-90, 90), 6),
            'longitude': round(random.uniform(-180, 180), 6),
            'branch_id': f"B{random.randint(10, 99)}",
            'branch_name': fake.company(),
            'payment_method': random.choice(['chip', 'contactless', 'online']),
            'discount_applied': random.choice([True, False]),
            'loyalty_points': random.randint(0, 500),
            'exchange_rate': round(random.uniform(0.8, 1.2), 4),
            'fee_amount': round(random.uniform(0, 5), 2),
            'tax_amount': round(random.uniform(0, 3), 2),
            'tip_amount': round(random.uniform(0, 10), 2),
            'refund_flag': random.choice([True, False]),
            'original_transaction_id': None,  # Se podría asignar si refund_flag es True
            'device_type': random.choice(['móvil', 'tablet', 'desktop']),
            'operating_system': random.choice(['Android', 'iOS', 'Windows', 'Linux', 'macOS']),
            'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
            'app_version': f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
            'transaction_channel': random.choice(['online', 'in-person']),
            'payment_processor': random.choice(['Stripe', 'PayPal', 'Square', 'Adyen']),
            'risk_score': round(random.uniform(0, 1), 4),
            'fraud_flag': random.choice([True, False]),
            'settlement_date': (fecha_transaccion + timedelta(days=random.randint(1, 5))).isoformat(),
            'account_balance_before': round(random.uniform(1000, 5000), 2),
            'account_balance_after': round(random.uniform(1000, 5000), 2),
            'narrative': fake.sentence(nb_words=10),
            'merchant_country': fake.country(),
            'merchant_city': fake.city(),
            'pos_entry_mode': random.choice(['chip', 'swipe', 'manual']),
            'authorization_code': fake.lexify(text='??????'),
            'settlement_status': random.choice(['settled', 'pending']),
            'loyalty_program': random.choice([True, False]),
            'promo_code': fake.bothify(text='PROMO-##??')
        }
        
        # Si la transacción es un reembolso, asigna un original_transaction_id
        if transaccion['refund_flag']:
            transaccion['original_transaction_id'] = f"T{random.randint(1, n_transacciones):07d}"
        
        transacciones.append(transaccion)
    
    return pd.DataFrame(transacciones)

# Parámetros para generar el dataset
n_clientes = 1000          # Ejemplo: 1,000 clientes
n_transacciones = 100000   # Ejemplo: 100,000 transacciones para el dataset base

# Generar clientes y transacciones sin drift
clientes_df = generar_clientes(n_clientes)
transacciones_df = generar_transacciones(clientes_df, n_transacciones, drift=False)

# Generar dataset con data drift
transacciones_drift_df = generar_transacciones(clientes_df, n_transacciones, drift=True)

# Mostrar estadísticas del atributo "amount" para observar el drift
print("Estadísticas de montos en dataset base:")
print(transacciones_df['amount'].describe())

print("\nEstadísticas de montos en dataset con data drift:")
print(transacciones_drift_df['amount'].describe())
