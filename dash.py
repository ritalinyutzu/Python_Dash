class test:
    def __init__(self):
        self.foo = 11
        self._bar = 23
        self.__baz = 45

t = test()
# 用dir回傳物件成員清單
dir(t) # 被改名成 '_test__baz' 了! -> Python直譯器做出的"名稱修飾"

# 定義一個子類別 來繼承test 並試著在其建構子__init__ 裡覆寫父類別的所有屬性
class Extendedtest(test):
    def __init__(self):
        super().__init__() # 呼叫父類別的建構子 (建立在父類別的屬性) 否則子類別的建構子會完全將之覆蓋
        self.foo = '已覆寫' # 嘗試覆寫
        self._bar = '已覆寫' # 嘗試覆寫
        self.__baz = '已覆寫' # 嘗試覆寫

t2 = Extendedtest()
t2.foo #>>> '已覆寫'
t2._bar #>>> '已覆寫'
t2.__baz #>>> AttributeError: 'Extendedtest' object has no attribute '__baz' 是不能修改的喔!!!
dir(t2) # baz又找不到了, 變成 '_Extendedtest__baz' 又是python名稱修飾 原本的__baz 屬性已經被改名 但父類別的'_test__baz'也仍然存在 沒有被子類別覆寫

# >>> conclusion : 前雙底線導致的名稱修飾結果 只會存在類別之外

print('---------------- 舉個栗子 ----------------')

class temp_test:
    def __init__(self):
        self.__rita = 'Rita' # 在建構子建立前雙底線名稱的屬性

    def get_rita(self): # 存取並傳回屬性的method 
        return self.__rita

t3 = temp_test()
t3.get_rita() # Rita (method可以用未修飾的名稱存取屬性)

t3.__rita #>>> AttributeError: 'temp_test' object has no attribute '__rita' 從外部無法以未修飾的屬性名稱取到(找不到此名稱 翻開覆蓋在檯面的陷阱卡)
t3._temp_test__rita #>>> Rita (對外部來說 物件屬性名稱已經改變成Rita)

print('---------------- 再來個栗子 連method 與其他名稱也能修飾 ----------------')

class rita_method:
    def __rita(self): # 使用雙底線名稱的method
        return 87

    def call_it(self): # 呼叫__rita 的 method
        return self.__rita()

t4 = rita_method()
t4.__rita() #>>> AttributeError: 'rita_method' object has no attribute '__rita' 直接使用雙底線呼叫 會找不到此名稱成員
t4.call_it() #>>> 87 這個 method 可以用原始名稱呼叫__rita()
t4._rita_method__rita() #>>> 87 從外部看 __rita() 已被改名

print('---------------- 再來個極端的栗子 ----------------')

_ritaGlobal__rita = 78 # 全域變數

class ritaGlobal:
    def df(self):
        return __rita # 名稱修飾後會指向全域變數(_ritaGlobal__rita)

ritaGlobal().df() #>>> 78

"""
先宣告_ritaGlobal__rita為全域變數, 在類別裡存取__rita
由於名稱修飾的作用 python直譯器會把類別中的__rita擴展成 _ritaGlobal__rita 剛好指向全域變數
所以可以在物件內以__rita來存取此全域變數
consequently: 只要在類別範圍內, 任何__雙底線開頭的名稱都會被python直譯器改寫, 名稱修飾不拘限於類別成員
"""

print('---------------- Python保留的特殊名稱 栗子 但最好不要這樣瞎搞 ----------------')

# 如果類別成員前後都有雙底線 就不會啟動名稱修飾 Python直譯器就不會去改寫他惹
class special_test:
    def __init__(self):
        self.__rita__ = 87

special_test().__rita__ #>>> 87

"""
Python把前後都有雙底線的名稱保留為"特殊用途"
e.g. __init__ 是物件建構子, __call__ 可以讓物件變成可呼叫物件 etc.,
雖然Python 可以使用前後都雙底線的變數名稱 但最好還是不要這樣命名類別成員
"避免與未來的Python功能起衝突啦!!!"
"""

print('---------------- 單底線栗子 其實是無名的暫時變數 ----------------')
# 只有一個底線的變數名稱 通常拿來代表一個暫時或不重要的變數
for i in range(87):
    print('Hello Rita')
# 這for loop其實不需要存取變數i的值 只是拿它來計算迴圈的次數 因此 i 可以用 _ 來取代

for _ in range(87):
    print('Hello Rita')
# 耶 效果一樣!
"""
單底線變數 可以用於Unpacking Expressions 也就是在拆解一系列值並指定給幾個變數時 我們可以略過當中的幾個值 不用特別設立變數去儲存 (垃圾暫存區)
"""
advantech = ('Neihu', 'IPC', 2022, 66) # 我隨便取的

location,_,_,date = advantech # tuple內的元素會分別指定給各個變數 (解包 解壓縮的感覺)
location #>>> Neihu
date #>>> 66
_ #>>> 2022 !!!單底線變數會先儲存第一個變數IPC,再儲存第二個單底線變數2022,所以最後保留的值就是2022

print('---------------- 如果很懶的話啦 ----------------')
"""
Python 的Terminal裡 "_" 會儲存直譯器裡 最後一次的執行結果
"""
print(_) #>>> 2022 這不就是剛剛最後一個保留的單底線變數2022嗎?

"""
前單底線:  _var : 命名慣例, 代表僅限給內部使用者的名稱,python直譯器不會改寫此種名稱, 只是開發者寫給其他工程師看, 最好別改我變數的小提示
後單底線: var_ : 命名慣例, 有些詞彙在python裡有特殊意義, 這時候加個後底線, 就不會跟Python關鍵字起衝突, 例如 class_ 這樣就沒毛病啦!
前雙底線: __var : 私有屬性, 會被Python直譯器發動名稱修飾,以避免被子類別的可能同名屬性覆寫QQ
前後雙底線: __var__ : Python中的特殊類別method 最好少用
前底線: _ : 暫時性或不重要的垃圾變數 或者Terminal最後一道執行結果
"""
