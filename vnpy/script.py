import os

from api.xtp.vnxtpmd import MdApi
from api.xtp.vnxtptd import TdApi

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
    def __init__(self):
        """"""
        super().__init__()

    def onDisconnected(self, session: int, reason: int) -> None:
        """"""
        self.connect_status = False
        self.login_status = False
        self.gateway.write_log(f"交易服务器连接断开, 原因{reason}")

        self.login_server()

    def onError(self, error: dict) -> None:
        """"""
        self.gateway.write_error("交易接口报错", error)

    def onOrderEvent(self, data: dict, error: dict, session: int) -> None:
        """"""
        if error["error_id"]:
            self.gateway.write_error("交易委托失败", error)

        symbol = data["ticker"]
        if len(symbol) == 8:
            direction = DIRECTION_OPTION_XTP2VT[data["side"]]
            offset = OFFSET_XTP2VT[data["position_effect"]]
        else:
            direction, offset = DIRECTION_STOCK_XTP2VT[data["side"]]

        orderid = str(data["order_xtp_id"])
        if orderid not in self.orders:
            timestamp = str(data["insert_time"])
            dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S%f")
            dt = CHINA_TZ.localize(dt)

            order = OrderData(
                symbol=symbol,
                exchange=MARKET_XTP2VT[data["market"]],
                orderid=orderid,
                type=ORDERTYPE_XTP2VT[data["price_type"]],
                direction=direction,
                offset=offset,
                price=data["price"],
                volume=data["quantity"],
                traded=data["qty_traded"],
                status=STATUS_XTP2VT[data["order_status"]],
                datetime=dt,
                gateway_name=self.gateway_name
            )
            self.orders[orderid] = order
        else:
            order = self.orders[orderid]
            order.traded = data["qty_traded"]
            order.status = STATUS_XTP2VT[data["order_status"]]

        self.gateway.on_order(order)

    def onTradeEvent(self, data: dict, session: int) -> None:
        """"""
        symbol = data["ticker"]
        if len(symbol) == 8:
            direction = DIRECTION_OPTION_XTP2VT[data["side"]]
            offset = OFFSET_XTP2VT[data["position_effect"]]
        else:
            direction, offset = DIRECTION_STOCK_XTP2VT[data["side"]]

        timestamp = str(data["trade_time"])
        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S%f")
        dt = CHINA_TZ.localize(dt)

        trade = TradeData(
            symbol=symbol,
            exchange=MARKET_XTP2VT[data["market"]],
            orderid=str(data["order_xtp_id"]),
            tradeid=str(data["exec_id"]),
            direction=direction,
            offset=offset,
            price=data["price"],
            volume=data["quantity"],
            datetime=dt,
            gateway_name=self.gateway_name
        )

        if trade.orderid in self.orders:
            order = self.orders[trade.orderid]
            order.traded += trade.volume

            if order.traded < order.volume:
                order.status = Status.PARTTRADED
            else:
                order.status = Status.ALLTRADED

            self.gateway.on_order(order)
        else:
            self.gateway.write_log(f"成交找不到对应委托{trade.orderid}")

        self.gateway.on_trade(trade)

    def onCancelOrderError(self, data: dict, error: dict, session: int) -> None:
        """"""
        if not error or not error["error_id"]:
            return

        self.gateway.write_error("撤单失败", error)

    def onQueryOrder(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryTrade(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryPosition(
            self,
            data: dict,
            error: dict,
            request: int,
            last: bool,
            session: int
    ) -> None:
        """"""
        if data["market"] == 0:
            return

        position = PositionData(
            symbol=data["ticker"],
            exchange=MARKET_XTP2VT[data["market"]],
            direction=POSITION_DIRECTION_XTP2VT[data["position_direction"]],
            volume=data["total_qty"],
            frozen=data["locked_position"],
            price=data["avg_price"],
            pnl=data["unrealized_pnl"],
            yd_volume=data["yesterday_position"],
            gateway_name=self.gateway_name
        )
        self.gateway.on_position(position)

    def onQueryAsset(
            self,
            data: dict,
            error: dict,
            request: int,
            last: bool,
            session: int
    ) -> None:
        """"""
        account = AccountData(
            accountid=self.userid,
            balance=data["total_asset"],
            frozen=data["withholding_amount"],
            gateway_name=self.gateway_name
        )

        if data["account_type"] == 1:
            self.margin_trading = True
        elif data["account_type"] == 2:
            account.available = data["buying_power"]
            account.frozen = account.balance - account.available
            self.option_trading = True

        self.gateway.on_account(account)

    def onQueryStructuredFund(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryFundTransfer(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onFundTransfer(self, data: dict, session: int) -> None:
        """"""
        pass

    def onQueryETF(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryETFBasket(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryIPOInfoList(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryIPOQuotaInfo(self, data: dict, error: dict, last: bool, session: int) -> None:
        """"""
        pass

    def onQueryOptionAuctionInfo(self, data: dict, error: dict, reqid: int, last: bool, session: int) -> None:
        """"""
        if not data or not data["ticker"]:
            return

        contract = ContractData(
            symbol=data["ticker"],
            exchange=MARKET_XTP2VT[data["security_id_source"]],
            name=data["symbol"],
            product=Product.OPTION,
            size=data["contract_unit"],
            min_volume=data["qty_unit"],
            pricetick=data["price_tick"],
            gateway_name=self.gateway_name
        )

        contract.option_portfolio = data["underlying_security_id"] + "_O"
        contract.option_underlying = (
                data["underlying_security_id"]
                + "-"
                + str(data["delivery_month"])
        )
        contract.option_type = OPTIONTYPE_XTP2VT.get(data["call_or_put"], None)

        contract.option_strike = data["exercise_price"]
        contract.option_expiry = datetime.strptime(
            str(data["last_trade_date"]), "%Y%m%d"
        )
        contract.option_index = get_option_index(
            contract.option_strike, data["contract_id"]
        )

        self.gateway.on_contract(contract)
        symbol_pricetick_map[contract.vt_symbol] = contract.pricetick

        if last:
            self.gateway.write_log("期权信息查询成功")

    def onQueryCreditDebtInfo(
            self,
            data: dict,
            error: dict,
            request: int,
            last: bool,
            session: int
    ) -> None:
        """"""
        if data["debt_type"] == 1:
            symbol = data["ticker"]
            exchange = MARKET_XTP2VT[data["market"]]

            position = self.short_positions.get(symbol, None)
            if not position:
                position = PositionData(
                    symbol=symbol,
                    exchange=exchange,
                    direction=Direction.SHORT,
                    gateway_name=self.gateway_name
                )
                self.short_positions[symbol] = position

            position.volume += data["remain_qty"]

        if last:
            for position in self.short_positions.values():
                self.gateway.on_position(position)

            self.short_positions.clear()

    def connect(
            self,
            userid: str,
            password: str,
            client_id: int,
            server_ip: str,
            server_port: int,
            software_key: str
    ) -> None:
        """"""

        self.userid = userid
        self.password = password
        self.client_id = client_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.software_key = software_key
        self.protocol = PROTOCOL_VT2XTP["TCP"]

        # Create API object
        if not self.connect_status:
            path = str(get_folder_path(self.gateway_name.lower()))
            self.createTraderApi(self.client_id, path)

            self.setSoftwareKey(self.software_key)
            self.subscribePublicTopic(0)
            self.login_server()
        else:
            self.gateway.write_log("交易接口已登录，请勿重复操作")

    def login_server(self) -> None:
        """"""
        n = self.login(
            self.server_ip,
            self.server_port,
            self.userid,
            self.password,
            self.protocol
        )

        if n:
            self.session_id = n
            self.connect_status = True
            self.login_status = True
            msg = f"交易服务器登录成功, 会话编号：{self.session_id}"
            self.init()
        else:
            error = self.getApiLastError()
            msg = f"交易服务器登录失败，原因：{error['error_msg']}"

        self.gateway.write_log(msg)

    def close(self) -> None:
        """"""
        if self.connect_status:
            self.exit()

    def query_option_info(self) -> None:
        """"""
        self.reqid += 1
        self.queryOptionAuctionInfo({}, self.session_id, self.reqid)

    def send_order(self, req: OrderRequest) -> str:
        """"""
        if req.exchange not in MARKET_VT2XTP:
            self.gateway.write_log(f"委托失败，不支持的交易所{req.exchange.value}")
            return ""

        if req.type not in ORDERTYPE_VT2XTP:
            self.gateway.write_log(f"委托失败，不支持的委托类型{req.type.value}")
            return ""

        if self.margin_trading and req.offset == Offset.NONE:
            self.gateway.write_log(f"委托失败，两融交易需要选择开平方向")
            return ""

        # check for option type
        if len(req.symbol) == 8:
            xtp_req = {
                "ticker": req.symbol,
                "market": MARKET_VT2XTP[req.exchange],
                "price": req.price,
                "quantity": int(req.volume),
                "side": DIRECTION_OPTION_VT2XTP.get(req.direction, ""),
                "position_effect": OFFSET_VT2XTP[req.offset],
                "price_type": ORDERTYPE_VT2XTP[req.type],
                "business_type": 10
            }

        # stock type
        else:
            xtp_req = {
                "ticker": req.symbol,
                "market": MARKET_VT2XTP[req.exchange],
                "price": req.price,
                "quantity": int(req.volume),
                "price_type": ORDERTYPE_VT2XTP[req.type],
            }

            if self.margin_trading:
                xtp_req["side"] = DIRECTION_STOCK_VT2XTP.get((req.direction, req.offset), "")
                xtp_req["business_type"] = 4
            else:
                xtp_req["side"] = DIRECTION_STOCK_VT2XTP.get((req.direction, Offset.NONE), "")
                xtp_req["business_type"] = 0

        orderid = self.insertOrder(xtp_req, self.session_id)

        order = req.create_order_data(str(orderid), self.gateway_name)
        self.gateway.on_order(order)

        return order.vt_orderid

    def cancel_order(self, req: CancelRequest) -> None:
        """"""
        self.cancelOrder(int(req.orderid), self.session_id)

    def query_account(self) -> None:
        """"""
        if not self.connect_status:
            return

        self.reqid += 1
        self.queryAsset(self.session_id, self.reqid)

    def query_position(self) -> None:
        """"""
        if not self.connect_status:
            return

        self.reqid += 1
        self.queryPosition("", self.session_id, self.reqid)

        if self.margin_trading:
            self.reqid += 1
            self.queryCreditDebtInfo(self.session_id, self.reqid)
if __name__ == '__main__':
    api=XtpTdApi()
    createTraderApi = api.createTraderApi(1, os.getcwd())
    print('createTraderApi', createTraderApi)

    subscribePublicTopic = api.subscribePublicTopic(0)
    setSoftwareKey = api.setSoftwareKey("b8aa7173bba3470e390d787219b2112e")
    setSoftwareVersion = api.setSoftwareVersion("test111")
    print(setSoftwareKey)
    print(setSoftwareVersion)
    r = api.my_login()
    if r:
        print(r)
    else:
        error = api.getApiLastError()
        msg = f"交易服务器登录失败，原因：{error['error_msg']}"
        print(msg)
