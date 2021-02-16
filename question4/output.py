# -*- coding: utf-8 -*-
from functions import *
import datetime
import sys


"""ファイルパスをコンソールから受付"""
file_path=sys.argv[1]

"""ファイルパスからログデータの入ったリストの生成"""
log_list=file_read(file_path)
log_count=len(log_list)

input_flag=True
"""コンソール入力"""
while(input_flag):
    N=abs(int(input("タイムアウト回数Nの上限を設定してください：")))#タイムアウトは何回までしていいか
    print("\n")
    m=abs(int(input("調べたい直近のログの数mを入力してください")))#最新から何個のデータをとるか
    print("\n")
    if N<=m:
        input_flag=False
    else:
        print("値はN<=mでなければなりません")
        print("\n")
    
t=abs(float(input("過負荷と認定する時間tを入力してください(単位はミリsec)")))#過負荷と認定する時間は何秒か
print("\n")


"""サーバーのIPアドレスの種類を数える"""
prefix_list=[]
prefix_count=0
for i in range(log_count):
    server=log_list[i]
    IP=server["Private_Ip"]
    prefix=check_same_server(IP)
    if prefix in prefix_list:
        None
    else:
        prefix_list.append(prefix)
        prefix_count+=1


"""各サーバーごとにloglistを振り分け"""        
new_log_list=split_each_server(log_list,prefix_count,prefix_list)
for i in range(prefix_count):
    new_log_list[i]=make_latest_m_list(new_log_list[i],m)    



"""メインループ：振り分けたloglistを各々調べていく"""
for log_list in new_log_list:
    """変数"""
    sum_arrive_time=0#合計応答時間
    ave_arrive_time=0#平均応答時間
    check_server_counter=0#通常運転と故障を振り分けるためのカウンター
    error_count=1#タイムアウトになった回数
    timeout_flag=0#ネットワークがタイムアウトしたかどうか判定するフラグ
    log_count=len(log_list)#現在のログリストにいくつ要素があるか
    
    
    """リスト"""
    normal_number_list=[]#通常サーバーのインデックス番号
    accident_number_list=[]#故障サーバーのインデックス番号
    error_continue_flag=[]#エラーの回数とエラーが連続したサーバーのインデックス番号を登録
    


    """問題サーバーの特定"""
    for check_server in log_list:
        if check_server["Response_Time"] == -999:
            accident_number_list.append(check_server_counter)        
        else:
            normal_number_list.append(check_server_counter)
        check_server_counter+=1
    
    accident_count=len(accident_number_list)#タイムアウト時の平均時間の分母
    normal_count=len(normal_number_list)#Ping正常時の平均時間の分母
    
    """直近の回数が各サーバーのログ数より多かった場合はmをサーバーのログ数に合わせる"""
    if m >=check_server_counter:
        m=check_server_counter

    """期間出力のための到着時間データ"""
    latest_log=log_list[m-1]["Arrive_Time"]#loglist内に含まれる直近の到着時間データ   
    oldest_log=log_list[0]["Arrive_Time"]#loglist内に含まれる最古の到着時間データ

    """Pingが返ってきたときのループ"""
    for i in normal_number_list:
        normal_server=log_list[i]
        normal_response_time=normal_server["Response_Time"]
        normal_IP=normal_server["Private_Ip"]
        """通常時の合計時間"""
        sum_arrive_time+=normal_response_time

    """タイムアウトの時のループ復旧までの時間を特定"""
    for i in accident_number_list:
        error_count=1
        if i in error_continue_flag:
            None
        else:
            """"問題サーバーの具体的なIP、応答時間、到着時間の定義"""
            accident_server=log_list[i]
            accident_IP=accident_server["Private_Ip"]
            accident_time=accident_server["Arrive_Time"]
            accident_response_time=accident_server["Response_Time"]
            accident_prefix=check_same_server(accident_IP)
            
            """復旧サーバーの特定"""
            for j in range(i+1,log_count):
                repair_candidate_server=log_list[j]#復旧した候補のIP、
                repair_candidate_IP=repair_candidate_server["Private_Ip"]
                repair_candidate_time=repair_candidate_server["Arrive_Time"]
                repair_candidate_response=repair_candidate_server["Response_Time"]
                repair_candidate_prefix=check_same_server(repair_candidate_IP)
                
                """復旧したときとできなかったときの分岐"""
                if repair_candidate_response!=-999:
                    repair_time=repair_candidate_time-accident_time
                    sum_arrive_time+=repair_time.seconds*1000#タイムアウトじの応答時間を合計値に加算(ミリ秒単位)
                    if N<=error_count:
                        print("\n")
                        print("故障サーバーのIPアドレス:" + str(repair_candidate_IP))
                        print("故障期間:"+str(accident_time)+" -> "+str(repair_candidate_time))
                        timeout_flag=1
                    break
                
                else:
                    error_continue_flag.append(j)
                    error_count+=1
                    if j==log_count-1:
                        timeout_flag=1
                        print("ネットワーク"+str(accident_IP)+"は故障中です故障期間は"+str(accident_time)+"～")

 
    
    """平均応答時間の計算"""
    ave_arrive_time=sum_arrive_time/m
    



    """過負荷状態のお知らせ"""
    if t<ave_arrive_time:
        print("\n")
        print(str(normal_IP) + "が過負荷状態です。平均応答時間が"+str(round(ave_arrive_time,2))+"ミリ秒です。")
        print("過負荷状態が発生した期間は"+str(oldest_log)+" -> "+str(latest_log)+"です。")
    if t>ave_arrive_time and timeout_flag==0:
        print("ネットワーク"+str(normal_IP)+"は正常です。")
    print("\n")
"""メインループ終わり"""                


