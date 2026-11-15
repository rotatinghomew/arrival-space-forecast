# 业务数据与接口

event_at 为业务发生时刻，known_at 为首次进入业务服务的时刻；同一 site、event_at 的更正由更晚 known_at 覆盖。cutoff 之前不可知的记录不能用于该时刻的预测。occupied 为占用数，capacity 为名义容量。

closures 是带发布时间的关闭泊位计划，可能减少有效容量。movements 的出入数是各设备时间格内流量，不能无条件与 occupancy 当作完全同源精确观测。

POST /v1/asof 接收 revision、at；按 known_at 返回当时可见的占用及关闭计划，不携带之后更正。合作方的候选集合和到达时间均是查询参数，不是固定配置。

## 资料发布

GET /v1/catalog 返回 revision、cutoff、settings 以及表名。GET /v1/tables/表名 按 revision、offset、limit 分页。默认 31 行，最多 100 行；next=null 表示结束。错误版本返回 409，参数错误返回 400，领域查询不可计算时返回 422。资料从 JSON 加载后对当前实例不可变；重启可换一个发布版本。

所有时间均为带 +08:00 的 ISO 8601 字符串，资料窗口用半开区间，只有免费时长阈值明确包含端点。计数为非负整数；null 表示未观察或未知，不等于零。来源分页顺序不是业务先后顺序。来源参数 revision 必须与资料一致。

业务服务现有 GET /v1/summary、GET /v1/reports/标识和 GET /health。概览保留 revision 和 cutoff，store.py 对规范 JSON 计算 SHA-256，内容相同重复读取不会产生不同标识。新的研究结果可独立扩展，不应改变现有概览指标的含义。
