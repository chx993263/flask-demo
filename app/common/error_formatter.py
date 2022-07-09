import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


def load_error_codes():
    """
    从本地文件读取错误定义文件
    TODO: 以后可以优化，从配置中心读取，比如从Redis 或者 API
    """
    code_file_tsv = os.path.join(basedir, "..", "files", "error_msg.tsv")
    code_file_csv = os.path.join(basedir, "..", "files", "error_msg.csv")
    if os.path.exists(code_file_csv):
        df = pd.read_csv(code_file_csv)
    elif os.path.exists(code_file_tsv):
        df = pd.read_csv(code_file_tsv, sep='\t')

    df['Source Code'] = df['Source Code'].fillna(0).astype(int).astype(str)

    return df


def find_and_format_error(
        msg, code=None, apl_code=None, need_formated=True, msg_detail=None):
    """
    code: source code, e.g. toutiao code/kuaishou code etc.
    apl_code: proname internal code
    msg_detail: additional info(a dict) to format err msg

    根据code & msg 去寻找对应的错误代码
    1. 如果code不为空，则先用code搜索
    2. msg不能为空，用msg再做精细匹配
    3. 将匹配过程写到日志之中
    """
    tmp_df = load_error_codes()
    tmp_df['source_msg'] = msg.lower()

    if code:
        tmp_df = tmp_df[tmp_df['Source Code'] == str(code)]

    def detect(row):
        # match err using proname Code first
        if apl_code and row['APL Code'] == str(apl_code):
            return True
        source_msg = row['source_msg'].lower().strip()
        pattern = row['Pattern'].lower().strip()
        logger.debug(f"pattern={pattern} source_msg={source_msg} : {pattern in source_msg}")
        if pattern in source_msg:
            return True
        return False

    if tmp_df.shape[0] == 0:
        return None

    tmp_df['is_detected'] = tmp_df.apply(detect, axis=1)
    tmp_df = tmp_df[tmp_df['is_detected'] == True]

    if tmp_df.shape[0] == 1:
        row = tmp_df.to_dict('records')[0]
        cn_msg = row['CN_Msg']
        if msg_detail:
            msg = msg.format(**msg_detail)
            cn_msg = cn_msg.format(**msg_detail)
        ret = {
            "raw_msg": msg,
            "apl_code": row['APL Code'],
            "cn_msg": cn_msg,
            "cn_solution": row['CN_Solution']
        }
        if need_formated:
            return format_msg(ret)
        else:
            return ret
    else:
        return None


def format_msg(err_info):
    msg = f"""
    {err_info['raw_msg']}
    错误代码：{err_info['apl_code']}
    错误原因：{err_info['cn_msg']}
    解决方案：{err_info['cn_solution']}
    """
    msg = [x.strip() for x in msg.splitlines() if x.strip()]
    msg = "\n".join(msg)
    return msg


if __name__ == '__main__':
    ret = find_and_format_error(msg='Access token is invalid, when you call '
                                    'access_token or refresh_token api, '
                                    'old token will become invalid', code='40105')
    print(ret)
