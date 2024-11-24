# Author: liqixin
# Mail: hi@qixinlee.com
# Web: https://www.qixinlee.com

import streamlit as st
import pandas as pd
import json
import logging
import os
import re
from datetime import datetime
from typing import List, Dict

# 设置日志级别和格式
logging.basicConfig(filename='log.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# 定义日志解析器的基类
class LogParser:
    def __init__(self, log_file: bytes):
        self.log_file = log_file

    def _parse_log(self, log_pattern: re.Pattern) -> List[Dict]:
        parsed_log_entries = []
        for line in self.log_file:
            line = line.decode('utf-8')
            match = log_pattern.findall(line)
            if match:
                for match_item in match:
                    request = match_item[3]
                    request_parts = request.split(' ', 2)
                    if len(request_parts) == 3:
                        request_method, request_url, http_protocol = request_parts
                    else:
                        request_method = request_parts[0]
                        request_url = ''
                        http_protocol = ''
                    parsed_log_entries.append({
                        'remote_addr': match_item[0],
                        'remote_user': match_item[1],
                        'time_local': match_item[2],
                        'request_method': request_method,
                        'request_url': request_url,
                        'http_protocol': http_protocol,
                        'status': match_item[4],
                        'body_bytes_sent': match_item[5],
                        'http_referer': match_item[6],
                        'http_user_agent': match_item[7]
                    })
        return parsed_log_entries

    def parse(self) -> List[Dict]:
        raise NotImplementedError("必须实现解析方法")

# Apache 日志解析器
class ApacheLogParser(LogParser):
    def parse(self) -> List[Dict]:
        log_pattern = re.compile(r'(\S+) - (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', re.DOTALL)
        return self._parse_log(log_pattern)

# Nginx 日志解析器
class NginxLogParser(LogParser):
    def parse(self) -> List[Dict]:
        log_pattern = re.compile(r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', re.DOTALL)
        return self._parse_log(log_pattern)

# IIS 日志解析器
class IISLogParser(LogParser):
    def parse(self) -> List[Dict]:
        log_pattern = re.compile(r'(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', re.DOTALL)
        return self._parse_log(log_pattern)

# Tomcat 日志解析器
class TomcatLogParser(LogParser):
    def parse(self) -> List[Dict]:
        log_pattern = re.compile(r'(\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"', re.DOTALL)
        return self._parse_log(log_pattern)

# 通用日志解析方法
class LogParserFactory:
    @staticmethod
    def create_parser(log_type: str, log_file: bytes) -> LogParser:
        if log_type == 'Apache':
            return ApacheLogParser(log_file)
        elif log_type == 'Nginx':
            return NginxLogParser(log_file)
        elif log_type == 'IIS':
            return IISLogParser(log_file)
        elif log_type == 'Tomcat':
            return TomcatLogParser(log_file)
        else:
            raise ValueError(f"不支持的日志类型: {log_type}")

# 定义导出文件函数
def export_file(df: pd.DataFrame, export_format: str) -> str:
    try:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if export_format == 'CSV（逗号分隔值）':
            csv_file_path = f'log_entries_{current_time}.csv'
            df.to_csv(csv_file_path, index=False)
            return csv_file_path
        elif export_format == 'JSON（JavaScript对象表示法）':
            json_file_path = f'log_entries_{current_time}.json'
            df['time_local'] = df['time_local'].apply(lambda x: x.isoformat())
            df['date'] = df['date'].apply(lambda x: x.isoformat())
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(df.to_dict(orient='records'), json_file, indent=4)
            return json_file_path
    except Exception as e:
        logging.error(f"导出文件失败：{e}")
        raise

# 定义Web应用程序
def main():
    # 设置主题
    st.set_page_config(layout="wide", page_title="安全运营 - Web日志分析工具")
    st.markdown("<style>body {background-color: #2F4F4F; color: #66D9EF;}</style>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>安全运营 - Web日志分析工具</h1>", unsafe_allow_html=True)

    # 上传日志文件
    st.subheader('请选择日志文件')
    log_file = st.file_uploader('请选择日志文件', type=['log'])
    log_type = st.selectbox("请选择日志类型", ['Apache', 'Nginx', 'IIS', 'Tomcat'])

    if log_file is not None:
        try:
            # 使用工厂模式创建适当的日志解析器
            log_parser = LogParserFactory.create_parser(log_type, log_file)
            parsed_log_entries = log_parser.parse()

            if parsed_log_entries:
                # 日志解析结果
                st.subheader('日志解析结果')
                df = pd.DataFrame(parsed_log_entries)
                df['time_local'] = df['time_local'].apply(lambda x: datetime.strptime(x, '%d/%b/%Y:%H:%M:%S %z'))
                df['date'] = df['time_local'].dt.date
                st.write(df)

                # 选择日期范围
                st.subheader('请选择日期范围')
                col1, col2 = st.columns(2)
                start_date = col1.date_input('请选择开始日期')
                end_date = col2.date_input('请选择结束日期')
                filtered_df = df[(df['time_local'].dt.date >= start_date) & 
                                 (df['time_local'].dt.date <= end_date)]

                # 筛选功能
                st.subheader('筛选功能')
                st.subheader('请选择筛选条件')
                columns = filtered_df.columns.tolist()
                select_columns = st.multiselect('请选择筛选字段', columns)
                select_values = {}
                for column in select_columns:
                    if column == 'date':
                        select_values[column] = st.date_input(f'请选择{column}值')
                    else:
                        select_values[column] = st.selectbox(f'请选择{column}值', filtered_df[column].unique())
                filtered_df = filtered_df
                for column, value in select_values.items():
                    if column == 'date':
                        filtered_df = filtered_df[filtered_df[column] == value]
                    else:
                        filtered_df = filtered_df[filtered_df[column] == value]

                st.write(filtered_df)

                # 统计功能
                st.subheader('统计功能')
                rank_columns = filtered_df.columns.tolist()
                rank_columns_selected = st.multiselect('请选择统计字段', rank_columns)

                if rank_columns_selected:
                    for i, column in enumerate(rank_columns_selected):
                        rank_df = filtered_df[column].value_counts().reset_index()
                        rank_df.columns = [column, '次数']
                        
                        if i % 2 == 0:
                            col1, col2 = st.columns(2)
                            col1.write(rank_df)
                        else:
                            col2.write(rank_df)
                else:
                    st.write("请选择至少一个字段")
                
                # 导出文件功能
                st.subheader('请选择导出格式')
                export_format = st.selectbox('请选择导出格式', ['CSV（逗号分隔值）', 'JSON（JavaScript对象表示法）'])
                if export_format:
                    file_path = export_file(filtered_df, export_format)
                    with open(file_path, 'rb') as file:
                        if export_format == 'CSV（逗号分隔值）':
                            st.download_button('下载CSV文件', file, file_path.split('/')[-1])
                        elif export_format == 'JSON（JavaScript对象表示法）':
                            st.download_button('下载JSON文件', file, file_path.split('/')[-1])

            else:
                st.error('没有匹配的日志条目')
        except Exception as e:
            st.error(f"错误：{e}")

if __name__ == '__main__':
    main()
