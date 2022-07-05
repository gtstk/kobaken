import pandas as pd

sta=int(input("連番の初めの番号を入力してください:"))
end=int(input("連番の最後の番号を入力してください:"))
loop=end-sta+1

for i in range(loop):
    num=str(i+sta)
    df=pd.read_csv("data_"+num, header=None, comment="#", delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) #パスは要確認
    df.to_csv("data_"+num+".csv", index=False, header=False)