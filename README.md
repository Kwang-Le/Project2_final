# CongVRP - improved

## Hướng dẫn biên dịch

Chương trình được viết bằng **python 3** nên trước khi bắt đầu, bạn hãy cài đặt **python** phiên bản 3. trên máy tính của bạn.

### Bắt đầu Python Interpreter

Cách đơn giản nhất để khởi động trình thông dịch là sử dụng trình thông dịch từ command-line.

Để mở command-line:

* Trên Windows, command-line được gọi là Command Prompt hoặc MS-DOS consoler. Một cách nhanh hơn để truy cập nó là vào **Start menu → Run** và nhập **cmd**.
* Trên GNU / Linux, command-line có thể được truy cập bởi một số ứng dụng như xterm, Gnome Terminal hoặc Konsole.
* Trên MAC OS X, thiết bị đầu cuối hệ thống được truy cập thông qua **Application → Utilities → Terminal**.

### Chạy một chương trình python sử dụng lệnh python

Cách cơ bản và dễ dàng nhất để chạy một file code python là sử dụng lệnh python. Bạn cần mở command-line và nhập **python3**, theo sau là đường dẫn đến một file code python như sau:

```
python3 main.py
```
khi được prompt chọn dữ liệu thì chọn là 60

Sau đó, bạn nhấn nút ENTER từ bàn phím và thế là xong. Tuy nhiên, nếu trình biên dịch báo lỗi, bạn có thể muốn kiểm tra PATH hệ thống về python và nơi bạn đã lưu trình biên dịch python của mình. Nếu nó vẫn không hoạt động, hãy cài đặt lại Python trong hệ thống của bạn và thử lại.

### Cài đặt các package 

Các tên của các package python được liệt kê trong `requirements.txt`.
Để cài đặt dùng lệnh sau trên command-line.

```
pip3 install -r requirements.txt
```

## Hướng dẫn sử dụng

### Đầu vào

Dữ liệu đầu vào sẽ chứa các cặp số thực biểu diễn giá trị của tọa độ X, Y của các điểm cần đến thăm trên bản đồ.

```python
data = [
    [8.939456842504736187e+02,4.034761063045534115e+02],
    [3.876890450146825060e+02,6.365656595380232829e+02],
    [9.179568634971359415e+02,2.524852304516690538e+02],
    [4.984700666820613719e+02,5.718856100176336668e+02],
    [3.177208396865226518e+02,1.689009229311310207e+02],
    [3.406770451677099345e+02,1.766252302125570495e-01],
    [2.321265600102241251e+02,3.758932595845091669e+02],
    [9.227534234393247061e+02,3.783611811828674263e+02],
    [2.987965070982887710e+02,6.020048512896006514e+02],
    [1.569800465577046964e+02,9.081312698079268557e+02],
    [8.832993640408167266e+02,7.860719698045464838e+02],
    [5.763923703313139413e+02,3.213482251096589835e+02],
    [9.634357056838834978e+02,4.113774352097954079e+01],
    [1.628308135673014476e+02,3.765182706815184588e+02],
    [4.604527009989528779e+02,3.560993549294757372e+02],
    [7.126259196387081829e+02,8.831912276632413068e+02],
    [9.108697068040797831e+02,3.246276450691532034e+01],
    [4.226714572837595369e+02,4.210921054621774573e+01],
    [7.798047646904439034e+02,4.464049089891056497e+02],
    [2.964270780894551081e+02,5.559091429551311876e+02],
    [8.518235510401278816e+02,1.361604570297928376e+02],
    [2.555905546142363960e+02,6.188373006466875950e+02],
    [3.016768075716998965e+02,8.344125542226516927e+02],
    [7.992160820610076826e+02,1.136505902495069620e+02],
    [5.315974283578809718e+02,7.752571303049539893e+02],
    [2.173965210752745065e+02,3.087357231809215818e+02],
    [9.411071705392539570e+02,6.857129196540954581e+02],
    [9.906180452320282939e+02,5.173935570763660508e+02],
    [5.118480983837188205e+02,5.742198526817301172e+02],
    [1.351969848718115230e+01,6.487034169276801094e+02]
]
```




