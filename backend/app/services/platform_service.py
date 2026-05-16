import random
from datetime import date, datetime, timedelta
from decimal import Decimal

from app.models import PlatformType


ROOM_TYPES = ["标准单人间", "标准双人间", "大床房", "豪华套房", "商务房"]
ROOM_NUMBERS = [f"{floor}{room}" for floor in range(2, 7) for room in range(1, 11)]


def generate_mock_sales_data(
    hotel_id: int,
    platform: PlatformType,
    start_date: date,
    end_date: date,
) -> list[dict]:
    """模拟从各平台拉取的销售数据"""
    delta = (end_date - start_date).days
    num_orders = random.randint(max(delta, 1) * 2, max(delta, 1) * 5)
    orders = []
    for i in range(num_orders):
        check_in = start_date + timedelta(days=random.randint(0, max(delta - 1, 0)))
        stay = random.randint(1, 4)
        check_out = check_in + timedelta(days=stay)
        amount = Decimal(str(round(random.uniform(200, 1500), 2)))
        commission_rate = Decimal(str(round(random.uniform(0.08, 0.15), 2)))
        commission = round(amount * commission_rate, 2)
        net_amount = round(amount - commission, 2)
        order = {
            "hotel_id": hotel_id,
            "platform": platform,
            "order_no": f"{platform.value.upper()}{check_in.strftime('%Y%m%d')}{i:04d}",
            "check_in": check_in,
            "check_out": check_out,
            "room_no": random.choice(ROOM_NUMBERS),
            "room_type": random.choice(ROOM_TYPES),
            "amount": amount,
            "commission": commission,
            "net_amount": net_amount,
            "source": "auto",
            "pulled_at": datetime.now(),
        }
        orders.append(order)
    return orders


def pull_platform_data(
    hotel_id: int,
    platform: PlatformType,
    start_date: date,
    end_date: date,
) -> list[dict]:
    """拉取单个平台数据，后续可替换为真实API调用"""
    return generate_mock_sales_data(hotel_id, platform, start_date, end_date)
