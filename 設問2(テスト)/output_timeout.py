# -*- coding: utf-8 -*-
import functions
import datetime
"""ファイルパス（コマンドライン引数にするかも）"""
file_path="./example_logfile.txt"

"""ファイルパスからログデータの入ったリストの生成"""
log_list=functions.file_read(file_path)
log_count=len(log_list)

"""問題が起こったサーバーの要素の箱"""
accident_number=0
accident_number_list=[]

"""問題サーバーの特定"""
for check_server in log_list:
    if check_server["Response_Time"] == -999:
        accident_number_list.append(accident_number)
    accident_number+=1


"""エラーの回数とエラーが連続したサーバーのインデックス番号を登録"""
error_continue_flag=[]
error_count=1

"""コンソールからタイムアウト制限回数を指定"""
limit_timeout_count=int(input("タイムアウト上限回数Nを設定してください："))

"""ネットワークがタイムアウトしたかどうか判定するフラグ"""
timeout_flag=0

"""復旧までの時間を特定"""
for i in accident_number_list:
    if i in error_continue_flag:
        None
    else:
        """"問題サーバーの具体的なIP、応答時間、到着時間の定義"""
        accident_server=log_list[i]
        accident_IP=accident_server["Private_Ip"]
        accident_time=accident_server["Arrive_Time"]
        accident_response_time=accident_server["Response_Time"]
        accident_prefix=functions.check_same_server(accident_IP)
        
        """復旧サーバーの特定"""
        for j in range(i+1,log_count):
            repair_candidate_server=log_list[j]#治った候補のIP、
            repair_candidate_IP=repair_candidate_server["Private_Ip"]
            repair_candidate_time=repair_candidate_server["Arrive_Time"]
            repair_candidate_response=repair_candidate_server["Response_Time"]
            repair_candidate_prefix=functions.check_same_server(repair_candidate_IP)
            
            """プレフィクスが同じときで復旧したときとできなかったときの分岐"""
            if repair_candidate_response!=-999:
                repair_time=repair_candidate_time-accident_time
                if limit_timeout_count<=error_count:
                    print("故障サーバーのIPアドレス:" + str(repair_candidate_IP))
                    print("故障期間:"+str(accident_time)+" -> "+str(repair_candidate_time))
                    print("\n")
                    timeout_flag=1
                    error_count=0
                break
            
            else:
                error_continue_flag.append(j)
                error_count+=1


if timeout_flag==0:
    print("Network has no accident.")
