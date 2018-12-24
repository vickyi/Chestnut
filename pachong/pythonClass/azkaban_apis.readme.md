# 工具说明

此工具是调用 azkaban 的 api 来实现的。

想了解详细，请查阅官方文档，https://azkaban.github.io/azkaban/docs/latest/#ajax-api OR https://azkaban.readthedocs.io/en/latest/ajaxApi.html#

关于此工具：

1. 如果是内网本地运行，使用：internet_url = "http://azkaban.your_com_addr.com"

2. 如果在 azkaban 环境下运行，使用：outernet_url = "http://outernet_url:port"。(注意要换成正确的主机地址和端口)

3. 测试可以使用：python azkaban_apis.py -m flush_flow -p flow_test -f flow_test --start_date 2018-12-15 --end_date 2018-12-20