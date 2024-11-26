### 1. Web日志分析工具

**启动命令**  
`streamlit run www.py`

**启动命令 设置自定上传大小**  
`streamlit run www.py --server.maxUploadSize 1000`


**介绍**
1. **支持多种日志格式**：支持Apache、Nginx、IIS和Tomcat日志格式。
2. **自动识别日志格式**：自动识别日志格式，无需手动配置。
3. **高效分析**：快速分析大型日志文件，获取有关网站访问量、用户行为和系统性能的详细信息。
4. **灵活筛选**：支持多种筛选条件，例如日期范围、请求方法、请求URL等。
5. **详细统计**：支持多种统计条件，例如请求方法、请求URL、状态码等。
6. **导出文件**：支持导出CSV和JSON文件，方便进一步分析和处理。

**使用说明**

1. 上传日志文件：点击“上传日志文件”按钮，选择需要分析的日志文件。
2. 选择日志类型：选择日志类型，例如Apache、Nginx、IIS或Tomcat。
3. 等待日志解析完成：工具将自动解析日志文件，解析结果将以表格形式显示。
4. 选择日期范围：选择特定的日期范围来筛选日志条目。
5. 选择筛选条件：选择多个字段来筛选日志条目。
6. 查看筛选结果：筛选结果将以表格形式显示。
7. 选择统计字段：选择多个字段来统计日志条目。
8. 查看统计结果：统计结果将以表格形式显示。
9. 选择导出格式：选择导出格式，例如CSV或JSON。
10. 下载导出的文件：点击“下载导出的文件”按钮，下载导出的文件。

**注意事项**

- 请确保上传的日志文件格式正确。
- 请确保选择正确的日志类型。
- 请确保筛选条件正确。
- 请确保统计字段正确。
- 请确保导出格式正确。

---
### 2. 项目应用

1. **Web日志分析**：分析Web服务器日志文件，获取有关网站访问量、用户行为和系统性能的详细信息。
2. **安全运营**：分析Web服务器日志文件，检测和预防安全威胁，例如SQL注入、跨站脚本攻击等。
3. **网站性能优化**：分析Web服务器日志文件，优化网站性能，例如优化图片、压缩代码等。
4. **用户行为分析**：分析Web服务器日志文件，了解用户行为，例如用户访问路径、停留时间等。
5. **市场研究**：分析Web服务器日志文件，了解市场趋势，例如用户偏好、市场份额等。

---

### 3. 软件流程

#### 3.1 上传日志文件

* 选择日志类型，支持Apache、Nginx、IIS和Tomcat日志格式
* 通过Web页面上传日志文件

#### 3.2 程序自动解析日志文件

本工具支持Apache、Nginx、IIS和Tomcat日志格式
可以自动识别日志格式并解析日志条目。
日志解析结果将以表格形式显示，包括以下字段：

- remote_addr：访问者的IP地址
- remote_user：访问者的用户名
- time_local：访问时间
- request_method：请求方法
- request_url：请求的URL
- http_protocol：HTTP协议版本
- status：响应状态码
- body_bytes_sent：发送的字节数
- http_referer：referer头部
- http_user_agent：user-agent头部

#### 3.3 选择日期

* 以时间维度进行统计分析
* 根据需要选择分析的日志时间，程序自动进行筛选日志并在页面进行展现

#### 3.4 筛选功能

日志可以按照所选日期灵活的进行分析，包括以下字段

- remote_addr：访问者的IP地址
- remote_user：访问者的用户名
- time_local：访问时间
- request_method：请求方法
- request_url：请求的URL
- http_protocol：HTTP协议版本
- status：响应状态码
- body_bytes_sent：发送的字节数
- http_referer：referer头部
- http_user_agent：user-agent头部
#### 3.5 统计功能

* 统计次数，方便进行统计分析
* 日志可以按照所选日期灵活的进行统计，包括以下字段，可以多选

- remote_addr：访问者的IP地址
- remote_user：访问者的用户名
- time_local：访问时间
- request_method：请求方法
- request_url：请求的URL
- http_protocol：HTTP协议版本
- status：响应状态码
- body_bytes_sent：发送的字节数
- http_referer：referer头部
- http_user_agent：user-agent头部


#### 3.6 导出功能

支持导出CSV和JSON格式
