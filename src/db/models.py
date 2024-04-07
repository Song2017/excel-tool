from sqlalchemy import Column, VARCHAR, TIMESTAMP, Integer, Float, DateTime, String, Table, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Factorder(Base):
    __tablename__ = 'factorder'

    id = Column(VARCHAR(255), primary_key=True)
    brand = Column(VARCHAR(255), index=True)
    channel = Column(VARCHAR(255))
    receiveProvince = Column(VARCHAR(255))
    receiveCity = Column(VARCHAR(255))
    receiverDistrict = Column(VARCHAR(255))
    receiveAddress = Column(VARCHAR(255))
    userId = Column(VARCHAR(255))
    customerId = Column(VARCHAR(255))
    orderId = Column(VARCHAR(255))
    createTime = Column(TIMESTAMP)
    orderDate = Column(TIMESTAMP)
    orderCompleteTime = Column(TIMESTAMP)
    storeId = Column(VARCHAR(255))
    storeName = Column(VARCHAR(255))
    items = Column(Integer)
    amount = Column(Float(asdecimal=True))
    tradePrice = Column(Float(asdecimal=True))
    discount = Column(Float(asdecimal=True))
    orderNum = Column(Integer)
    orderType = Column(Integer)
    isVisitorSales = Column(Integer)
    isGroupSales = Column(Integer)
    employeeNo = Column(VARCHAR(255))
    employee = Column(VARCHAR(255))
    couponId = Column(VARCHAR(255))
    couponName = Column(VARCHAR(255))
    refundAmount = Column(Float(asdecimal=True))


class Dimcustomer(Base):
    __tablename__ = 'dimcustomer'

    brand = Column(VARCHAR(255))
    userId = Column(VARCHAR(255), primary_key=True)
    source = Column(VARCHAR(255))
    customerId = Column(VARCHAR(255))
    customerName = Column(VARCHAR(255))
    mobile = Column(VARCHAR(255))
    mobileValId = Column(Integer)
    gender = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    birthday = Column(DateTime)
    unionId = Column(VARCHAR(255))
    paidMember = Column(Integer)
    smsContact = Column(Integer)
    emailContact = Column(Integer)
    telContact = Column(Integer)
    wechatContact = Column(Integer)
    wechatBindDate = Column(TIMESTAMP)
    openId = Column(VARCHAR(255))
    tmallBindDate = Column(TIMESTAMP)
    tmallId = Column(VARCHAR(255))
    registTime = Column(DateTime)
    registChannel = Column(VARCHAR(255))
    registChannelId = Column(VARCHAR(255))
    registChannelName = Column(VARCHAR(255))
    channelTag = Column(VARCHAR(255))
    registStore = Column(VARCHAR(255))
    regSaName = Column(VARCHAR(255))
    regStoreId = Column(VARCHAR(255))
    regSa = Column(VARCHAR(255))
    manageStore = Column(VARCHAR(255))
    manageStoreId = Column(VARCHAR(255))
    firstOrderDate = Column(TIMESTAMP)
    lastOrderDate = Column(TIMESTAMP)
    lastStoreId = Column(VARCHAR(255))
    lastOrderName = Column(VARCHAR(255))
    lastSA = Column(VARCHAR(255))
    lastSAName = Column(VARCHAR(255))
    totalPoints = Column(Integer)
    availablePoints = Column(Integer)
    freezePoints = Column(Integer)
    manageSAName = Column(VARCHAR(255))
    manageSA = Column(VARCHAR(255))
    memberLevel = Column(VARCHAR(255))
    tierBeginDate = Column(TIMESTAMP)
    tierEndDate = Column(TIMESTAMP)
    tierNextDiffAmount = Column(Integer)
    tierRemindAmount = Column(Integer)
    tierRemindDate = Column(TIMESTAMP)
    expirePoints = Column(Integer)
    expireDate = Column(TIMESTAMP)


metadata_db = MetaData()

t_coupon_redeemed = Table(
    'coupon_redeemed', metadata_db,
    Column('brand', String(255)),
    Column('customerid', String(255)),
    Column('couponcode', String(255)),
    Column('couponId', String(255)),
    Column('couponname', String(255)),
    Column('type', String(255)),
    Column('status', String(255)),
    Column('receive_time', String(255)),
    Column('expired_time', String(255)),
    Column('redept_time', String(255)),
    Column('redept_storename', String(255)),
    Column('redept_storeid', String(255)),
    Column('redept_orderid', String(255))
)

t_factorderitem = Table(
    'factorderitem', metadata_db,
    Column('tradeId', VARCHAR(255), index=True),
    Column('brand', VARCHAR(255), nullable=False, index=True),
    Column('channel', VARCHAR(255)),
    Column('userId', VARCHAR(255)),
    Column('customerId', VARCHAR(255)),
    Column('orderId', VARCHAR(255)),
    Column('createTime', TIMESTAMP),
    Column('orderDate', TIMESTAMP),
    Column('orderCompleteTime', TIMESTAMP),
    Column('storeId', VARCHAR(255)),
    Column('storeName', VARCHAR(255)),
    Column('sku', VARCHAR(255)),
    Column('productId', VARCHAR(255)),
    Column('outSkuId', VARCHAR(255)),
    Column('goodsNumber', VARCHAR(255)),
    Column('productName', VARCHAR(255)),
    Column('items', Float(asdecimal=True)),
    Column('unitPrice', Float(asdecimal=True)),
    Column('originalPrice', Float(asdecimal=True)),
    Column('discount', Float(asdecimal=True)),
    Column('amount', Float(asdecimal=True)),
    Column('orderType', Integer, nullable=False),
    Column('isSample', Integer, nullable=False),
    Column('isVisitorSales', Integer, nullable=False)
)
