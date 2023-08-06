import unittest

from decimal import Decimal

from dsmr_parser.objects import MBusObject, CosemObject
from dsmr_parser.parsers import TelegramParser
from dsmr_parser import telegram_specifications
from dsmr_parser import obis_references as obis
from test.example_telegrams import TELEGRAM_V2_2


telegram_cjandrasits  = r"""/ISK5\2M550T-1012

1-3:0.2.8(50)
0-0:1.0.0(200426223325S)
0-0:96.1.1(4530303434303037333832323436303139)
1-0:1.8.1(002130.115*kWh)
1-0:1.8.2(000245.467*kWh)
1-0:2.8.1(000000.000*kWh)
1-0:2.8.2(000000.000*kWh)
0-0:96.14.0(0001)
1-0:1.7.0(00.111*kW)
1-0:2.7.0(00.000*kW)
0-0:96.7.21(00005)
0-0:96.7.9(00003)
1-0:99.97.0(1)(0-0:96.7.19)(190326095015W)(0000002014*s)
1-0:32.32.0(00001)
1-0:52.32.0(00001)
1-0:72.32.0(00192)
1-0:32.36.0(00001)
1-0:52.36.0(00001)
1-0:72.36.0(00001)
0-0:96.13.0()
1-0:32.7.0(229.9*V)
1-0:52.7.0(229.2*V)
1-0:72.7.0(222.9*V)
1-0:31.7.0(000*A)
1-0:51.7.0(000*A)
1-0:71.7.0(001*A)
1-0:21.7.0(00.056*kW)
1-0:41.7.0(00.000*kW)
1-0:61.7.0(00.055*kW)
1-0:22.7.0(00.000*kW)
1-0:42.7.0(00.000*kW)
1-0:62.7.0(00.000*kW)
0-1:24.1.0(003)
0-1:96.1.0()
0-1:24.2.1(700101010000W)(00000000)
0-2:24.1.0(003)
0-2:96.1.0(4730303339303031393336393930363139)
0-2:24.2.1(200426223001S)(00246.138*m3)
!56DD
"""
sample = telegram_cjandrasits.replace('\n', '\r\n')

class DevTest(unittest.TestCase):

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V5, apply_checksum_validation=False)
        result = parser.parse(sample)

        # for r in result:
        #     print(r)

        print(result[obis.HOURLY_GAS_METER_READING])
        print(result.get(obis.HOURLY_GAS_METER_READING, 1))
        print(result.get(obis.HOURLY_GAS_METER_READING, 2))


        # # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        # assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1], CosemObject)
        # assert result[obis.ELECTRICITY_USED_TARIFF_1].unit == 'kWh'
        # assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1].value, Decimal)
        # assert result[obis.ELECTRICITY_USED_TARIFF_1].value == Decimal('1.001')
        #
        # # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        # assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2], CosemObject)
        # assert result[obis.ELECTRICITY_USED_TARIFF_2].unit == 'kWh'
        # assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2].value, Decimal)
        # assert result[obis.ELECTRICITY_USED_TARIFF_2].value == Decimal('1.001')
        #
        # # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        # assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1], CosemObject)
        # assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].unit == 'kWh'
        # assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value, Decimal)
        # assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value == Decimal('1.001')
        #
        # # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        # assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2], CosemObject)
        # assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].unit == 'kWh'
        # assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value, Decimal)
        # assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value == Decimal('1.001')
        #
        # # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        # assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF], CosemObject)
        # assert result[obis.ELECTRICITY_ACTIVE_TARIFF].unit is None
        # assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF].value, str)
        # assert result[obis.ELECTRICITY_ACTIVE_TARIFF].value == '0001'
        #
        # # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        # assert isinstance(result[obis.EQUIPMENT_IDENTIFIER], CosemObject)
        # assert result[obis.EQUIPMENT_IDENTIFIER].unit is None
        # assert isinstance(result[obis.EQUIPMENT_IDENTIFIER].value, str)
        # assert result[obis.EQUIPMENT_IDENTIFIER].value == '00000000000000'
        #
        # # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        # assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE], CosemObject)
        # assert result[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'
        # assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE].value, Decimal)
        # assert result[obis.CURRENT_ELECTRICITY_USAGE].value == Decimal('1.01')
        #
        # # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        # assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY], CosemObject)
        # assert result[obis.CURRENT_ELECTRICITY_DELIVERY].unit == 'kW'
        # assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY].value, Decimal)
        # assert result[obis.CURRENT_ELECTRICITY_DELIVERY].value == Decimal('0')
        #
        # # TEXT_MESSAGE_CODE (0-0:96.13.1)
        # assert isinstance(result[obis.TEXT_MESSAGE_CODE], CosemObject)
        # assert result[obis.TEXT_MESSAGE_CODE].unit is None
        #
        # # TEXT_MESSAGE (0-0:96.13.0)
        # assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        # assert result[obis.TEXT_MESSAGE].unit is None
        # assert result[obis.TEXT_MESSAGE].value is None
        #
        # # DEVICE_TYPE (0-x:24.1.0)
        # assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        # assert result[obis.DEVICE_TYPE].unit is None
        # assert isinstance(result[obis.DEVICE_TYPE].value, str)
        # assert result[obis.DEVICE_TYPE].value == '3'
        #
        # # EQUIPMENT_IDENTIFIER_GAS (0-x:96.1.0)
        # assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS], CosemObject)
        # assert result[obis.EQUIPMENT_IDENTIFIER_GAS].unit is None
        # assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS].value, str)
        # assert result[obis.EQUIPMENT_IDENTIFIER_GAS].value == '000000000000'
        #
        # # GAS_METER_READING (0-1:24.3.0)
        # assert isinstance(result[obis.GAS_METER_READING], MBusObject)
        # assert result[obis.GAS_METER_READING].unit == 'm3'
        # assert isinstance(result[obis.GAS_METER_READING].value, Decimal)
        # assert result[obis.GAS_METER_READING].value == Decimal('1.001')
