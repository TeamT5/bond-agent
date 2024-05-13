# bond-agent

這是一個可以常駐在端點上等待執行測試應用任務的專案

## 注意事項
* Python 使用至少 3.8.0 以上
* 此專案在 windows 環境中將強制使用 administrator 權限

## 如何安裝

* Clone 專案
  
* 使用虛擬環境
  * virtualenv
  
    ```shell
    virtualenv .env
    .env\Scripts\activate
    pip install -r ./requirements.txt
    ```

  * poetry

    ```shell
    poetry shell
    poetry install
    ```

## 如何使用

* 請先將服務執行起來
    * prod 環境
  
    ```shell
    python main.py
    ```

    * dev 環境
  
    ```shell
    python main.py -d5 T
    ```

  * Windows 環境下將默認縮小化到右下應用程式托盤中

* 打開瀏覽器併訪問以下位置，查看是否正確運行
    
    ```shell
    http://localhost:8086
    http://127.0.0.1:8086
    ```