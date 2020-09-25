# encoding: UTF-8
from vnpy.api.xtp.vnxtpmd import MdApi
from vnpy.api.xtp.vnxtptd import TdApi
import os

setting = {
    "账号": "53191002029",
    "密码": "ZHewL6Ct",
    "客户号": "1",
    "交易地址": "120.27.164.69",
    "交易端口": 6001,
    "行情地址": "120.27.164.138",
    "行情端口": 6002,
    "行情协议": "TCP",
    "授权码": "b8aa7173bba3470e390d787219b2112e",
}


class XtpTdApi(TdApi):
    """"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def onDisconnected(self, session: int, reason: int):
        """"""
        print("onDisconnected", reason)

    def onError(self, data):
        """"""
        print('onError', data)

    def onOrderEvent(self, data, error, session):
        """"""
        pass

    def onTradeEvent(self, data, session):
        """"""
        pass

    def onCancelOrderError(self, data, error, session):
        """"""
        print('onCancelOrderError', data, error, session)

    def onQueryOrder(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryOrderByPage(self, data, req_count, order_sequence, query_reference, reqid, last, session):
        """"""
        pass

    def onQueryTrade(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryTradeByPage(self, data, req_count, trade_sequence, query_reference, reqid, last, session):
        """"""
        pass

    def onQueryPosition(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryAsset(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryStructuredFund(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryFundTransfer(self, data, error, reqid, last, session):
        """"""
        pass

    def onFundTransfer(self, data, error, session):
        """"""
        pass

    def onQueryETF(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryETFBasket(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryIPOInfoList(self, data, error, reqid, last, session):
        """"""
        pass

    def onQueryIPOQuotaInfo(self, data, error, reqid, last, session):
        """"""
        pass

    # 请求查询期权合约的响应，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线
    def onQueryOptionAuctionInfo(self, data, error, reqid, last, session):
        """"""
        pass


class XtpMdApi(MdApi):
    """"""

    def __init__(self):
        """Constructor"""
        super(XtpMdApi, self).__init__()
        # 当客户端与行情后台通信连接断开时，该方法被调用。
        # @param reason 错误原因，请与错误代码表对应
        # @remark api不会自动重连，当断线发生时，请用户自行选择后续操作。可以在此函数中调用Login重新登录。注意用户重新登录后，需要重新订阅行情

    def onDisconnected(self, reason):
        """"""
        print('onDisconnected', reason)

        # 错误应答
        # @param data 当服务器响应发生错误时的具体的错误代码和错误信息，当data为空，或者data.error_id为0时，表明没有错误
        # @remark 此函数只有在服务器发生错误时才会调用，一般无需用户处理

    def onError(self, data):
        """"""
        print('onError', data)

        # 订阅行情应答，包括股票、指数和期权
        # @param data 详细的合约订阅情况
        # @param error 订阅合约发生错误时的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        # @remark 每条订阅的合约均对应一条订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onSubMarketData(self, data, error, last):
        """"""
        print('onSubMarketData', data, error)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码（不包含交易所信息）例如"600000"
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订行情应答，包括股票、指数和期权
        # @param data 详细的合约取消订阅情况
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次取消订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        # @remark 每条取消订阅的合约均对应一条取消订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onUnSubMarketData(self, data, error, last):
        """"""
        print('onUnSubMarketData', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码（不包含交易所信息）例如"600000"
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 深度行情通知，包含买一卖一队列
        # @param data 行情数据
        # @param bid1_qty_list 买一队列数据
        # @param bid1_counts 买一队列的有效委托笔数
        # @param max_bid1_count 买一队列总委托笔数
        # @param ask1_qty_list 卖一队列数据
        # @param ask1_count 卖一队列的有效委托笔数
        # @param max_ask1_count 卖一队列总委托笔数
        # @remark 需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onDepthMarketData(self, data, bid1_qty_list, bid1_counts, max_bid1_count, ask1_qty_list, ask1_count,
                          max_ask1_count):
        """"""
        print('onDepthMarketData', data, bid1_qty_list, bid1_counts, max_bid1_count, ask1_qty_list, ask1_count,
              max_ask1_count)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码（不包含交易所信息）
        print("data['last_price']:", data['last_price'])  # 最新价
        print("data['pre_close_price']:", data['pre_close_price'])  # 昨收盘价
        print("data['open_price']:", data['open_price'])  # 今开盘价
        print("data['high_price']:", data['high_price'])  # 最高价
        print("data['low_price']:", data['low_price'])  # 最低价
        print("data['close_price']:", data['close_price'])  # 今收盘价
        print("data['pre_total_long_positon']:", data['pre_total_long_positon'])  # 期权数据昨日持仓量
        print("data['total_long_positon']:", data['total_long_positon'])  # 持仓量
        print("data['pre_settl_price']:", data['pre_settl_price'])  # 昨日结算价
        print("data['settl_price']:", data['settl_price'])  # 今日结算价
        print("data['upper_limit_price']:", data['upper_limit_price'])  # 涨停价
        print("data['lower_limit_price']:", data['lower_limit_price'])  # 跌停价
        print("data['pre_delta']:", data['pre_delta'])  # 预留
        print("data['curr_delta']:", data['curr_delta'])  # 预留
        print("data['data_time']:", data['data_time'])  # 时间类，格式为YYYYMMDDHHMMSSsss
        print("data['qty']:", data['qty'])  # 数量，为总成交量（单位股，与交易所一致）
        print("data['turnover']:", data['turnover'])  # 成交金额，为总成交金额（单位元，与交易所一致）
        print("data['avg_price']:", data['avg_price'])  # 当日均价
        print("data['trades_count']:", data['trades_count'])  # 成交笔数
        print("data['ticker_status']:", data['ticker_status'])  # 当前交易状态说明
        print("data['ask']:", data['ask'])  # 十档申卖价
        print("data['bid']:", data['bid'])  # 十档申买价
        print("data['bid_qty']:", data['bid_qty'])  # 十档申买量
        print("data['ask_qty']:", data['ask_qty'])  # 十档申卖量
        print("data['data_type']:", data['data_type'])  # 0-现货(股票/基金/债券等) 1-期权
        if data['data_type'] == 0:
            print("data['total_bid_qty']:", data['total_bid_qty'])  # 委托买入总量
            print("data['total_ask_qty']:", data['total_ask_qty'])  # 委托卖出总量
            print("data['ma_bid_price']:", data['ma_bid_price'])  # 加权平均委买价格
            print("data['ma_ask_price']:", data['ma_ask_price'])  # 加权平均委卖价格
            print("data['ma_bond_bid_price']:", data['ma_bond_bid_price'])  # 债券加权平均委买价格
            print("data['ma_bond_ask_price']:", data['ma_bond_ask_price'])  # 债券加权平均委卖价格
            print("data['yield_to_maturity']:", data['yield_to_maturity'])  # 债券到期收益率
            print("data['iopv']:", data['iopv'])  # 基金实时参考净值
            print("data['etf_buy_count']:", data['etf_buy_count'])  # ETF申购笔数(SH)
            print("data['etf_sell_count']:", data['etf_sell_count'])  # ETF赎回笔数(SH)
            print("data['etf_buy_qty']:", data['etf_buy_qty'])  # ETF申购数量(SH)
            print("data['etf_buy_money']:", data['etf_buy_money'])  # ETF申购金额(SH)
            print("data['etf_sell_qty']:", data['etf_sell_qty'])  # ETF赎回数量(SH)
            print("data['etf_sell_money']:", data['etf_sell_money'])  # ETF赎回金额(SH)
            print("data['total_warrant_exec_qty']:", data['total_warrant_exec_qty'])  # 权证执行的总数量(SH)
            print("data['warrant_lower_price']:", data['warrant_lower_price'])  # 权证跌停价格（元）(SH)
            print("data['warrant_upper_price']:", data['warrant_upper_price'])  # 权证涨停价格（元）(SH)
            print("data['cancel_buy_count']:", data['cancel_buy_count'])  # 买入撤单笔数(SH)
            print("data['cancel_sell_count']:", data['cancel_sell_count'])  # 卖出撤单笔数(SH)
            print("data['cancel_buy_qty']:", data['cancel_buy_qty'])  # 买入撤单数量(SH)
            print("data['cancel_sell_qty']:", data['cancel_sell_qty'])  # 卖出撤单数量(SH)
            print("data['cancel_buy_money']:", data['cancel_buy_money'])  # 买入撤单金额(SH)
            print("data['cancel_sell_money']:", data['cancel_sell_money'])  # 卖出撤单金额(SH)
            print("data['total_buy_count']:", data['total_buy_count'])  # 买入总笔数(SH)
            print("data['total_sell_count']:", data['total_sell_count'])  # 卖出总笔数(SH)
            print("data['duration_after_buy']:", data['duration_after_buy'])  # 买入委托成交最大等待时间(SH)
            print("data['duration_after_sell']:", data['duration_after_sell'])  # 卖出委托成交最大等待时间(SH)
            print("data['num_bid_orders']:", data['num_bid_orders'])  # 买方委托价位数(SH)
            print("data['num_ask_orders']:", data['num_ask_orders'])  # 卖方委托价位数(SH)
            print("data['pre_iopv']:", data['pre_iopv'])  # 基金T-1日净值(SZ)
            print("data['r1']:", data['r1'])  # 预留
            print("data['r2']:", data['r2'])  # 预留
        else:
            print("data['auction_price']:", data['auction_price'])  # 波段性中断参考价(SH)
            print("data['auction_qty']:", data['auction_qty'])  # 波段性中断集合竞价虚拟匹配量(SH)
            print("data['last_enquiry_time']:", data['last_enquiry_time'])  # 最近询价时间(SH)

        # 订阅行情订单簿应答，包括股票、指数和期权
        # @param data 详细的合约订阅情况
        # @param error 订阅合约发生错误时的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        # @remark 每条订阅的合约均对应一条订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onSubOrderBook(self, data, error, last):
        """"""
        print('onSubOrderBook', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码（不包含交易所信息）例如"600000"
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订行情订单簿应答，包括股票、指数和期权
        # @param data 详细的合约取消订阅情况
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次取消订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        # @remark 每条取消订阅的合约均对应一条取消订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onUnSubOrderBook(self, data, error, last):
        """"""
        print('onUnSubOrderBook', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码（不包含交易所信息）例如"600000"
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 行情订单簿通知，包括股票、指数和期权
        # @param data 行情订单簿数据，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onOrderBook(self, data):
        """"""
        print('onOrderBook', data)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码
        print("data['data_time']:", data['data_time'])  # 时间类
        print("data['last_price']:", data['last_price'])  # 最新价
        print("data['qty']:", data['qty'])  # 数量，为总成交量
        print("data['turnover']:", data['turnover'])  # 成交金额，为总成交金额
        print("data['trades_count']:", data['trades_count'])  # 成交笔数
        print("data['ask']:", data['ask'])  # 十档申卖价
        print("data['bid']:", data['bid'])  # 十档申买价
        print("data['bid_qty']:", data['bid_qty'])  # 十档申买量
        print("data['ask_qty']:", data['ask_qty'])  # 十档申卖量

        # 订阅逐笔行情应答，包括股票、指数和期权
        # @param data 详细的合约订阅情况
        # @param error 订阅合约发生错误时的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        # @remark 每条订阅的合约均对应一条订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onSubTickByTick(self, data, error, last):
        """"""
        print('onSubTickByTick', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订逐笔行情应答，包括股票、指数和期权
        # @param data 详细的合约取消订阅情况
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次取消订阅的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应
        # @remark 每条取消订阅的合约均对应一条取消订阅应答，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onUnSubTickByTick(self, data, error, last):
        """"""
        print('onUnSubTickByTick', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 逐笔行情通知，包括股票、指数和期权
        # @param data 逐笔行情数据，包括逐笔委托和逐笔成交，此为共用结构体，需要根据type来区分是逐笔委托还是逐笔成交，需要快速返回，否则会堵塞后续消息，当堵塞严重时，会触发断线

    def onTickByTick(self, data):
        """"""
        print('onTickByTick', data)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码
        print("data['data_time']:", data['data_time'])  # 委托时间 or 成交时间
        print("data['type']:", data['type'])  # 1委托 or 2成交
        if data['type'] == 1:
            print("data['channel_no']:", data['channel_no'])  # 频道代码
            print("data['seq']:", data['seq'])  # 委托序号
            print("data['price']:", data['price'])  # 委托价格
            print("data['qty']:", data['qty'])  # 委托数量
            print("data['side']:", data['side'])  # '1':买; '2':卖; 'G':借入; 'F':出借
            print("data['ord_type']:", data['ord_type'])  # 订单类别: '1': 市价; '2': 限价; 'U': 本方最优
        else:
            print("data['channel_no']:", data['channel_no'])  # 频道代码
            print("data['seq']:", data['seq'])  # 委托序号(在同一个channel_no内唯一，从1开始连续)
            print("data['price']:", data['price'])  # 成交价格
            print("data['qty']:", data['qty'])  # 成交量
            print("data['money']:", data['money'])  # 成交金额(仅适用上交所)
            print("data['bid_no']:", data['bid_no'])  # 买方订单号
            print("data['ask_no']:", data['ask_no'])  # 卖方订单号
            print("data['trade_flag']:",
                  data['trade_flag'])  # SH: 内外盘标识('B':主动买; 'S':主动卖; 'N':未知)SZ: 成交标识('4':撤; 'F':成交)

        # 订阅全市场的股票行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onSubscribeAllMarketData(self, exchange_id, error):
        """"""
        print('onSubscribeAllMarketData', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订全市场的股票行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onUnSubscribeAllMarketData(self, exchange_id, error):
        """"""
        print('onUnSubscribeAllMarketData', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 订阅全市场的股票行情订单簿应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onSubscribeAllOrderBook(self, exchange_id, error):
        """"""
        print('onSubscribeAllOrderBook', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订全市场的股票行情订单簿应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onUnSubscribeAllOrderBook(self, exchange_id, error):
        """"""
        print('onUnSubscribeAllOrderBook', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 订阅全市场的股票逐笔行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onSubscribeAllTickByTick(self, exchange_id, error):
        """"""
        print('onSubscribeAllTickByTick', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订全市场的股票逐笔行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onUnSubscribeAllTickByTick(self, exchange_id, error):
        """"""
        print('onUnSubscribeAllTickByTick', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 查询可交易合约的应答
        # @param data 可交易合约信息
        # @param error 查询可交易合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次查询可交易合约的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应

    def onQueryAllTickers(self, data, error, last):
        """"""
        print('onQueryAllTickers', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码
        print("data['ticker_name']:", data['ticker_name'])  # 合约名称
        print("data['ticker_type']:", data['ticker_type'])  # 合约类型
        print("data['pre_close_price']:", data['pre_close_price'])  # 昨收盘
        print("data['upper_limit_price']:", data['upper_limit_price'])  # 涨停板价
        print("data['lower_limit_price']:", data['lower_limit_price'])  # 跌停板价
        print("data['price_tick']:", data['price_tick'])  # 最小变动价位
        print("data['buy_qty_unit']:", data['buy_qty_unit'])  # 合约最小交易量
        print("data['sell_qty_unit']:", data['sell_qty_unit'])  # 合约最小交易量
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 查询合约的最新价格信息应答
        # @param data 可交易合约信息
        # @param error 查询可交易合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @param last 是否此次查询可交易合约的最后一个应答，当为最后一个的时候为true，如果为false，表示还有其他后续消息响应

    def onQueryTickersPriceInfo(self, data, error, last):
        """"""
        print('onQueryTickersPriceInfo', data, error, last)
        print("data['exchange_id']:", data['exchange_id'])  # 交易所代码
        print("data['ticker']:", data['ticker'])  # 合约代码
        print("data['last_price']:", data['last_price'])  # 最新价
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 订阅全市场的期权行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onSubscribeAllOptionMarketData(self, exchange_id, error):
        """"""
        print('onSubscribeAllOptionMarketData', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订全市场的期权行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onUnSubscribeAllOptionMarketData(self, exchange_id, error):
        """"""
        print('onUnSubscribeAllMarketData', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 订阅全市场的期权行情订单簿应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onSubscribeAllOptionOrderBook(self, exchange_id, error):
        """"""
        print('onSubscribeAllOptionOrderBook', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订全市场的期权行情订单簿应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onUnSubscribeAllOptionOrderBook(self, exchange_id, error):
        """"""
        print('onUnSubscribeAllOptionOrderBook', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 订阅全市场的期权逐笔行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # @param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onSubscribeAllOptionTickByTick(self, exchange_id, error):
        """"""
        print('onSubscribeAllOptionTickByTick', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])

        # 退订全市场的期权逐笔行情应答
        # @param exchange_id 表示当前全订阅的市场，如果为XTP_EXCHANGE_UNKNOWN(3)，表示沪深全市场，XTP_EXCHANGE_SH(1)表示为上海全市场，XTP_EXCHANGE_SZ(2)表示为深圳全市场
        # param error 取消订阅合约时发生错误时返回的错误信息，当error为空，或者error.error_id为0时，表明没有错误
        # @remark 需要快速返回

    def onUnSubscribeAllOptionTickByTick(self, exchange_id, error):
        """"""
        print('onUnSubscribeAllOptionTickByTick', exchange_id, error)
        print("error['error_id']):", error['error_id'])
        print("error['error_msg']):", error['error_msg'])


from settings import xtp_login_info


class MyXtpApi():
    def __init__(self):
        self.td_api = XtpTdApi()
        self.md_api = XtpMdApi()
        self.session = 0

    def connect(self):
        self.md_api.createQuoteApi(2, os.getcwd())
        n = self.md_api.login(xtp_login_info["行情ip"], xtp_login_info['行情port'], xtp_login_info["user"],
                              xtp_login_info["password"], xtp_login_info["protocol"])
        if n != 0:
            print("行情服务器登录失败", n)
            print(self.md_api.getApiLastError())
        elif n == 0:
            print("行情服务器登录成功")
        # 创建TraderApi
        self.td_api.createTraderApi(1, os.getcwd())
        # 订阅流
        # self.td_api.logout(self.session)
        self.td_api.subscribePublicTopic(0)
        # set key
        self.td_api.setSoftwareKey(xtp_login_info["key"])
        # 版本
        self.td_api.setSoftwareVersion(xtp_login_info["version"])
        self.session = self.td_api.login(xtp_login_info["交易ip"], xtp_login_info["交易port"], xtp_login_info["user"],
                                         xtp_login_info["password"], xtp_login_info["protocol"])
        if not self.session:
            print("交易服务器登录失败")
            print(self.td_api.getApiLastError())
        elif self.session:
            print("交易服务器登录成功")


if __name__ == '__main__':
    api = MyXtpApi()
    api.connect()
    n = api.md_api.subscribeMarketData("000002", 1, 1)
    print(n)
