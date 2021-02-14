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


"""復旧サーバーを特定出来たら次の問題サーバーへ移る"""

error_continue_flag=[]
"""復旧までの時間を特定"""
for i in accident_number_list:
    if i in error_continue_flag == False :#もしエラーが続いていなかったら
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
            if  repair_candidate_prefix == accident_prefix:
                if repair_candidate_response!=-999:
                    repair_time=repair_candidate_time-accident_time
                    print("Repaired Ip is " + str(repair_candidate_IP))
                    print("Time spends" + str(repair_time.seconds)+"sec")
                    print("\n")
                    break
            
                else:
                    error_continue_flag.append(j)
    
            