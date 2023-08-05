__all__ = ('SmsMTSPoint', 'SmsMTS2Point', 'SmsToReferralPoint')

from expressmoney_service.api import *

_SERVICE = 'services'


class _SmsMTSCreateContract(Contract):
    message = serializers.CharField(max_length=60)


class _SmsMTS2CreateContract(Contract):
    message = serializers.CharField(max_length=69)


class _SmsToReferralCreateContract(Contract):
    message = serializers.CharField(max_length=130)
    phone_number = serializers.CharField(max_length=20)


class _SmsMTSResponseContract(_SmsMTSCreateContract):
    pass


class _SmsMTSID(ID):
    _service = _SERVICE
    _app = 'sms_mts'
    _view_set = 'sms_mts'


class _SmsMTS2ID(ID):
    _service = _SERVICE
    _app = 'sms_mts'
    _view_set = 'sms_mts2'


class _SmsToReferralID(ID):
    _service = _SERVICE
    _app = 'sms_mts'
    _view_set = 'sms_to_referral'


class SmsMTSPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = _SmsMTSID()
    _create_contract = _SmsMTSCreateContract
    _response_contract = _SmsMTSResponseContract


class SmsMTS2Point(CreatePointMixin, ContractPoint):
    _point_id = _SmsMTS2ID()
    _create_contract = _SmsMTS2CreateContract


class SmsToReferralPoint(CreatePointMixin, ContractPoint):
    _point_id = _SmsToReferralID()
    _create_contract = _SmsToReferralCreateContract
