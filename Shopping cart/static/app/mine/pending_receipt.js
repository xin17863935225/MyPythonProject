$(function () {
    // 存在收款按钮
    if ($('#receipt')) {
        $('#receipt').click(function () {
            $this = $(this);
            urlPath = "/axf/changeOrderStatu";
            ordernumber = $this.attr("orderNumber");
            $.getJSON(urlPath, {"ordernumber": ordernumber, "status": 3}, function (data) {
                if (data["code"] == 200) {//请求成功
                    window.open("/axf/pending_receipt", target = "_self")
                }
            });
        });
    }

});





























