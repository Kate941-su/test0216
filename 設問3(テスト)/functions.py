# -*- coding: utf-8 -*-
import datetime


#文字からdatetimeへ
def string_to_datetime(string_date):
    dateobj=datetime.datetime.strptime(string_date,'%Y%m%d%H%M%S')
    return dateobj


#同一サーバー判別
def check_same_server(Private_Ip):
    
    """引数からプレフィクスつきのIPアドレス取得"""
    private_ip_index=0
    subnet_index=1
    P_Ip_list=Private_Ip.split("/")#サブネットとIP部分を分離
    P_Ip_detail=P_Ip_list[private_ip_index].split(".")
    subnet_10=int(P_Ip_list[subnet_index])


    """サブネット二進数"""        
    subnet_2=0b00
    for i in range(1,subnet_10+1):
        subnet_2+=2**(32-i)
        
    """プライベートIP二進数"""
    first_eight_bit=int(P_Ip_detail[0])*2**24
    second_eight_bit=int(P_Ip_detail[1])*2**16
    third_eight_bit=int(P_Ip_detail[2])*2**8    
    fourth_eight_bit=int(P_Ip_detail[3])    
    IP_2=0b00
    IP_2=first_eight_bit+second_eight_bit+third_eight_bit+fourth_eight_bit

    """AND演算"""        
    result=IP_2&subnet_2

    return result


"""ファイルを読み込んでリストにして返す"""
def file_read(FilePath):
    lis=[]
    arrive_time_index=0
    private_ip=1
    response_time=2
    with open(FilePath) as f:
        
        """ファイルを1行ずつ読み込む終わったらループを抜ける"""
        while True:
            file_line=f.readline()
            if not file_line:
                break       
            
            """カンマで分解リストに格納"""
            detail=file_line.split(",")#リストに格納する
            detail[arrive_time_index]=string_to_datetime(detail[arrive_time_index])#文字型をdatetime型に変換する
            
            """応答時間をint型に変換。エラーのハイフンは-999にして扱いやすくする"""
            try:
                detail[response_time]=int(detail[response_time])
            except:
                detail[response_time]=-999#エラーを扱いやすいように-999でフラグを立てる

            """辞書をリストに格納"""
            lis.append({"Private_Ip":detail[private_ip],"Arrive_Time":detail[arrive_time_index],"Response_Time":detail[response_time]})
            print(file_line)#デバッグ用
        print("\n\n")
        return lis

    
"""log_listを各サーバーごとに分割する"""
def split_each_server(Log_list,Prefix_count,Prefix_list):
    new_log_list=[ [] for i in range(Prefix_count)]
    for serch_server in Log_list:
        serch_prefix=check_same_server(serch_server["Private_Ip"])
        for j in range(Prefix_count):
            if Prefix_list[j] == serch_prefix:
                new_log_list[j].append(serch_server)  
    return new_log_list

"""直近m回のリストの作成"""
def make_latest_m_list(List,M):
    """戻り値用空リスト"""
    return_list=[]
    """引数で受け取ったリストの長さ"""
    List_count=len(List)    
    """入力されたmがリストより大きかったらそのままリストを返す"""
    if M>=List_count:
        return List
    else:
        for i in range(List_count-M,List_count):
            return_list.append(List[i])
        return return_list

